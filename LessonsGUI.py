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
        self.master = master
        master.title("Simulator Session Data Recording")
        master.geometry("800x550")
        master.configure(bg="lightgray")

        self.create_widgets()

    def create_widgets(self):
        """Creates and arranges the widgets for the GUI."""
        # Main title
        tk.Label(self.master, text="Simulator Session Data Recording", font=("Arial", 16)).pack(pady=10)

        # Simulation control buttons
        sim_frame = tk.Frame(self.master, bg="lightgray")
        sim_frame.pack()

        tk.Button(sim_frame, text="Start Simulation", bg="green", fg="white", width=20, command=self.start_simulation).pack(pady=2)
        tk.Button(sim_frame, text="Stop Simulation", bg="red", fg="white", width=20, command=self.stop_simulation).pack(pady=2)

        # Left panel: Pilot, Block, Lesson
        left_frame = tk.LabelFrame(self.master, text="", padx=10, pady=10)
        left_frame.place(x=20, y=80)

        tk.Label(left_frame, text="Pilot:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(left_frame, values=["Pilot 1", "Pilot 2"], width=15).grid(row=0, column=1, pady=2)

        tk.Label(left_frame, text="Block:").grid(row=1, column=0, sticky="w")
        ttk.Combobox(left_frame, values=["Block 1", "Block 2"], width=15).grid(row=1, column=1, pady=2)

        tk.Label(left_frame, text="Lesson:").grid(row=2, column=0, sticky="w")
        ttk.Combobox(left_frame, values=["Lesson 1", "Lesson 2"], width=15).grid(row=2, column=1, pady=2)

        # Recorder status
        status_frame = tk.Frame(self.master, bg="white", bd=1, relief="solid")
        status_frame.place(x=250, y=160, width=300, height=30)
        tk.Label(status_frame, text="Recorder Status: ", bg="white").pack(side="left")
        tk.Label(status_frame, text="Recording", fg="green", bg="white").pack(side="left")
        tk.Label(status_frame, text="/", bg="white").pack(side="left")
        tk.Label(status_frame, text="Not Recording", fg="red", bg="white").pack(side="left")

        # Recorder log
        log_frame = tk.Frame(self.master, bd=1, relief="solid")
        log_frame.place(x=250, y=190, width=300, height=120)
        tk.Label(log_frame, text="Recorder Log:", anchor="w").pack(fill="x")
        self.log_text = tk.Text(log_frame, height=5, wrap="word")
       # self.log_text.insert("end", "• Simulation Start: XXhXXminXXs\n• XX Maneuver Start at XXhXXminXXs\n• XX Maneuver Stop at XXhXXminXXs")
        self.log_text.pack(fill="both", expand=True)

        # Maneuver controls
        maneuver_frame = tk.LabelFrame(self.master, text="", padx=10, pady=10)
        maneuver_frame.place(x=580, y=80, width=200, height=250)

        tk.Label(maneuver_frame, text="Maneuver:").pack(anchor="w")
        ttk.Combobox(maneuver_frame, values=["Maneuver 1", "Maneuver 2"], width=20).pack(pady=5)

        tk.Button(maneuver_frame, text="Start Maneuver", bg="green", fg="white", width=20, command=self.start_maneuver).pack(pady=2)
        tk.Button(maneuver_frame, text="Stop Maneuver", bg="red", fg="white", width=20, command=self.stop_maneuver).pack(pady=2)
        tk.Button(maneuver_frame, text="Cancel\nManeuver", bg="orange", fg="white", width=20, height=2, command=self.cancel_maneuver).pack(pady=2)

        # Comment section
        comment_frame = tk.Frame(self.master, bd=1, relief="solid", padx=10, pady=5)
        comment_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        tk.Label(comment_frame, text="Comment:").pack(side="left")
        comment_entry = tk.Entry(comment_frame, width=70)
        comment_entry.pack(side="left", padx=5)

        tk.Button(comment_frame, text="Time", bg="gray", fg="white", width=8, command=self.add_timestamp_to_comment).pack(side="left", padx=5)
        tk.Button(comment_frame, text="Submit", bg="gray", fg="white", width=8, command=self.submit_comment).pack(side="left")

    def start_simulation(self):
        print("Start Simulation button clicked")
    
        IOHelper = IOSetup() #Create instance of Setup class
        IOStatus = IOHelper.InitializeIO() #Initialize output header and lookup tables
        
        if IOStatus == 1:
            self.log_message("toml and setup loaded")
            
            
        if IOStatus == 0:

            self.log_message("ERR: toml or setup failed")
        

    def stop_simulation(self):
        """Placeholder for stop simulation functionality."""
        self.log_message("Simulation stopped.")
        print("Stop Simulation button clicked")

    def start_maneuver(self):
        """Placeholder for start maneuver functionality."""
        self.log_message("Maneuver started.")
        print("Start Maneuver button clicked")

    def stop_maneuver(self):
        """Placeholder for stop maneuver functionality."""
        self.log_message("Maneuver stopped.")
        print("Stop Maneuver button clicked")

    def cancel_maneuver(self):
        """Placeholder for cancel maneuver functionality."""
        self.log_message("Maneuver cancelled.")
        print("Cancel Maneuver button clicked")

    def add_timestamp_to_comment(self):
        """Placeholder for adding timestamp to the comment."""
        print("Time button clicked")



    
    def submit_comment(self):
        """Placeholder for submitting the comment."""
        print("Submit button clicked")

    def log_message(self, message):
        """Appends a message to the recorder log."""
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        self.log_text.insert(tk.END, f" {current_time} || {message}\n")
        self.log_text.see(tk.END) # Autoscroll to the bottom


class GRPCControl:
    """
    """
    
    def __init__(self):
        self.host = '192.168.168.11'
        self.server_port = 5011

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))
        # bind the client and the server
        self.stub = pb2_grpc.StateStoreStub(self.channel)
        self.outputDict = {}
    
    def ConnectClient(self) -> None:
        
        global client, sub_request
        #client = Client()
        stateIDs = []
        
        sub_request = pb2.SubscribeStatesRequest(state_ids=stateIDs,
                                          notify_empty_change_sets = True,
                                          notify_unchanged = True,
                                          minimum_notification_interval_ms = 16)
    
    def StartDataCapture(self):
        subscribe_response = self.stub.SubscribeStates(sub_request)
        
        
    def SubscribeDate(self):
        self.outputDict = {}
        subscribe_response = self.stub.SubscribeStates(sub_request)
        
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M:%S.%f')[:-3]
        
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
                
                if (simPaused == False and threadFlag != 0 ): #This is where we will write to the file after each message has been processed

                    writer.writerow(outputDict)
    
class IOSetup:
    """
        Still need to input pilot and block information
    """
    
    def __init__ (self):
        self.dataParameter_Lookup = {}
        self.blankOutputFileHeader = {}
        self.pilot_Lookup = []
        self.block_Lookup = []
        self.lesson_Lookup = []
        
    def InitializeIO(self):
        """
        Imports required config files
        
        Returns
        -------
         Returns status and list of pilots, lessons, and blocks.
        """
        
        return 1 if self._ImportParameterToml() else 0
        
     
        
    
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
                     
            return 1
        except: 
            return 0
        
    def _CreateFile(self):
        
        currentAircraft = self.dataParameter_Lookup["aircraft_type"]
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M:%S.%f')[:-3]
        
        fileName =  f"{currentAircraft}_{current_time}.csv"
        outputFile = open(f"C:\\Users\\gmorfitt\\Documents\\LoftLessonsGUI\\data\\{fileName}", "w+", newline = '')
        
        
        writer = csv.DictWriter(outputFile, fieldnames=outputVars)
        writer.writeheader()
        writer.writerow(outputFileVarDescriptions)#After the header, second row will give descriptions of each variable based on toml
        
    
def main():
    """Creates the main Tkinter window and runs the application."""
    root = tk.Tk()
    app = SimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
