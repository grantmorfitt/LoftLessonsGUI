import tkinter as tk
import tkinter.font as tkFont
import grcpClientRecieve
from datetime import datetime
import pytz
from threading import Thread
import queue 
import time
import sys
'''
Basic app for interface/control with data collection code
'''


class App:
    thread = None
    
    def __init__(self, root):
        #setting title
        root.title("Helo Recorder")
        #setting window size
        width=586
        height=354
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        btn_start=tk.Button(root)
        btn_start["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        btn_start["font"] = ft
        btn_start["fg"] = "#000000"
        btn_start["justify"] = "center"
        btn_start["text"] = "Start Collection"
        btn_start.place(x=170,y=190,width=106,height=30)
        btn_start["command"] = self.btn_start_command

        btn_stop=tk.Button(root)
        btn_stop["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        btn_stop["font"] = ft
        btn_stop["fg"] = "#000000"
        btn_stop["justify"] = "center"
        btn_stop["text"] = "Stop Collection"
        btn_stop.place(x=300,y=190,width=105,height=30)
        btn_stop["command"] = self.btn_stop_command

        global GLabel_875;
        GLabel_875=tk.Label(root)
        ft = tkFont.Font(family='Times',size=12)
        GLabel_875["font"] = ft
        GLabel_875["fg"] = "#333333"
        GLabel_875["justify"] = "center"
        GLabel_875["text"] = "label"
        GLabel_875.place(x=300,y=140,width=111,height=30)

        GLabel_227=tk.Label(root)
        ft = tkFont.Font(family='Times',size=12)
        GLabel_227["font"] = ft
        GLabel_227["fg"] = "#333333"
        GLabel_227["justify"] = "center"
        GLabel_227["text"] = "Start Time:"
        GLabel_227.place(x=190,y=140,width=70,height=25)

        global GMessage_101;
        GMessage_101=tk.Message(root)
        ft = tkFont.Font(family='Times',size=12)
        GMessage_101["font"] = ft
        GMessage_101["fg"] = "#333333"
        GMessage_101["justify"] = "center"
        GMessage_101["text"] = "Info"
        GMessage_101.place(x=100,y=250,width=400,height=100)
        
    def process_queue(self):
       try:
           msg = self.queue.get_nowait()
           # Show result of the task if needed
           #self.prog_bar.stop()
       except queue.Empty:
           self.master.after(100, self.process_queue)
           
            
        
    def btn_start_command(self):

        global thread;
        
        grcpClientRecieve.ConnectClient();
        tz = pytz.timezone('EST')
        currentTime = datetime.now(tz) 
        
        print(grcpClientRecieve.IsDataCapturing())
        
        if (grcpClientRecieve.IsDataCapturing() != True):
            
            print("Enabling data capture")
            GLabel_875["text"] = currentTime.strftime('%H:%M:%S')
            
            grcpClientRecieve.threadFlag = 2;
            thread = Thread(target = grcpClientRecieve.StartDataCapture) #Start data capture on seperate thread
            thread.start()
        
        

           
    
    def btn_stop_command(self):
        print("Stop Button Pressed")
        
        GLabel_875["text"] = ""
        GMessage_101["text"] = "Closing File"
        
        try:
           grcpClientRecieve.StopDataCapture()    
        except: 
             print("Closing the file and stopping stream")
        finally: 
            
            thread.join()
            
            #time.sleep(2000)
            
            GMessage_101["text"] = "Seeya!"
            sys.exit()
        

if __name__ == "__main__":
    
    
    startUp = grcpClientRecieve.LoadStartData()
    
    root = tk.Tk()
    app = App(root)
    
    if (startUp == False):
        GMessage_101["text"] = "Files are missing!"
    if (startUp == True):
        GMessage_101["text"] = "Files loaded correctly"  
         
    root.mainloop()

        
