"""
@author: Grant Morfitt
grant.e.morfitt@faa.gov

"""
import grpc
import StateStore_pb2_grpc as pb2_grpc
import StateStore_pb2 as pb2
import tkinter as tk
from tkinter import ttk
import datetime
import tomli
import collections
import csv
import os 
from threading import Thread
import threading
from queue import Queue

class SimulatorGUI:
    """
    Sets up the GUI window for simulator session data recording
    and connects required functions to buttons.
    """
    def __init__(self, master):
        """
        Initializes the SimulatorGUI.

        Args:
            master: The root Tkinter window.
        """
        self.pilot_Lookup = [] #these are going to store the lookup tables imported from the IOHelper class/toml configs
        self.block_Lookup = []
        self.lesson_Lookup = []
        self.maneuver_Lookup = []
        
        self.pilotCombo = None #These will store the combo boxes to be updated after files are initialized
        self.blockCombo = None
        self.lessonCombo = None
        self.maneuverCombo = None
        
        self.recordingStatus = None
        
        self.startButton = None
        self.stopButton = None
        self.timeButton = None
        self.deleteFileButton = None
        
        self.maneuverStopbtn = None
        self.maneuverStartbtn = None
        self.maneuverCancelbtn = None
        
        self.commentEntry = None
        self.timeLabel = None
        self.grpcControl = None
        self.IOHelper = IOHelper() #instance of IOhelper class
        self.stop_event = None
        self.recorder_thread = None
        
        
        self.master = master
        master.title("Simulator Session Data Recording")
        master.geometry("800x550")
        master.configure(bg="lightgray")
        
        
        self.create_widgets()
        self.initialize_files()
        self.master.resizable(False, False)
        self.log_message("Select Parameters to Continue")
        
    def create_widgets(self):
        """Creates and arranges the widgets for the GUI."""
        # Main title
        tk.Label(self.master, text="Simulator Session Data Recording", font=("Arial", 16)).pack(pady=10)

        # Simulation control buttons
        sim_frame = tk.Frame(self.master, bg="lightgray")
        sim_frame.pack()
        
   
        self.startButton = tk.Button(sim_frame, text="Start Simulation", bg="green", fg="white", width=20, takefocus=False, highlightthickness = 0, command=self.start_simulation)
        self.startButton.pack(side = "left", pady=2)
        self.startButton['state'] = 'disable'
        
        
        
        self.stopButton = tk.Button(sim_frame, text="Stop Simulation", bg="red", fg="white", width=20, takefocus=False, highlightthickness = 0, command=self.stop_simulation)
        self.stopButton.pack(pady=2)
        self.stopButton['state'] = 'disable'
        
        delete_frame = tk.Frame() #put delete button off to the side of the start button
        #delete_frame.pack(fill = "x", padx = 5)
        delete_frame.place(x=605, y=10)
        self.deleteFileButton = tk.Button(delete_frame, text="Delete File", bg="orange", fg="white", width=20, command = self.delete_file)
        self.deleteFileButton.pack(side = "right")
        self.deleteFileButton['state'] = 'disable'
       

        # Left panel: Pilot, Block, Lesson
        left_frame = tk.LabelFrame(self.master, text="", padx=10, pady=10)
        left_frame.place(x=20, y=80)

        tk.Label(left_frame, text="Pilot:").grid(row=0, column=0, sticky="w")
        self.pilotCombo = ttk.Combobox(left_frame, values=self.pilot_Lookup, width=15)
        self.pilotCombo.grid(row=0, column=1, pady=2)
        self.pilotCombo.bind("<<ComboboxSelected>>", self.checkcombobox)
        
        tk.Label(left_frame, text="Block:").grid(row=1, column=0, sticky="w")
        self.blockCombo = ttk.Combobox(left_frame, values=self.block_Lookup, width=15)
        self.blockCombo.grid(row=1, column=1, pady=2)
        self.blockCombo.bind("<<ComboboxSelected>>", self.checkcombobox)

        tk.Label(left_frame, text="Lesson:").grid(row=2, column=0, sticky="w")        
        self.lessonCombo = ttk.Combobox(left_frame, values=self.lesson_Lookup, width=15)
        self.lessonCombo.grid(row=2, column=1, pady=2)
        self.lessonCombo.bind("<<ComboboxSelected>>", self.checkcombobox) #trace will callback check function
        
        maneuver_frame = tk.LabelFrame(self.master, text="", padx=10, pady=10)
        maneuver_frame.place(x=580, y=80, width=200, height=250)
        tk.Label(maneuver_frame, text="Maneuver:").pack(anchor="w")
        

        
        self.maneuverCombo = ttk.Combobox(maneuver_frame, values=[""], width=20)
        self.maneuverCombo.pack(pady=5)

        # Recorder status
        status_frame = tk.Frame(self.master, bg="white", bd=1, relief="solid")
        status_frame.place(x=215, y=160, width=350, height=30)
        tk.Label(status_frame, text="Recorder Status: ", bg="white").pack(side="left")
        
        self.recordingStatus = tk.Label(status_frame, text="Not Recording", fg="red", bg="white")
        self.recordingStatus.pack(side="left")

        # Recorder log
        log_frame = tk.Frame(self.master, bd=1, relief="solid")
        log_frame.place(x=215, y=190, width=350, height=250)
        tk.Label(log_frame, text="Recorder Log:", anchor="w").pack(fill="x")
        self.log_text = tk.Text(log_frame, height=5, wrap="word")
        self.log_text.pack(fill="both", expand=True)

        # Maneuver controls
        self.maneuverStartbtn = tk.Button(maneuver_frame, text="Start Maneuver", bg="green", fg="white", width=20, command=self.start_maneuver)
        self.maneuverStartbtn.pack(pady=2)
        self.maneuverStartbtn['state'] = 'disabled'
        self.maneuverStopbtn = tk.Button(maneuver_frame, text="Stop Maneuver", bg="red", fg="white", width=20, command=self.stop_maneuver)
        self.maneuverStopbtn.pack(pady=2)
        self.maneuverStopbtn['state'] = 'disabled'
        self.maneuverCancelbtn = tk.Button(maneuver_frame, text="Cancel\nManeuver", bg="orange", fg="white", width=20, height=2, command=self.cancel_maneuver)
        self.maneuverCancelbtn.pack(pady=2)
        self.maneuverCancelbtn['state'] = 'disabled'
        # Comment section
        comment_frame = tk.Frame(self.master, bd=1, relief="solid", padx=10, pady=5)
        comment_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        tk.Label(comment_frame, text="Comment:").pack(side="left")
        
        #self.commentEntry = comment_entry = tk.Entry(comment_frame, width=70)
        self.commentEntry = comment_entry = tk.Text(comment_frame, width = 55, height = 4)
        comment_entry.pack(side="left", padx=5)

        tk.Button(comment_frame, text="Submit", bg="gray", fg="white", width=8, command=self.submit_comment).pack(side="right")
        self.timeButton = tk.Button(comment_frame, text="Time", bg="gray", fg="white", width=8, command=self.add_timestamp_to_comment)
        self.timeButton.pack(side="right", padx=5)

    
        self.timeLabel = tk.Label(comment_frame, text="HH:MM:SS")
        self.timeLabel.pack(side="right")

    def initialize_files(self):
        
        print("Load files")
        #Create instance of Setup class
        
        IOStatus1, IOStatus2 = self.IOHelper.InitializeParameters() #Initialize output header and lookup tables
        
        self.pilot_Lookup = self.IOHelper.pilot_Lookup
        self.block_Lookup = self.IOHelper.block_Lookup
        self.lesson_Lookup = self.IOHelper.lesson_Lookup
        self.maneuver_Lookup = self.IOHelper.maneuver_Lookup
        
        if (IOStatus1,IOStatus2) == (1,1):
            self.log_message("toml files loaded")
            self.update_combobox()
            
        if (IOStatus1,IOStatus2) != (1,1):

            self.log_message("ERR: toml setup failed")
    
    def update_combobox(self):
        self.pilotCombo["values"] = self.pilot_Lookup
        self.blockCombo["values"] = self.block_Lookup
        self.lessonCombo["values"] = self.lesson_Lookup
        self.maneuverCombo["values"] = self.maneuver_Lookup
    
    def checkcombobox(self, *_):
        """
        Check that all combo boxes are filled before enabling the start button

        Parameters
        ----------
        *_ : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        if self.pilotCombo.get() and self.blockCombo.get() and self.lessonCombo.get():
            self.startButton['state'] = 'normal'
        else:
            print ("not all boxes are selected, womp womp")
            
        
    def start_simulation(self):
        
        self.stop_event = threading.Event() #event to stop thread recording data
        self.log_message("Simulation started")
        
        pilotSelected = self.pilotCombo.get()
        blockSelected = self.blockCombo.get()
        lessonSelected = self.lessonCombo.get()
        
        #print(f"pilot selected: {pilotSelected} ")
        file = self.IOHelper.CreateOutputFile(pilotSelected, blockSelected, lessonSelected)
        
        self.grpcControl = GRPCControl(file, self.IOHelper)
 
        self.grpcControl.ConnectClient()
        
        self.recorder_thread = threading.Thread(target=self.grpcControl.SubscribeData, args=(self.stop_event,))
        self.recorder_thread.start()
        
        self.recordingStatus['text'] = "Recording"
        self.recordingStatus['fg'] = "green"
        self.stopButton['state'] = 'normal'
        self.startButton['state'] = 'disabled'
        self.maneuverStartbtn['state'] = 'normal'
        self.deleteFileButton['state'] = 'normal'
        

    def stop_simulation(self):
        """Placeholder for stop simulation functionality."""
        self.log_message("Simulation stopped")
        self.recordingStatus['text'] = "Not Recording"
        self.recordingStatus['fg'] = "red"
        
        self.stop_event.set()
        self.grpcControl.StopDataCapture()
        
        
        self.recorder_thread.join()
        
        self.IOHelper.CloseFile()
        self.stop_event = None
        
        self.maneuverStartbtn['state'] = 'disabled'
        self.maneuverStopbtn['state'] = 'disabled'
        self.maneuverCancelbtn['state'] = 'disabled'
        self.stopButton['state'] = 'disabled'
        self.startButton['state'] = 'normal'
        
        self.grpcControl = None
    
    def delete_file(self):
        print("file marked for deletion")
        self.deleteFileButton['state'] = 'disabled'
        self.maneuverStartbtn['state'] = 'normal'
        self.maneuverStopbtn['state'] = 'disabled'
        self.maneuverCancelbtn['state'] = 'disabled'
        
        self.stop_simulation()
        statusStr = self.IOHelper.DeleteFile()
        self.log_message(statusStr)
        
    def start_maneuver(self):

        self.maneuverStartbtn['state'] = 'disabled'
        self.maneuverStopbtn['state'] = 'normal'
        self.maneuverCancelbtn['state'] = 'normal'
        self.deleteFileButton['state'] = 'normal'
        maneuver_comment = f"START_{self.maneuverCombo.get()}"
        self.log_message(maneuver_comment)
     
        self.IOHelper.que.put(maneuver_comment)
        print(maneuver_comment)

    def stop_maneuver(self):

        self.maneuverStartbtn['state'] = 'normal'
        self.maneuverStopbtn['state'] = 'disabled'
        self.maneuverCancelbtn['state'] = 'disabled'
        
        maneuver_comment = f"STOP_{self.maneuverCombo.get()}"
        self.log_message(maneuver_comment)
     
        self.IOHelper.que.put(maneuver_comment)
        print(maneuver_comment)

    def cancel_maneuver(self):

        self.maneuverStartbtn['state'] = 'normal'
        self.maneuverStopbtn['state'] = 'disabled'
        self.maneuverCancelbtn['state'] = 'disabled'
        
        maneuver_comment = f"CANCEL_{self.maneuverCombo.get()}"
        self.log_message(maneuver_comment)
     
        self.IOHelper.que.put(maneuver_comment)
        print(maneuver_comment)
        
    def add_timestamp_to_comment(self):
        """Placeholder for adding timestamp to the comment."""
        print("Time button clicked")
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M:%S')
        
        self.timeLabel['text'] = current_time
        self.timeButton['state'] = 'disabled'
    
    def submit_comment(self):
        """Placeholder for submitting the comment."""
        print("Submit button clicked")
        
        time = self.timeLabel['text']
        commentText = self.commentEntry.get("1.0", "end-1c")
        comment = f"COMMENT_{time} {commentText}"
        
        self.IOHelper.que.put(comment)
        self.log_message(comment)
        
        self.commentEntry.delete("1.0", tk.END)
        self.timeLabel['text'] = "HH:MM:SS"
        self.timeButton['state'] = 'normal'
        
    def log_message(self, message):
        """Appends a message to the recorder log."""
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        self.log_text.insert(tk.END, f" {current_time} || {message}\n")
        self.log_text.see(tk.END) # Autoscroll to the bottom


class GRPCControl:
    """
    """
    
    def __init__(self, file, IOHelperInstance):
        
        self.host = '127.0.0.1'
        self.server_port = 5011
        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))
        # bind the client and the server
        self.stub = pb2_grpc.StateStoreStub(self.channel)
       
        self.IOHelper = IOHelperInstance
        self.fileOutput = file #file created and passed from IOSetup class
        self.fileHeader = self.IOHelper.blankOutputFileHeader #header for file created and passed form IOSetup class
        self.subscribe_response = None
            
        #print("outputdict "  + self.outputDict['Aerofly_Out_Aircraft_MagneticHeading'])
        
    def ConnectClient(self) -> None:
        
        global client, sub_request
        #client = Client()
        stateIDs = self.IOHelper.GetStateIDs() #pull stateids from list
        sub_request = pb2.SubscribeStatesRequest(state_ids=stateIDs,
                                          notify_empty_change_sets = True,
                                          notify_unchanged = True,
                                          minimum_notification_interval_ms = 16)
    
    def StopDataCapture(self):
        self.subscribe_response.cancel()
        
        
    def SubscribeData(self, stop_event):
        
       #need new instance of output dict here
        
        #subscribe_response = self.stub.SubscribeStates(sub_request)
        self.subscribe_response = self.stub.SubscribeStates(sub_request)
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M:%S.%f')[:-3]
        
          #  Each return_value should be StateValue
          #  And each StateValue should have state ID and an union of value
         
        print(stop_event.is_set())
        while not stop_event.is_set():
            try:
                for reply in self.subscribe_response:
   
                    value_array = reply.values
                    processedDict = self.IOHelper.ProcessGRPC(value_array)
                    self.IOHelper.WriteOutputLine(processedDict)
                    
            except:
                pass
       
    
class IOHelper:
    """
        Still need to input pilot and block information
    """
    
    def __init__ (self):
        self.dataParameter_Lookup = {}
        self.blankOutputFileHeader = {}
        self.pilot_Lookup = []
        self.block_Lookup = []
        self.lesson_Lookup = []
        self.maneuver_Lookup = []
        self.initialized = False
        
        self.simPaused = False
        
        self.outputDict = {key: '' for key in self.blankOutputFileHeader} #create blank output dictionary for processing replies from server
        self.outputFile = None
        self.writer = None
        
        self.que = Queue() #make a quene for comments/manuever info. Only one instance of this class is called
                            #so this queue will be checked when writing rows
        
    def GetPilots(self):
        return self.pilot_Lookup;
    
    def GetBlocks(self):
        return self.block_Lookup
    
    def GetLessons(self):
        return self.lesson_Lookup
    
    def GetStateIDs(self):
        
        paramlist = list(self.dataParameter_Lookup.keys())
        return [item for item in paramlist if isinstance(item, int)]
    
    def InitializeParameters(self):
        """
        Imports required config files 
        
        Returns
        -------
         Returns two status items. One for each config toml
        """
        lesson_status = self._ImportLessonToml()
        param_status = self._ImportParameterToml()
        
        if lesson_status and param_status == 1:   
            self.initialized = True
            #file = self._CreateFile(self.blankOutputFileHeader)
            return lesson_status, param_status
        
        return lesson_status, param_status
    
    def ProcessGRPC(self, value_array) -> dict:
        """
        Will take in value array from dict and return a dict of formatted values

        Parameters
        ----------
        valuearray : TYPE
            DESCRIPTION.

        Returns
        -------
        dict
            DESCRIPTION.

        """
        outputDict_copy = self.outputDict.copy()
        
        for value in value_array:        
     
            recieveVal = ""
            
            message_value = getattr(value, value.WhichOneof('value'))
            valueDataType = value.WhichOneof('value')

            state_id = value.state_id
            
            now = datetime.datetime.now()
            current_time = now.strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
            
            outputDict_copy["Datetime"] = current_time
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
                
                if state_id in self.dataParameter_Lookup:
                    variableName = self.dataParameter_Lookup[state_id]
                    outputDict_copy[variableName] = recieveVal  # or message_value
                else:
                    print(f"[WARNING] Unknown state_id received: {state_id}")
                #variableName = self.dataParameter_Lookup[state_id] #find name of variable from lookup table
                #outputDict_copy[variableName] = recieveVal
             
            else:
                variableName = self.dataParameter_Lookup[state_id] 

                outputDict_copy[variableName] = message_value
                
                if (variableName == "Aerofly_Out_Simulation_Pause" and str(message_value) == "True"): #will set simpause to true to prevent recorded paused data
                    self.simPaused = True
                if (variableName == "Aerofly_Out_Simulation_Pause" and str(message_value) == "False"):
                    self.simPaused = False
                
                if (self.simPaused == False): #This is where we will write to the file after each message has been processed
                    print("sim not paused writing lines")
                    print(variableName)
        return outputDict_copy
        
    
    def _ImportParameterToml(self):
        """
        Private function that imports the toml config for parameters from loft sim

        Returns
        -------
        1 if successful, 0 if not successful

        """
        try: 
            dirname = os.path.abspath(os.getcwd())
            filename = dirname + '\\config\\parameterconfig.toml'
            toml = open(filename, "rb")
            
            toml_dict = tomli.load(toml)['outputvariables']
            
            for value in toml_dict:
                if (isinstance(toml_dict[value],str) == False): 
                    currentItem = toml_dict[value]
                    current_description = currentItem['description']
                    current_stateID = currentItem["state_id"]
                    self.dataParameter_Lookup[current_stateID] = value
                    self.blankOutputFileHeader[value] = current_description 
                    
                if (isinstance(toml_dict[value],str) == True):
                    
                    if (value == "aircraft_type"):
                        currentAircraft = toml_dict[value]
                       # outputVars[value] = toml_dict[value]
                        self.blankOutputFileHeader["aircraft_type"] = currentAircraft
                        self.dataParameter_Lookup["aircraft_type"] = currentAircraft
                    if (value == "Datetime"):
                       # outputVars[value] = toml_dict[value]
                        self.blankOutputFileHeader["Datetime"] = None #outputVars[value]
                    if (value == "comments"):
                        self.blankOutputFileHeader["comments"] = None
            return 1
        except: 
            return 0
        
    def _ImportLessonToml(self):
        """
        Private function that imports the lesson toml config for parameters from loft sim

        Returns
        -------
        1 if successful, 0 if not successful

        """
        try: 
            dirname = os.path.abspath(os.getcwd())
            filename = dirname + '\\config\\lessonconfig.toml'
            toml = open(filename, "rb")
            
            toml_dict = tomli.load(toml)['lessonconfig']
            
            for value in toml_dict:
                if value == "pilots": 
                    for i in toml_dict[value]:
                        self.pilot_Lookup.append(i) #add each pilot to the lookup table
                        
                if value == "blocks": 
                    for i in toml_dict[value]:
                        self.block_Lookup.append(i) #add each pilot to the lookup table
                 
                if value == "lessons": 
                    for i in toml_dict[value]:
                        self.lesson_Lookup.append(i) #add each pilot to the lookup table
                if value == "maneuvers":
                    for i in toml_dict[value]:
                        self.maneuver_Lookup.append(i) #add each pilot to the lookup table
                     
            return 1
        except: 
            return 0
        
    def CreateOutputFile(self, pilot:str, block:str, lesson:str) -> object:
        
        print("Placeholder for cretefile")
        currentAircraft = self.dataParameter_Lookup["aircraft_type"]
        now = datetime.datetime.now()
        current_time = now.strftime('%H.%M.%S.%f')[:-3]
        
        fileName =  f"{currentAircraft}_{current_time}_{pilot}_{block}_{lesson}.csv"
        outputFile = open(f"C:\\Users\\gmorfitt\\Documents\\LoftLessonsGUI\\data\\{fileName}", "w+", newline = '')
        
        
        writer = csv.DictWriter(outputFile, fieldnames=self.blankOutputFileHeader)
        writer.writeheader()
        
        return outputFile
        #writer.writerow(outputFileVarDescriptions)#After the header, second row will give descriptions of each variable based on toml
    
    def CreateOutputFile(self, pilot:str, block:str, lesson:str):
        
        print("File created")
        currentAircraft = self.dataParameter_Lookup["aircraft_type"]
        now = datetime.datetime.now()
        current_time = now.strftime('%Y%m%d_%H%M%S')
        
        fileName =  f"{currentAircraft}_{current_time}_{pilot}_{block}_{lesson}.csv"
        self.outputFile = open(f"C:\\Users\\gmorfitt\\Documents\\LoftLessonsGUI\\data\\{fileName}", "w+", newline = '')
        
        print(self.outputFile)
        self.writer = csv.DictWriter(self.outputFile, fieldnames=self.blankOutputFileHeader)
        self.writer.writeheader()
        
    
    def WriteOutputLine(self, dataLine: dict):
        #writer.writerow(outputFileVarDescriptions)#After the header, second row will give descriptions of each variable based on toml
        
        #need to check queue and if something is in it, add it to a comments line

        if self.que.qsize() != 0: 
            queData = self.que.get()
            dataLine['comments'] = queData
            
        else:
            dataLine['comments'] = ""
        
        self.writer.writerow((dataLine))
   
    
    def CloseFile(self):
        self.outputFile.close()
    
    def DeleteFile(self) -> str:
        try:
            os.remove(self.outputFile.name)
            basename = os.path.basename(self.outputFile.name)
            return (f"{basename} deleted successfully.")
            
        except FileNotFoundError:
            basename = os.path.basename(self.outputFile.name)
            return(f"Error:'{basename}' not found.")
        except Exception as e:
            return(f"An error occurred: {e}")
        
def main():
    """Creates the main Tkinter window and runs the application."""
    
    root = tk.Tk()
    app = SimulatorGUI(root)
    
    #app.initialize_files()

    root.mainloop()

if __name__ == "__main__":
    main()
