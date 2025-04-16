"""
Author(s): Grant Morfitt/Phuong Tran
6.15.2023
"""

import grpc
import StateStore_pb2_grpc as pb2_grpc
import StateStore_pb2 as pb2
import time
from datetime import datetime
import pytz
import os.path
import json
import atomics
import collections
import csv
import curses
import time
import tomli

STATEID_LOOKUP = {}

VARIABLE_PRECISION = {}

outputVars = {}
outputFileVarDescriptions = {}

stateIDs = []

currentAircraft = None

outputDict = collections.OrderedDict()
outputFile = None

subscribe_response = None

dataCapturing = False
dataLoaded = False
simPaused = False

threadFlag = atomics.atomic(width=4, atype=atomics.INT) #Thread friendly variable
threadFlag = 2

stdscr = None

toml_dict = None

class Client(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = '192.168.168.11'
        self.server_port = 5011

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.StateStoreStub(self.channel)


def ConnectClient() -> None:
    
    global client, sub_request
    
    client = Client()
    
    sub_request = pb2.SubscribeStatesRequest(state_ids=stateIDs,
                                      notify_empty_change_sets = True,
                                      notify_unchanged = True,
                                      minimum_notification_interval_ms = 16)
          
def StartDataCapture() -> None:
    '''
        Connect to gRPC client and start collection
    
        Returns
        -------
        None

    '''
    global outputDict #Need reference to outside global variable
    global outputFile
    global dataCapturing
    global simPaused
    global VARIABLE_PRECISION
    dataCapturing = True

    global subscribe_response
    subscribe_response = client.stub.SubscribeStates(sub_request)

    fileName_UTC = pytz.timezone('UTC')
    current_time = fileName_UTC.localize(datetime.utcnow()) #Name the file
    current_time = current_time.strftime("%m%d%Y_%H%M%S")
    
    stdscr = InitializeOutput()
    fileName =  f"{currentAircraft}_{current_time}.csv"
    outputFile = open(f"C:\\Users\\TestCrew\\Documents\\{fileName}", "w+", newline = '')
    
    writer = csv.DictWriter(outputFile, fieldnames=outputVars)
    writer.writeheader()
    writer.writerow(outputFileVarDescriptions)#After the header, second row will give descriptions of each variable based on toml
    
    oldTime = time.time()

    print("test")
    for reply in subscribe_response:
        if (threadFlag == 2):
            
            newTime = time.time()
            timeElapsed = newTime - oldTime
            dataRate = round(1000.0 * timeElapsed)
            oldTime = newTime
            
            utc = pytz.timezone('UTC')
            current_time = utc.localize(datetime.utcnow())
            
            outputDict["Datetime"] = str(current_time)
              #  Each return_value should be StateValue
              #  And each StateValue should have state ID and an union of value
              # Populate dictionary values each loop and write out to the file using dictwriter. Close file after stop button pressed
            value_array = reply.values
            for value in value_array:        
         
                recieveVal = ""
                
                message_value = getattr(value, value.WhichOneof('value'))
                
                valueDataType = value.WhichOneof('value')

                state_id = value.state_id
                vartempName = STATEID_LOOKUP[state_id]
                variablePrecision = VARIABLE_PRECISION[vartempName] #Get lookup from variable precision table. # to round to
                
                 #This is only if notprimative
                if ((valueDataType != "boolean_value") and (valueDataType != "int32_value") and (valueDataType != "double_value") and (valueDataType != "string_value") ):
             
                     # Then we get the number of fields a the value has, like double2 should have two fields. etc
                    field_list = message_value.ListFields()
                    num_field = len(field_list)
                 
                     # Loop through each field of a type, like double2 should have 2 fields, named value_0 and value_1
                     
                    index = 0
                    for (field_desciptor, field_value) in field_list:
                         # field_desciptor.name is the name of the field
                         # And field value is the actual value of the field.
                         # So you can print it out like this
                         #print(f"{field_desciptor.name}: {field_value}")
                 
                         # Or you can create the string of value join by a comma too
                        if index == num_field - 1:
                            recieveVal += f"{field_value}"
                        else:
                            recieveVal += f"{field_value}, "
                 
                        index += 1
                    
                    variableName = STATEID_LOOKUP[state_id] #find name of variable from lookup table
                    outputDict[variableName] = recieveVal
                 
                else:
                    variableName = STATEID_LOOKUP[state_id] #find name of variable from lookup table

                   
                    precisionVal = VARIABLE_PRECISION[variableName]
                   
                    if precisionVal != "default": #if no precision val found in toml, we set to "default" when loading in   
                        #print(precisionVal)
                        roundedVal = round(message_value, precisionVal)
                        outputDict[variableName] = roundedVal
                    elif precisionVal == "default":
                        outputDict[variableName] = message_value
                    
                    #print(variableName)
                    if (variableName == "Aerofly_Out_Simulation_Pause" and str(message_value) == "True"): #will set simpause to true to prevent recorded paused data
                        simPaused = True
                    if (variableName == "Aerofly_Out_Simulation_Pause" and str(message_value) == "False"):
                        simPaused = False
                        
                stdscr.addstr(2,1, f"Current Aircraft: {currentAircraft}")
                stdscr.addstr(4,1, f"Sim Paused: {simPaused}") #Print out to the console for user viewing
                stdscr.addstr(5,1, f"Filename: {fileName}")
                stdscr.addstr(6,1, f"Current Time: {current_time}")
                stdscr.addstr(7,1, f"Message Data Rate: {dataRate} ms")
                stdscr.refresh()

  
        elif (threadFlag == 0):
            print("")
            break;

                
        if (simPaused == False and threadFlag != 0 ): #This is where we will write to the file after each message has been processed

            writer.writerow(outputDict)       

def LoadStartData() -> bool:
    '''
    Load dictionary in that contains lookup data/stateids 

    Returns
    -------
    
    Returns value that tells if startup loaded properly. Used to update text on GUI and alert user

    '''
    global toml_dict
    global STATEID_LOOKUP
    global stateIDs
    global currentAircraft
    global VARIABLE_PRECISION
    
    try: 
        
        #f = open("StateDescriptions.json", "r")
        #txt = f.read()
        toml = open("config.toml", "rb")
        toml_dict = tomli.load(toml)['outputvariables']
        
        #myDict = json.loads(txt)
        print("TOML File Found")
        
        for value in toml_dict:
           
            if (isinstance(toml_dict[value],str) == False):     #We can't index a string. I mean..you can technically, but not this way.
                currentItem = toml_dict[value]
                current_id = currentItem['state_id']
                
                if (("precision" in currentItem) == True):#Check to see if this variable has a precision value
                    print("precision value found!")
                    current_precision = currentItem['precision'] #If it doesn't we just leave it blank
                    VARIABLE_PRECISION[value] = current_precision
                    
                else:
                    test = ("precision" in currentItem)
                    VARIABLE_PRECISION[value] = "default"
                    
                stateIDs.append(current_id)
                STATEID_LOOKUP[current_id] = value
              
        dataLoaded = True
        
        return True;
    
    except Exception as e: 
        print(e)
        print ("TOML File Not Found!")
        return False;

def InitializeOutput():
    global outputDict
    global outputFileVarDescriptions
    global outputFile
    #global stdscr
    global toml_dict
    global currentAircraft
    
    stdscr = curses.initscr() #Used to print stuff to the screen for monitoring data
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    
    for value in toml_dict:
        if (isinstance(toml_dict[value],str) == False): 
            currentItem = toml_dict[value]
            current_description = currentItem['description']
            current_stateID = currentItem
            outputVars[value] = None #Set up initial dictionary for outputting data to excel
            outputFileVarDescriptions[value] = current_description #Get descriptions for each variable from the toml file
            
        if (isinstance(toml_dict[value],str) == True):
            
            if (value == "aircraft_type"):
                currentAircraft = toml_dict[value]
                outputVars[value] = toml_dict[value]
                outputFileVarDescriptions["aircraft_type"] = currentAircraft
                
            if (value == "Datetime"):
                outputVars[value] = toml_dict[value]
                
    outputDict = collections.OrderedDict.fromkeys(outputVars)
    
    return stdscr
    #return None

def StopDataCapture() -> None:
    
    global outputFile
    global subscribe_response

    try:
         
        subscribe_response.cancel() #Call server to stop sending data. TThrows exception##       
        
    except Exception as e:
        print("ERROR:" + str(e))

    finally:
        outputFile.close()
        
        threadFlag == 0
        dataCapturing = False
        
        curses.nocbreak() #Close up the terminal
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        
    print("Stopping")

def IsDataCapturing() -> bool:
    
    '''
    Pretending python has any semblance of data encapsulation
    
    Returns
    -------
    bool
        Returns bool that shows if data is currently being captured.
    '''
    return dataCapturing;

    
    





















