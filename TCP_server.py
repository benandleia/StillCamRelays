import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(21, GPIO.OUT)

#Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.0.25', 6000)
sock.bind(server_address)

sock.listen(1)
print(f'Listening for connections at {server_address[0]}, port {server_address[1]}')

while True:
    connection, client_address = sock.accept()
    print(f'connection from {client_address}')
    try:
            rxbuffer = connection.recv(256).decode("ascii")
            print(rxbuffer)
            message = rxbuffer.split('r\n', 1)#Seperate message from the carriage return and line feed
            if len(message) == 2: #This means that both the data and the carriage return/line feed have been received
                parsed_message = message[0]
                print(parsed_message)
                if parsed_message == "ON1":
                    GPIO.output(21, GPIO.HIGH)
                if parsed_message == "OFF1":
                    GPIO.output(21, GPIO.LOW)          
            #In the even that a full message was not received, keep adding bytes to the bugger until you
            #get a full message
            more_data = connection.recv(256).decode("ascii")
            rxbuffer += more_data           
           
    finally:
        print('Closing')
        connection.close()
        GPIO.cleanup()
            