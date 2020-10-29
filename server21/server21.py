from xmlrpc.server import SimpleXMLRPCServer
import logging
import os
import shutil
import random
import string
from cryptography.fernet import Fernet



print("Working as a Client for File Server Registration...")

import xmlrpc.client
proxy = xmlrpc.client.ServerProxy('http://localhost:9000')

print('Registering file server')
key=proxy.reg('21')

print(key)




# Set up logging
logging.basicConfig(level=logging.DEBUG)

print("Working as a File Server...")
print("Listening on port 8000...")
server = SimpleXMLRPCServer(('localhost', 8000), logRequests=True)



# Expose a function
sessionkey=''
nonce2=random.randint(100001,999999)
nonce2=str(nonce2)



def second(a1,a3,a2):
 print('Encrypted Parameters Received From Client Node')
 print(type(a1),type(a2),type(a3),key)
 print("Initiating Fourth Step in our Communication..")
 suite1=Fernet(key)
 decrypt1=suite1.decrypt(a2.encode('utf8'))
 decrypt1=decrypt1.decode('utf8')
 decrypt2=suite1.decrypt(a3.encode('utf8'))

 suite2=Fernet(decrypt2)
 decrypt3=suite2.decrypt(a1.encode('utf8'))
 decrypt3=decrypt3.decode('utf8')
 decrypt3=int(decrypt3)
 decrypt3=decrypt3-1
 decrypt3=str(decrypt3)
 sessionkey=decrypt2

 file1=open("new.txt","w+")
 file1.write(sessionkey.decode('utf8'))
 file1.close()
 crypt1=suite2.encrypt(decrypt3.encode('utf8'))
 crypt2=suite2.encrypt(nonce2.encode('utf8'))



 file1=open("nounce.txt","w+")
 file1.write(nonce2)
 file1.close()
 
 print('Sending Encrypted Parameters back to Client Node..')
 return crypt1.decode('utf8'),crypt2.decode('utf8')

def third(a1):
 file1 = open("new.txt","r+")
 ey=file1.read()
 sessionkey=ey

 suite=Fernet(sessionkey.encode('utf8'))
 decry=suite.decrypt(a1.encode('utf8'))

 decry=decry.decode('utf8')
 decry=int(decry)
 file2 = open("nounce.txt","r+")
 n=file2.read()
 n=int(n)
 file1.close()
 file2.close()
 if decry+1==n:
  print("Connection Established using mutual authentication protocol!!")
  return 1
 else:
  print("Connection Broken")
  return -1

server.register_function(third)
server.register_function(second)

def list_contents(dir_name):
    dir_name=dir_name.encode('utf8')
    file1 = open("new.txt","r+")
    ey=file1.read()
    suite=Fernet(ey.encode('utf8'))

    dir_name=suite.decrypt(dir_name)
    dir_name=dir_name.decode('utf8')
    logging.debug('list_contents(%s)', dir_name)
    return os.listdir(dir_name)

def show_directory():
    return os.getcwd()	


def copy_file(a1,a2):
    a1=a1.encode('utf8')
    a2=a2.encode('utf8')
    file1 = open("new.txt","r+")
    ey=file1.read()
    suite=Fernet(ey.encode('utf8'))
    a1=suite.decrypt(a1)
    a2=suite.decrypt(a2)
    a1=a1.decode('utf8')
    a2=a2.decode('utf8')
        
    return shutil.copy2(a1, a2) # complete target filename given

def disp(a1):
    a1=a1.encode('utf8')
    file1 = open("new.txt","r+")
    ey=file1.read()
    suite=Fernet(ey.encode('utf8'))
    a1=suite.decrypt(a1)
    a1=a1.decode('utf8')
    with open(a1) as f: # The with keyword automatically closes the file when you are done
        return f.read() 


server.register_function(list_contents)
server.register_function(show_directory)
server.register_function(copy_file)
server.register_function(disp)

try:
    print ('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print ('Exiting')
