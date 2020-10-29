from xmlrpc.server import SimpleXMLRPCServer
import logging
import os
import shutil
import random
import string
from cryptography.fernet import Fernet



idclient1='11'

idclient2='12'

idserver1='21'

idserver2='22'

unique_key1=Fernet.generate_key()
unique_key3=Fernet.generate_key()
unique_key2=Fernet.generate_key()
unique_key4=Fernet.generate_key()

registered=[]



# Set up logging
logging.basicConfig(level=logging.DEBUG)

server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)

print("Starting KDC server..")
print("Listening on port 9000..")




def reg(a1):
 print("Registration Completed through KDC server..")
 registered.append(a1)
 if (a1==idclient1):
  return unique_key1.decode('utf8')
 elif a1==idclient2:
  return unique_key2.decode('utf8')
 elif a1==idserver1:
  return unique_key3.decode('utf8')
 else:
  return unique_key4.decode('utf8')


server.register_function(reg)


def first(a1,a2,a3):
 w=0
 for i in registered:
  if i==a2:
   w=1
   break
 if w==1:
  print ("File Server is already Registered! ")
 else:
  print ("Registration is not complete ...")
  print ("Terminating Connection Request..")
  return 0,0,0,0
 print("Parameters Received From Node ",a1)
 print("Connection Request with File Server ",a2)
 
 if a1==idclient1:
  key=unique_key1
 elif a1==idclient2:
  key=unique_key2
 sessionkey=Fernet.generate_key()
 if a2==idserver1:
  key2=unique_key3
 else:
  key2=unique_key4

 suite1 = Fernet(key)
 suite2=Fernet(key2)

 crypt00=suite2.encrypt(sessionkey)
 crypt01=suite2.encrypt(a1.encode('utf8'))
 crypt1=suite1.encrypt(a3.encode('utf8'))
 crypt2=suite1.encrypt(a2.encode('utf8'))
 crypt3=suite1.encrypt(sessionkey)
 print('Initiating the Second Step in Communication')
 print('Sending Encrypted Parameters back to the client node.... ', a1)
 return crypt1.decode('utf8'),crypt2.decode('utf8'),crypt3.decode('utf8'),crypt00.decode('utf8'),crypt01.decode('utf8')
 
server.register_function(first)





try:
    print ('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print ('Exiting')
