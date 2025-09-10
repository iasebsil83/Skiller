from socket import *
from threading import Thread
from time import sleep

######################################### SKILLER SERVER[1.2.0] #############################################
# CODE STRUCTURE:                                                                                           #
#    -> Functions                                                                                           #
#    -> Initialisation                                                                                      #
#    -> Main                                                                                                #
#                                                                                                           #
# DONE :                                                                                                    #
#    -> DTN_files communication                             [1.0.0]                                         #
#    -> Server/Client update method (u1,u2,...)             [1.1.0]                                         #
#                                                                                                           #
# TO DO :                                                                                                   #
#    -> Add mobs interactions (focus and fight)                                                             #
#                                                                                                           #
# BUGS :                                                                                                    #
#    -> Problem with some disconnections : people haven't been removed from the good map                    #
#       (S.Map assignement ?)                                                                               #
#                                                                                                           #
#############################################################################################################


################################################## Config #####################################################
serverPath   = "/home/starkiant/Documents/Coding/Python/old/2019/Projects/Skiller2/2.3.0/"
mainPort     = 15557
updaterPort  = 15558
middleString = '_m_'

#data
class Data:
    def __init__(self):
        self.orders = []
        self.alive = True


############################################### Functions ####################################################
def waitForAnother():
    while data.alive:
        temp = server.accept()
        temp1 = serverUpdater.accept()
        print("New client added :",temp[1][0]) #The host don't matter
        clients.append(temp[0])
        clientsUpdaters.append(temp1[0])
        adresses.append(temp[1][0])
        clientsThreads.append(Thread(
            target=receveFromClient,
            args=(len(clients)-1,)
        ))
        clientsThreads[int(len(clientsThreads)-1)].start()

def sizeIn4(text): #DTN buffer limit : 9999 Bytes
    sz = len(text)
    if sz > 9999:
        raise BufferError
    if sz > 999:
        return str(sz)
    if sz > 99:
        return '0' + str(sz)
    if sz > 9:
        return '00' + str(sz)
    return '000' + str(sz)

def receveFromClient(no):
    try:
        while data.alive:
            size = int(clients[no].recv(4).decode())
            temp = clients[no].recv(size).decode()
            data.orders.append(str(no) + temp)
    except:
        print("{0} quit the server.".format(adresses[no]))


############################################# Initialisation #################################################
data = Data()
#game vars (Skiller)
maps = {
    'Lobby(Skyens)':[],
    'Skyens(North)':[],'Skyens(South)':[],
    'Skyens(West)' :[],'Skyens(East)' :[],
    'Elayl':[],
    'Elayl(West)':[],  'Elayl(East)':[],
    'Shanke':[],
    'Shanke(West)':[], 'Shanke(East)':[],
    'Yolms':[],
    'Yolms(North)':[], 'Yolms(South)':[],
    'Jyams':[],
    'Jyams(North)':[], 'Jyams(South)':[],
    'Zondemes':[],     'Yaleas Dungeon':[]
}
#network connections
server = socket(AF_INET,SOCK_STREAM)
serverUpdater = socket(AF_INET,SOCK_STREAM)
server.bind(('',mainPort))
serverUpdater.bind(('',updaterPort))
server.listen(5)
serverUpdater.listen(5)
#clients multithreading
clients = []
clientsUpdaters = []
adresses = []
clientsThreads = []
#waiting for clients
waiting = Thread(target=waitForAnother)
waiting.start()
print("Server ON")


################################################## Main ######################################################
ON = True
while ON:
    if len(data.orders) != 0:
        cmd = data.orders[len(data.orders)-1]
        if cmd[1] == 't': #try (to open file)
            print("{0} try to open {1}".format(adresses[int(cmd[0])],cmd[2:]))
            try:
                f = open(serverPath + cmd[2:],'r')
                f.close()
                temp = '1'
            except:
                temp = '0'
            clients[int(cmd[0])].send(sizeIn4(temp).encode())
            clients[int(cmd[0])].send(temp.encode())
            data.orders.remove(cmd)
        elif cmd[1] == 'r': #read (file)
            f = open(serverPath + cmd[2:],'r')
            temp = f.read()
            f.close()
            clients[int(cmd[0])].send(sizeIn4(temp).encode())
            clients[int(cmd[0])].send(temp.encode())
            print("{0} read {1}".format(adresses[int(cmd[0])],cmd[2:]))
            data.orders.remove(cmd)
        elif cmd[1] == 'w': #write (in file)
            temp = cmd[2:].split(middleString)
            f = open(serverPath + temp[0],'w')
            f.write(temp[1])
            f.close()
            print("{0} wrote at {1}".format(adresses[int(cmd[0])],cmd[2:].split(middleString)[0]))
            data.orders.remove(cmd)
        elif cmd[1] == 'u': #update
            temp = cmd[3:].split(middleString)
            if cmd[2] == '0': #user move (on the map)
                for u in maps[temp[0]]:
                    if u[0] == cmd[0]:
                        userName = u[1]
                        break
                #warning all users on the map
                for u in maps[temp[0]]:
                    temp1 = '0' + userName + middleString\
                                + temp[1] + middleString\
                                + temp[2] + middleString\
                                + temp[3]
                    clientsUpdaters[int(u[0])].send(sizeIn4(temp1).encode())
                    clientsUpdaters[int(u[0])].send(temp1.encode())
                #print("{0} > update 0 : {1} move on {2}".format(
                #    adresses[int(cmd[0])],
                #    userName,temp[0]
                #))
                data.orders.remove(cmd)
            elif cmd[2] == '1': #user change map
                if temp[1] == 'No': #connection to the server => S.Map = 'No'
                    maps[temp[2]].append([])
                    maps[temp[2]][len(maps[temp[2]])-1].append(cmd[0]) #user thread numero (string)
                    maps[temp[2]][len(maps[temp[2]])-1].append(temp[0]) #userName
                else:
                    #warning all users on the old map
                    for u in maps[temp[1]]:
                        if u[0] != cmd[0]:
                            temp1 = '1' + temp[0] + middleString\
                                        + temp[3] + middleString\
                                        + temp[4] + middleString\
                                        + temp[5] + middleString\
                                        + temp[6] + middleString\
                                        + temp[7] + middleString\
                                        + temp[8] + middleString\
                                        + temp[9] + middleString\
                                        + temp[10]
                            #prevent the oldMap user to delete me
                            clientsUpdaters[int(u[0])].send(sizeIn4(temp1).encode())
                            clientsUpdaters[int(u[0])].send(temp1.encode())
                    #change user map
                    maps[temp[1]].remove(
                        [cmd[0], temp[0]]
                    )
                    if temp[2] != 'No': #if I don't disconnect from the server
                        maps[temp[2]].append(
                            [cmd[0], temp[0]]
                        )
                if temp[2] != 'No': #if I don't disconnect from the server
                    #warning all users on the new map
                    for u in maps[temp[2]]:
                        if u[0] != cmd[0]:
                            temp1 = '1' + temp[0] + middleString\
                                        + temp[3] + middleString\
                                        + temp[4] + middleString\
                                        + temp[5] + middleString\
                                        + temp[6] + middleString\
                                        + temp[7] + middleString\
                                        + temp[8] + middleString\
                                        + temp[9] + middleString\
                                        + temp[10]
                            #prevent the newMap user to add me
                            clientsUpdaters[int(u[0])].send(sizeIn4(temp1).encode())
                            clientsUpdaters[int(u[0])].send(temp1.encode())
                print("{0} > update 1 : {1} go from {2} to {3}".format(
                    adresses[int(cmd[0])],
                    temp[0],temp[1],temp[2]
                ))
                data.orders.remove(cmd)
            elif cmd[2] == '2': #user chat
                for u in maps[temp[0]]:
                    if u[0] == cmd[0]:
                        userName = u[1]
                        break
                #all need to know except me
                for u in maps[temp[0]]:
                    if u[1] != userName: #don't need to send it to the concerned user too
                        temp1 = '2' + userName + middleString\
                                    + temp[1]
                        clientsUpdaters[int(u[0])].send(sizeIn4(temp1).encode())
                        clientsUpdaters[int(u[0])].send(temp1.encode())
                print("{0} > update 2 : {1} say \"{2}\" on {3}".format(
                    adresses[int(cmd[0])],
                    userName,temp[1],temp[0]
                ))
                data.orders.remove(cmd)
            elif cmd[2] == '3': #user attack
                for u in maps[temp[0]]:
                    if u[0] == cmd[0]:
                        userName = u[1]
                        break
                #all need to know
                for u in maps[temp[0]]:
                    temp1 = '3' + userName
                    clientsUpdaters[int(u[0])].send(sizeIn4(temp1).encode())
                    clientsUpdaters[int(u[0])].send(temp1.encode())
                print("{0} > update 3 : {1} toggle attack mode on {2}".format(
                    adresses[int(cmd[0])],
                    userName,temp[0]
                ))
                data.orders.remove(cmd)
            elif cmd[2] == '4': #send my infos to somebody
                #get the concerned user numero
                for u in maps[temp[0]]:
                    if u[1] == temp[1]: #only have his userName
                        no = u[0]
                        break
                #get the requesting user userName
                for u in maps[temp[0]]:
                    if u[0] == cmd[0]:
                        userName = u[1]
                        break
                temp1 = '4' + userName + middleString\
                            + temp[2] + middleString\
                            + temp[3] + middleString\
                            + temp[4] + middleString\
                            + temp[5] + middleString\
                            + temp[6] + middleString\
                            + temp[7] + middleString\
                            + temp[8] + middleString\
                            + temp[9]
                clientsUpdaters[int(no)].send(sizeIn4(temp1).encode())
                clientsUpdaters[int(no)].send(temp1.encode())
                print("{0} > update 4 : {1} sent his infos back on {2}".format(
                    adresses[int(cmd[0])],
                    userName,temp[0]
                ))
                data.orders.remove(cmd)
            #elif cmd[2] == '5':
    sleep(0.01)
print("Server OFF")
