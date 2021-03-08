# -*- coding: utf-8 -*-
"""
Phantom Still Camera Relays Controller
This script is a simple Tkinter GUI to active three relays in the Phantom still camera subsea can, this relays are as follows:
Relay 1 - Power to the Canon G5X camera
Relay 2 - Power to the USB data connection to the Canon G5X Camera
Relay 3 - Power to the 5V red lasers in the camera

This script connects to a TCP server running on the Raspberry Pi in the subsea camera, at 192.168.3.45:6000. Upon successful
connection, the buttons send a message that is interpreted by the TCP server to actuate the appropriate relays
"""

import tkinter as tk
import socket


#Instantiate a message box, that will print relevant info in the GUI to inform the user of what is taking place

class StatusBox(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.status_msg = tk.Text(self.parent, height = 25, width = 60)
        self.scroll_bar = tk.Scrollbar(self.parent)
        self.scroll_bar.config(orient="vertical", command=self.status_msg.yview)
        self.status_msg.configure(yscrollcommand=self.scroll_bar.set)
        self.status_label = tk.Label(self.parent, text = "Program Status", font = 'underline').grid(row = 0, column =1, columnspan=2)
        self.status_msg.grid(row=1, column=1, rowspan = 4)
        self.scroll_bar.grid(row=1, column=2, rowspan =4)
        self.PostStatus("")
        
    def PostStatus(self, msg):
        self.status_msg.insert('end', str(msg + "\n"))
        self.status_msg.see('end')


#Instantiate class for the MainWindow of the program, inherit from tk.Frame()

class MainWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Still Camera Relay Controls V1.0")
        #Replace default window close button behaviour with a more graceful approach to closing TCP sockets.
        self.parent.protocol("WM_DELETE_WINDOW", self.SocketCloser)
        
        #The socket module expects to be passed a tuple containing the IP address and port of the host (server)
        #store this tuple in a list, for ease of iterating later in this script
        
        
        self.tcp_devices = [("192.168.0.25", 6000)] #IP address and port of the script running on the Raspberry Pi
        
        #Generate an empty list of 'None' elements, to fill with socket objects from the SocketOpener function.
        
        self.active_sockets = [None] * len(self.tcp_devices)
        
        #Instantiate the StatusBox class, inside the MainWindow
        self.StatusBox = StatusBox(self)        
        
######################INITIALIZE THE NETWORK CONNECTION #################################

        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.server_address = ('localhost', 6000)
        StatusBox.PostStatus(f'starting up program on {self.server_address[0]} at port {self.server_address[1]}')
        self.sock.bind(self.server_address)
      
        #Listen for a connection
        """
        
        #Buttons for all 4 relays
        self.relay1on_button = tk.Button(self, text = "Relay 1 - Camera Power ON", command=lambda : [self.RelayCommand(1,0)])
        self.relay1off_button = tk.Button(self, text = "Relay 1 - Camera Power OFF", command=lambda :  [self.RelayCommand(1,1)])
        self.relay2on_button = tk.Button(self, text = "Relay 2 - Camera USB ON", command=lambda : [self.RelayCommand(2,0)])
        self.relay2off_button = tk.Button(self, text = "Relay 2 - Camera USB OFF", command=lambda : [self.RelayCommand(2,1)])
        self.relay3on_button = tk.Button(self, text = "Relay 3 - Red Lasers ON", command=lambda : [self.RelayCommand(3,0)])
        self.relay3off_button = tk.Button(self, text = "Relay 3 - Red Lasers OFF", command=lambda : [self.RelayCommand(3,1)])        
        self.relay4on_button = tk.Button(self, text = "Relay 4 - SPARE ON", command=lambda : [self.RelayCommand(4,0)])
        self.relay4off_button = tk.Button(self, text = "Relay 4 - SPARE OFF", command=lambda : [self.RelayCommand(4,1)])

        #Place the buttons on the MainWindow

        self.relay1on_button.grid(row=1, column= 0, padx =20)
        self.relay1off_button.grid(row=2, column= 0, padx =20)
        self.relay2on_button.grid(row=3, column= 0, padx =20)
        self.relay2off_button.grid(row=4, column= 0, padx =20)
        self.relay3on_button.grid(row=5, column= 0, padx =20)
        self.relay3off_button.grid(row=6, column= 0, padx =20)
        self.relay4on_button.grid(row=7, column= 0, padx =20)
        self.relay4off_button.grid(row=8, column= 0, padx =20)

        #Try to open the socket at startup 
        
        self.SocketOpener()
        
        #Buttons at bottom of window to open/close the connection to the relays
        
        self.openconnection = tk.Button(self, text = "Connect to Relays", command = self.SocketOpener)
        self.closeconnection = tk.Button(self, text = "Disconnect from Relays and Close Program", command = self.SocketCloser)
        
        self.openconnection.grid(row=5, column =0, columnspan=2, pady = 10)
        self.closeconnection.grid(row=6, column =0, columnspan=2, pady = 10)


########################FUNCTIONS TO SEND DATA TO RASPBERRY PI TCP SERVER ###########################################
        
        #Function to send commands to the actuate relays. These are inefficient text data, but the difference
        #is probably a few bytes, irrelevant over a decent Ethernet connection.
        
    def RelayCommand(self, relay_num, state):
      #  try:            
            if relay_num == 1 and state == 0:
                self.send_command = "ON1"
            if relay_num == 1 and state == 1:
                self.send_command = "OFF1"
            if relay_num == 2 and state == 0:
                self.send_command = "ON2"    
            if relay_num == 2 and state == 1:
                self.send_command = "OFF2"
            if relay_num == 3 and state == 0:
                self.send_command = "ON3"
            if relay_num == 3 and state == 1:
                self.send_command = "OFF3"    
            if relay_num == 4 and state == 0:
                self.send_command = "OFF4"                
            if relay_num == 4 and state == 1:
                self.send_command = "OFF4"                   
            self.active_sockets[0].sendall(bytes(self.send_command + "\r\n", "ascii"))  
            self.StatusBox.PostStatus(f'Sending command {self.send_command}')
      #  except:
           # self.StatusBox.PostStatus("Cannot send relay commands, check network connection")
            

##############################FUNCTIONS TO OPEN AND CLOSE SOCKETS, AND CATCH ERRORS####################################

    #Try to open all device sockets, if they fail, catch the timeout errors and print to screen
    #if they succeed, store the opened sockets in a list. If the socket has allready been opened 
    #(i.e. it's not 'None'), skip it and do not try to open it again.
    
    #NOTE the object 's' is now a socket object, and data can be sent to it through the the ToggleRelay function.
    
    def SocketOpener(self):
            if self.active_sockets[0] is not None:
                message = f'Allready connected at {self.tcp_devices[0]}'
                self.StatusBox.PostStatus(message)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                address = self.tcp_devices[0]
                try:
                    s.connect(address)
                except (TimeoutError, socket.timeout):
                    message = f'Timed out connecting to {self.tcp_devices[0]}'
                    self.StatusBox.PostStatus(message)
                except ConnectionRefusedError:
                    message = f'Connection at {self.tcp_devices[0]} was refused'
                    self.StatusBox.PostStatus(message)
                except OSError:
                    message = 'No network connection available. Check connections'
                    self.StatusBox.PostStatus(message)
                else:
                    self.active_sockets[0] = s
                    message = f'Successfully opened {self.tcp_devices[0]}'
                    self.StatusBox.PostStatus(message)
            self.StatusBox.PostStatus("")       


    #Loop through all the sockets stored in active sockets; if the socket is open, shut it down and close it when 
    #exiting the program.
    def SocketCloser(self):
            try:
                sockinfo = self.active_sockets[0].getpeername()
                message = f'Closing socket at {sockinfo}'
                self.StatusBox.PostStatus(message)
                self.active_sockets[0].shutdown(socket.SHUT_WR)
                self.active_sockets[0].close()
            except OSError:
                message = 'Cannot close socket, has it allready been closed?'
                self.StatusBox.PostStatus(message)
            except AttributeError:
                message = f'No socket open at {self.tcp_devices[0]}'
                self.StatusBox.PostStatus(message)
            self.parent.destroy()


        


#Call the program main loop here

if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root).grid(row = 0, column =0)
    root.mainloop()
