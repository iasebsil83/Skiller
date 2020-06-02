from os import getcwd
from time import sleep

pathFile = open(getcwd() + '/_data/server.path','r')
lastPath = pathFile.read()
pathFile.close()
print("Actual server path is : ")
print(lastPath)
pathFile = open(getcwd() + '/_data/server.path','w')
pathFile.write(input("\nEnter the new server path :\n\n > "))
pathFile.close()
print("Server succesfully set !")
sleep(2)
