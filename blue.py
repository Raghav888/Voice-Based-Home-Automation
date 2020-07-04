import bluetooth
from mqtt import *

server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_socket.bind(("",port))
server_socket.listen(1)

client_socket,address = server_socket.accept()
print ("Accepted connection from ",address)
while 1:

 data = client_socket.recv(1024)
 print ("Received: %s" % data)
 print(type(data))
 data=str(data)
 if (data == "b'00'"):  #if '0' is sent from the Android App, turn OFF the CFL bulb
  print ("AC light OFF")
  mqtt("3992944","00")
 if (data == "b'01'"):  #if '1' is sent from the Android App, turn OFF the CFL bulb
  print ("AC light ON")
  mqtt("3992944","01")
 if (data == "b'10'"):  #if '1' is sent from the Android App, turn OFF the CFL bulb
  print ("AC light OFF")
  mqtt("3992944","10")
 if (data == "b'11'"):  #if '1' is sent from the Android App, turn OFF the CFL bulb
  print ("AC light ON")
  mqtt("3992944","11")
 if (data == "b'000'"):  #if '1' is sent from the Android App, turn OFF the CFL bulb
  print ("AC light ON")
  mqtt("3992944","00")
  mqtt("3992944","10")
 if (data == "b'111'"):  #if '1' is sent from the Android App, turn OFF the CFL bulb
  print ("AC light ON")
  mqtt("3992944","01")
  mqtt("3992944","11")
 if (data == "q"):
  print ("Quit")
  break

client_socket.close()
server_socket.close()
