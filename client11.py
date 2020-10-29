import xmlrpc.client
import random

import string
from cryptography.fernet import Fernet
proxy = xmlrpc.client.ServerProxy('http://localhost:9000')

proxy1 = xmlrpc.client.ServerProxy('http://localhost:8000')

proxy2=xmlrpc.client.ServerProxy('http://localhost:8080')
g='/home/garvit/dis-RPC'

idclient1='11'

idclient2='12'

idserver1='21'

idserver2='22'


test=1



print("Starting Registration with KDC Server..")
unique_key=proxy.reg('11')
print(unique_key)
nonce1='123456'


gg=input("Enter File server which you want to communicate  ")

if gg not in ('21','22'):
 test=-1
 print("Sorry Wrong File mentioned. Close Connection and Reconnect!")

if gg=='22':
 proxy1=proxy2

print("Initiating the First Step of Communication")
print("Sending Node's Id,File Server Id,Nounce to the KDC....")
c1,c2,c3,c00,c01=proxy.first('11',gg,nonce1)
#print(c1,c2,c3,c00,c01)
key=unique_key
print('Received Encrypted Parameters back From KDC server...')
c1=c1.encode('utf8')
c2=c2.encode('utf8')
c3=c3.encode('utf8')
c00=c00.encode('utf8')
c01=c01.encode('utf8')


suite=Fernet(key.encode('utf8'))
print(type(c1))
decrypt1=suite.decrypt(c1)
decrypt1=decrypt1.decode('utf8')
decrypt2=suite.decrypt(c2)
decrypt2=decrypt2.decode('utf8')
decrypt3=suite.decrypt(c3)
decrypt3=decrypt3.decode('utf8')


sessionkey=decrypt3

nonce3=random.randint(100001,999999)
nonce3=str(nonce3)

suite1=Fernet(sessionkey.encode('utf8'))

crypt1=suite1.encrypt(nonce3.encode('utf8'))

print('Initiating the third step in Communication..')
print('Sending Encrypted Parameters to File Server ',gg)

a1,a2=proxy1.second(crypt1.decode('utf8'),c00.decode('utf8'),c01.decode('utf8'))


print('Parameters Received From File Server..')
a1=a1.encode('utf8')
a2=a2.encode('utf8')

nonce3=int(nonce3)
nonce3=nonce3-1
nonce3=str(nonce3)


print('Initiating Fifth and last Step in our Communication..')
decry1=suite1.decrypt(a1)
decry1=decry1.decode('utf8')

if decry1==nonce3:
 print("Nounce matched!!..")
else:
 test=-1
decry2=suite1.decrypt(a2)
decry2=decry2.decode('utf8')
decry2=int(decry2)
decry2=decry2-1
decry2=str(decry2)

print('sending parameters to File server..')
encry=suite1.encrypt(decry2.encode('utf8'))

check=proxy1.third(encry.decode('utf8'))
if test==1:
 test=check





while(test==1):
 print("Enter your Command")
 a=input('->')
 if a=='-':
  print("Exiting Goodbye")
  break
 elif a=='pwd':
  d=suite1.encrypt(g.encode('utf8'))
  print (proxy1.list_contents(d.decode('utf8')))
 elif a=='ls':
  print(proxy1.show_directory())
 elif a=='cp':
  b=input('Please enter first file path')
  c=input('Please enter second file path')
  b=suite1.encrypt(b.encode('utf8'))
  c=suite1.encrypt(c.encode('utf8'))
  
  print ("Destination path is",proxy1.copy_file(b.decode('utf8'),c.decode('utf8')))
  print("Successfully File Copied")

 elif a=='cat':
  d=input('Please enter path to file')
  d=suite1.encrypt(d.encode('utf8'))
  print(proxy1.disp(d.decode('utf8')))
 
 else:
  print("Command not recognized. Kindly enter again")

if test==-1:
 print("Connection can not be authenticated and established!!")

