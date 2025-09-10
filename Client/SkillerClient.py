# -*- coding: cp1252 -*-

from glob import glob
from math import log
from random import randint
from tkinter import *
from time import sleep
from threading import Thread
from socket import *
from sys import exit as directExit
import os



############################################# SKILLER[2.4.0] ################################################
# CODE STRUCTURE:                                                                                           #
#    -> DTN                                                                                                 #
#    -> Update : Server                                                                                     #
#    -> Update : Client                                                                                     #
#    -> Events&Graphics                                                                                     #
#    -> Utilities                                                                                           #
#    -> Interfaces                                                                                          #
#    -> Commands                                                                                            #
#    -> Initialisation : Functions                                                                          #
#    -> Initialisation : Vars                                                                               #
#    -> Initialisation : Game                                                                               #
#    -> Start                                                                                               #
#    -> Main                                                                                                #
#                                                                                                           #
# DONE :                                                                                                    #
#    -> All client systems reviewed (maximum optimisation)  [2.1.0]                                         #
#    -> DTN_files system added                              [2.2.0]                                         #
#    -> Server updates system added (Thread + 5 updates)    [2.3.0]                                         #
#    -> DTN_files removed (except user connexion)           [2.4.0]                                         #
#                                                                                                           #
# TO DO :                                                                                                   #
#    -> add the user class in 0/1 updates                                                                   #
#    -> add the mobs in the updateScreen(fps,inGame=True)                                                   #
#    -> BUGS : A chance to crash when a mob die (should be because of file writing overflow)                #
#    -> DO THE BOSS_XP_DROP                                                                                 #
#    -> DO AND ADD SOME MOB INFOS (IN '.MOB' FILES) (MOB_ATK, MOB_DEF,...)                                  #
#                                                                                                           #
#############################################################################################################


################################################ CONFIG #####################################################

#network
serverPath  = "Server/_data/"
serverIp    = '127.0.0.1'
mainPort    = 15557
updaterPort = 15558

#other
middleString = "_m_"
refreshTime = 20 #in s


################################################## DTN ######################################################
class DTN_file:
    def __init__(self,path,tryOpen=True):
        self.path = path
        if tryOpen:
            temp = 't' + path
            server.send(sizeIn4(temp).encode())
            server.send(temp.encode())
            size = int(server.recv(4).decode())
            temp = server.recv(size).decode()
            if temp == '0':
                raise FileNotFoundError

    def read(self):
        temp = 'r' + self.path
        server.send(sizeIn4(temp).encode())
        server.send(temp.encode())
        size = int(server.recv(4).decode())
        return server.recv(size).decode()

    def write(self,content):
        temp = 'w' + self.path + middleString + content
        server.send(sizeIn4(temp).encode())
        server.send(temp.encode())

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



############################################# Update : Server ###############################################
def getServerUpdates(): #receive server updates (only read/write data !!!)
    while S.playing:
        size = int(serverUpdater.recv(4).decode())
        cmd = serverUpdater.recv(size).decode()
        S.serverUpdate = True   #to update the screen, S.serverUpdate=True
        S.serverMessage = ''    #to send a message on the server, S.serverMessage="#msg#"
        if cmd[0] == '0': #users move
            temp = cmd[1:].split(middleString)
            for u in range(len(S.users)):
                if S.users[u][0] == temp[0]: #userName
                    S.users[u][1] = int(temp[1]) #x,y,dir
                    S.users[u][2] = int(temp[2])
                    S.users[u][3] = int(temp[3])
                    break
        elif cmd[0] == '1': #users go in/out the map
            temp = cmd[1:].split(middleString)
            act = False
            for u in S.users:
                if u[0] == temp[0]: #user already exist
                    S.users.remove(u) #=> go out
                    act = True
                    break
            if not act: #else
                S.users.append([]) #=> go in
                for a in range(len(temp)):
                    if a == 0:
                        S.users[len(S.users)-1].append(temp[a])
                    else:
                        S.users[len(S.users)-1].append(int(temp[a]))
                S.users[len(S.users)-1].append(False) #Armed state (default:False)
                #Automatic send of '4' update to the new user going on our map
                for u in range(len(S.users)):
                    if S.users[u][0] == S.userName:
                        n = u
                        break
                S.serverMessage = 'u4{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}{0}{8}{0}{9}{0}{10}'.format(
                    middleString,S.Map,temp[0],
                    S.users[n][1],S.users[n][2],
                    S.users[n][3],S.users[n][4],
                    S.users[n][5],S.users[n][6],
                    S.users[n][7],S.users[n][8]
                )
        elif cmd[0] == '2': #users chat
            temp = cmd[1:].split(middleString)
            S.chatText = "[{0}] : {1}".format(temp[0],temp[1]) #<=>updateChat(,onServer=False)
        elif cmd[0] == '3':
            temp = cmd[1:].split(middleString)
            for u in range(len(S.users)):
                if S.users[u][0] == temp[0]:
                    S.users[u][9] = not S.users[u][9] #Armed state
                    break
        elif cmd[0] == '4':
            temp = cmd[1:].split(middleString)
            S.users.append([])
            for a in range(len(temp)):
                if a == 0:
                    S.users[len(S.users)-1].append(temp[a])
                else:
                    S.users[len(S.users)-1].append(int(temp[a]))
            S.users[len(S.users)-1].append(False) #Armed state (default:False)
        #elif cmd[0] == '5':

def updatePos(x,y,d):
    temp = 'u0' + S.Map\
                + middleString + str(int(x))\
                + middleString + str(int(y))\
                + middleString + str(d)
    server.send(sizeIn4(temp).encode())
    server.send(temp.encode())

def updateMap(newMap,x,y,d):
    temp = []
    for u in S.users:
        if u[0] != S.userName:
            temp.append(u)
    for a in temp: #remove all the users on the old map
        S.users.remove(a)
    if not newMap in ['No','Lobby(Skyens)',
                      'Skyens(West)','Skyens(East)',
                      'Skyens(North)','Skyens(South)',
                      'Elayl(West)','Elayl(East)',
                      'Elayl',
                      'Shanke(West)','Shanke(East)',
                      'Shanke',
                      'Yolms(North)','Yolms(South)',
                      'Yolms',
                      'Jyams(North)','Jyams(South)',
                      'Jyams',
                      'Zondemes','Yaleas Dungeon']:
        raise NameError
    temp1 = []
    for u in range(len(S.users)):
        if S.users[u][0] == S.userName:
            S.users[u][1] = x            #set the new coordinates
            S.users[u][2] = y
            S.users[u][3] = d
            for a in range(len(S.users[u])):
                temp1.append(S.users[u][a])
    if len(temp1) != 0: #if the user is not in his own S.users list (if quit in start menu)
        temp = 'u1' + S.userName\
                    + middleString + S.Map\
                    + middleString + newMap\
                    + middleString + str(temp1[1])\
                    + middleString + str(temp1[2])\
                    + middleString + str(temp1[3])\
                    + middleString + str(temp1[4])\
                    + middleString + str(temp1[5])\
                    + middleString + str(temp1[6])\
                    + middleString + str(temp1[7])\
                    + middleString + str(temp1[8])
        S.Map = newMap
        server.send(sizeIn4(temp).encode())
        server.send(temp.encode())
        initInteracts()

def updateChat(text,onServer=True,update=True):
    S.chatText = text
    if onServer:
        text = 'u2' + S.Map + middleString + text
        server.send(sizeIn4(text).encode())
        server.send(text.encode())
    if update:
        updateScreen(fps)

def updateAttack():
    temp = 'u3' + S.Map
    server.send(sizeIn4(temp).encode())
    server.send(temp.encode())

def updateXP():
    levelLimit = calcLevelLimit()
    if S.levelBar >= levelLimit:
        S.level += 1
        S.levelBar -= levelLimit
        setStats()
        save()
        if S.level != 1:
            updateChat("You grow to level " + str(S.level) + " !",onServer=False)



############################################# Update : Client ###############################################
def timeUpdate():
    while S.playing:
        sleep(refreshTime)
        S.timedUpdate = True

def updateScreen(x,inGame=True):
    display.delete(ALL)
    if inGame:
        d2Dimg(maxl/2,maxh/2,mapSprites[S.Map])
        #interacts
        for i in S.interacts:
            temp = i.split(';')
            temp[0] = int(temp[0])
            temp[1] = int(temp[1])
            if temp[2] == 'npc':
                d2Dimg(temp[0],temp[1],npcSprites[temp[3]])
            elif temp[2] == 'seller':
                d2Dimg(temp[0],temp[1],sellersSprites[temp[3]])
        #users
        for u in S.users:
            d2Dimg(u[1],u[2],defaultSkins['priest' + directions[u[3]-1]]) #body
            try:
                d2Dimg(u[1],u[2],equipSprites[u[4] + directions[u[3]-1]]) #helmet
            except:
                pass
            try:
                d2Dimg(u[1],u[2],equipSprites[u[5] + directions[u[3]-1]]) #armor
            except:
                pass
            try:
                if u[9] == False:
                    d2Dimg(u[1],u[2],equipSprites[u[6] + directions[u[3]-1]]) #arm (not armed)
                else:
                    d2Dimg(u[1]+32,u[2],equipSprites[u[6] + 'Armed' + directions[u[3]-1]])  #arm (armed)
            except:
                pass
        #user interface
        d2Drect(0,0,408,15,'darkRed')
        d2Drect(0,0,int(408*S.life/S.Sstat['lifeMax']),15,'red')
        d2Drect(0,15,408,30,'darkBlue')
        d2Drect(0,15,int(408*S.mana/S.Sstat['manaMax']),30,'blue')
        d2Drect(0,30,maxl,45,'darkGreen')
        levelLimit = calcLevelLimit()
        d2Drect(0,30,int(maxl*S.levelBar/(levelLimit+1)),45,'green')
        if S.debugger: # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DEBUG <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            x,y = getUserCoo()[:2]
            d2Drect(x,y,x,y,'red') #player center
            d2Drect(maxl/2-100,           maxh/outDiv-16,maxl/2+100,           maxh/outDiv   ,'cyan') #UpOutZone
            d2Drect(maxl/2-100,(outDiv-1)*maxh/outDiv   ,maxl/2+100,(outDiv-1)*maxh/outDiv+16,'cyan') #DownOutZone
            d2Drect(           maxl/outDiv-16,maxh/2-100,           maxl/outDiv   ,maxh/2+100,'cyan') #LeftOutZone
            d2Drect((outDiv-1)*maxl/outDiv   ,maxh/2-100,(outDiv-1)*maxl/outDiv+16,maxh/2+100,'cyan') #RightOutZone
        display.create_text(maxl/2,maxh-130,text=S.chatText,fill='yellow',font='yellow') #chat
    for a in range(6):
        display.create_text(maxl/2,maxh-10-20*a,text=S.menuText[5-a],fill='grey20',font='grey20') #menu
    #events reset
    S.mouseState = ''
    S.key = ''
    #display
    display.update()
    sleep(1/x)



############################################ Events&Graphics ################################################
def getKeyP(k):
    S.key = 'P' + k.char

def getKeyR(k):
    S.key = 'R' + k.char

def getReturn(k):
    S.key = 'return'

def getLClick(e):
    S.mouseState = 'L'
    S.mousePos[0] = e.x
    S.mousePos[1] = e.y

def getMClick(e):
    S.mouseState = 'M'
    S.mousePos[0] = e.x
    S.mousePos[1] = e.y

def getRClick(e):
    S.mouseState = 'R'
    S.mousePos[0] = e.x
    S.mousePos[1] = e.y

def d2Drect(x1,y1,x2,y2,color):
    display.create_rectangle(x1,y1,x2,y2,fill=color,outline=color)

def d2Dimg(x,y,img):
    display.create_image(x,y,image=img)

def getInput(inGame=True):
    e = Entry(game)
    e.pack()
    e.bind('<Return>',getReturn)
    while not (S.key == 'return'):
        e.focus_set()
        updateScreen(fps,inGame=inGame)
    text = e.get()
    e.destroy()
    display.focus_set()
    if text == '':
        return ' '
    else:
        return text



################################################# Useful ####################################################
def setEquip():
    for u in range(len(S.users)):
        if S.users[u][0] == S.userName:
            n = u
            break
    #setHelmet
    helmetFile = open('_data/equip/helmets.equip','r')
    content = helmetFile.read().split(';')
    helmetFile.close()
    content = content[S.users[n][4]].split(':')
    S.names[0] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[0][a] = int(content[a])
    #setArmor
    armorFile = open('_data/equip/armors.equip','r')
    content = armorFile.read().split(';')
    armorFile.close()
    content = content[S.users[n][5]].split(':')
    S.names[1] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[1][a] = int(content[a])
    #setArm
    armFile = open('_data/equip/arms.equip','r')
    content = armFile.read().split(';')
    armFile.close()
    content = content[S.users[n][6]].split(':')
    S.names[2] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[2][a] = int(content[a])
    #setAmulet
    amuletFile = open('_data/equip/amulets.equip','r')
    content = amuletFile.read().split(';')
    amuletFile.close()
    content = content[S.users[n][7]].split(':')
    S.names[3] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[3][a] = int(content[a])
    #setRing
    ringFile = open('_data/equip/rings.equip','r')
    content = ringFile.read().split(';')
    ringFile.close()
    content = content[S.users[n][8]].split(':')
    S.names[4] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[4][a] = int(content[a])

def setStats():
    S.Sstat['attack'] = int(
        (S.equip[2][0]
         + S.equip[2][0]*S.equip[0][0]
         + S.equip[2][0]*S.equip[1][0]
         + S.equip[2][0]*S.equip[3][0]
         + S.equip[2][0]*S.equip[4][0]) * (0.55*S.Pstat['strAD'] + 0.5*S.Pstat['magAD'])
    )
    S.Sstat['defence'] = int(
        (S.equip[1][1]
         + S.equip[1][1]*S.equip[2][1]
         + S.equip[1][1]*S.equip[3][1]
         + S.equip[1][1]*S.equip[4][1]
         + S.equip[0][1]
         + S.equip[0][1]*S.equip[2][1]
         + S.equip[0][1]*S.equip[3][1]
         + S.equip[0][1]*S.equip[4][1]) * (0.45*S.Pstat['strAD'] + 0.5*S.Pstat['magAD'])
    )
    S.Sstat['speed'] = int(
        (S.equip[1][2]
         + S.equip[1][2]*S.equip[0][2]
         + S.equip[1][2]*S.equip[2][2]
         + S.equip[1][2]*S.equip[3][2]
         + S.equip[1][2]*S.equip[4][2]) * (0.35*S.Pstat['agiMS'] + 0.85*S.Pstat['dexSC'])
    )
    S.Sstat['miss'] = int(
        (S.equip[0][3]
         + S.equip[1][3]
         + S.equip[2][3]
         + S.equip[3][3]
         + S.equip[4][3]) * (0.65*S.Pstat['agiMS'] + 0.75*S.Pstat['intMC'])
    )
    S.Sstat['critical'] = int(
        (S.equip[0][4]
         + S.equip[1][4]
         + S.equip[2][4]
         + S.equip[3][4]
         + S.equip[4][4]) * (0.15*S.Pstat['dexSC'] + 0.25*S.Pstat['intMC'])
    )
    if S.Sstat['speed'] > 100:
        S.Sstat['speed'] = 100
    if S.Sstat['miss'] > 100:
        S.Sstat['miss'] = 100
    if S.Sstat['critical'] > 100:
        S.Sstat['critical'] = 100

def setEquipFromInv(nbr,unequip=False):
    for u in range(len(S.users)):
        if S.users[u][0] == S.userName:
            n = u
            break
    if unequip:
        if nbr == 0:
            name = helmets[S.users[n][4]]
        elif nbr == 1:
            name = armors[S.users[n][5]]
        elif nbr == 2:
            name = arms[S.users[n][6]]
        elif nbr == 3:
            name = amulets[S.users[n][7]]
        elif nbr == 4:
            name = rings[S.users[n][8]]
        ok = False
        for a in range(24):
            if S.inv[a][0] == 'nothing' or S.inv[a][0] == name:
                ok = True
                row = a
                S.users[n][4+nbr] = 0
                break
        if ok:
            S.inv[row][0] = name
            S.inv[row][1] += 1
    else:
        equipN = -1
        row = 0
        for a in range(len(helmets)):
            if helmets[a] == S.inv[nbr][0]:
                equipN = 0
                row = a
                break
        if equipN == -1:
            for a in range(len(armors)):
                if armors[a] == S.inv[nbr][0]:
                    equipN = 1
                    row = a
                    break
        if equipN == -1:
            for a in range(len(arms)):
                if arms[a] == S.inv[nbr][0]:
                    equipN = 2
                    row = a
                    break
        if equipN == -1:
            for a in range(len(amulets)):
                if amulets[a] == S.inv[nbr][0]:
                    equipN = 3
                    row = a
                    break
        if equipN == -1:
            for a in range(len(rings)):
                if rings[a] == S.inv[nbr][0]:
                    equipN = 4
                    row = a
                    break
        if equipN != -1: #if item found
            if S.users[n][4+equipN] == 0: #if I don't have equip something of this type
                if S.inv[nbr][1] == 1:
                    S.inv[nbr][0] = 'nothing'
                    S.inv[nbr][1] = 0
                else:
                    S.inv[nbr][1] -= 1
                S.users[n][4+equipN] = row
            else:
                if S.inv[nbr][1] == 1:
                    if equipN == 0:
                        S.inv[nbr][0] = helmets[S.users[n][4]]
                    elif equipN == 1:
                        S.inv[nbr][0] = armors[S.users[n][5]]
                    elif equipN == 2:
                        S.inv[nbr][0] = arms[S.users[n][6]]
                    elif equipN == 3:
                        S.inv[nbr][0] = amulets[S.users[n][7]]
                    elif equipN == 4:
                        S.inv[nbr][0] = rings[S.users[n][8]]
                    S.users[n][4+equipN] = row
    setEquip()
    setStats()

def save(tryOpen=True):
    for u in range(len(S.users)):
        if S.users[u][0] == S.userName:
            n = u
            break
    content = '{0};Unable;{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};\
{13};{14};{15};{16};{17};{18};{19};{20};{21};{22};{23};{24};{25};{26};{27};{28};\
{29};{30};{31};{32};{33};{34};{35};{36};{37};{38};{39};{40};{41};{42};{43};{44};\
{45};{46};{47};{48};{49};{50};{51};{52};{53};{54};{55};{56};{57};{58};{59};{60};\
{61};{62};{63};{64};{65};{66};{67};{68};{69};{70};{71};{72};{73};{74};{75};{76};\
{77};{78};{79};{80};{81};{82};{83};{84};{85};{86};{87};{88};{89};{90};{91};{92};\
{93};{94};{95};{96};{97};{98};{99};{100};{101};{102};{103};{104};{105};{106};\
{107};{108};{109};{110};{111};{112};{113};{114};{115};{116};{117};{118};{119};\
{120};{121};{122};{123};{124};{125};{126};{127};{128};{129};{130};{131};{132};\
{133};{134};{135};{136};{137};{138};{139};{140};{141};{142};{143};{144};{145};\
{146};{147};{148};{149}'.format(
                    S.password,S.levelBar,S.level,
                    S.skills['punch'][0],S.skills['punch'][1],
                    S.skills['punch'][2],S.skills['punch'][3],
                    S.skills['punch'][4],S.skills['punch'][5],
                    S.skills['punch'][6],S.skills['punch'][7],
                    S.skills['punch'][8],
                    S.skills['1'][0],S.skills['1'][1],
                    S.skills['1'][2],S.skills['1'][3],
                    S.skills['1'][4],S.skills['1'][5],
                    S.skills['1'][6],S.skills['1'][7],
                    S.skills['1'][8],
                    S.skills['2'][0],S.skills['2'][1],
                    S.skills['2'][2],S.skills['2'][3],
                    S.skills['2'][4],
                    S.skills['2'][5],S.skills['2'][6],
                    S.skills['2'][7],S.skills['2'][8],
                    S.skills['3'][0],S.skills['3'][1],
                    S.skills['3'][2],S.skills['3'][3],
                    S.skills['3'][4],S.skills['3'][5],
                    S.skills['3'][6],S.skills['3'][7],
                    S.skills['3'][8],S.skills['4'][0],
                    S.skills['4'][1],S.skills['4'][2],
                    S.skills['4'][3],S.skills['4'][4],
                    S.skills['4'][5],S.skills['4'][6],
                    S.skills['4'][7],S.skills['4'][8],
                    S.skills['5'][0],S.skills['5'][1],
                    S.skills['5'][2],S.skills['5'][3],
                    S.skills['5'][4],S.skills['5'][5],
                    S.skills['5'][6],S.skills['5'][7],
                    S.skills['5'][8],S.skills['6'][0],
                    S.skills['6'][1],S.skills['6'][2],
                    S.skills['6'][3],S.skills['6'][4],
                    S.skills['6'][5],S.skills['6'][6],
                    S.skills['6'][7],S.skills['6'][8],
                    S.skills['7'][0],S.skills['7'][1],
                    S.skills['7'][2],S.skills['7'][3],
                    S.skills['7'][4],S.skills['7'][5],
                    S.skills['7'][6],S.skills['7'][7],
                    S.skills['7'][8],S.skills['8'][0],
                    S.skills['8'][1],S.skills['8'][2],
                    S.skills['8'][3],S.skills['8'][4],
                    S.skills['8'][5],S.skills['8'][6],
                    S.skills['8'][7],S.skills['8'][8],
                    S.skills['9'][0],S.skills['9'][1],
                    S.skills['9'][2],S.skills['9'][3],
                    S.skills['9'][4],S.skills['9'][5],
                    S.skills['9'][6],S.skills['9'][7],
                    S.skills['9'][8],
                    S.manaTimer,
                    S.Class1,S.ClassLevel1,S.Class2,S.ClassLevel2,
                    S.Class3,S.ClassLevel3,S.Class4,S.ClassLevel4,
                    S.life,S.mana,
                    S.Pstat['strAD'],  S.Pstat['agiMS'],
                    S.Pstat['dexSC'],  S.Pstat['intMC'],
                    S.Pstat['magAD'],  S.Sstat['lifeMax'],
                    S.Sstat['manaMax'],S.Sstat['attack'],
                    S.Sstat['defence'],S.Sstat['speed'],
                    S.Sstat['miss'],   S.Sstat['critical'],
                    S.Map,
                    S.users[n][4],S.users[n][5],S.users[n][6],
                    S.users[n][7],S.users[n][8],
                    S.inv[0], S.inv[1], S.inv[2], S.inv[3], S.inv[4],
                    S.inv[5], S.inv[6], S.inv[7], S.inv[8], S.inv[9],
                    S.inv[10],S.inv[11],S.inv[12],S.inv[13],S.inv[14],
                    S.inv[15],S.inv[16],S.inv[17],S.inv[18],S.inv[19],
                    S.inv[20],S.inv[21],S.inv[22],S.inv[23],
                    S.opped,
                    S.users[n][1],S.users[n][2],S.users[n][3] #x,y,d
    )
    saveFile = open('_data/userTemp.dat','w')
    saveFile.write(content)
    saveFile.close()
    userFile = DTN_file(serverPath + 'users/' + S.userName + '.user',tryOpen=tryOpen)
    userFile.write(content)

def npc(name):
    npcFile = open('_data/interacts/npc/' + name + '.npc','r')
    content = npcFile.read().split(';')
    npcFile.close()
    for a in content:
        for b in range(6):
            S.menuText[b] = ""
        temp = a.split('/')
        for b in range(len(temp)):
            S.menuText[b] = temp[b]
        S.menuText[5] = "[Press " + S.keys['next'] + " to continue]"
        S.key = ''
        stand = True
        while stand:
            if S.key == 'P' + S.keys['next']:
                stand = False
            updateScreen(fps)
    for a in range(6):
        S.menuText[a] = ""
    updateScreen(fps)

def checkExit(d):
    if mapOuts[S.Map][d-1] != '':
        opD = d+2 #oppositeD
        if opD > 4:
            opD -= 4
        for u in range(len(S.users)): #change my position on the map
            if S.users[u][0] == S.userName:
                S.users[u][1] = positions[opD-1][0]
                S.users[u][2] = positions[opD-1][1]
        updateMap(mapOuts[S.Map][d-1],positions[opD-1][0],positions[opD-1][1],d)
        updateChat(S.Map,onServer=False)
    else:
        updatePos(x,y,d)

def tryLogIn():
    try:
        userFile = DTN_file(serverPath + 'users/' + S.userName + '.user')
        content = userFile.read().split(';')
        if content[0] != S.password or content[1] != 'Able':
            return False
        else:
            return True
    except:
        return False

def getUserInfo():
    userFile = DTN_file(serverPath + 'users/' + S.userName + '.user')
    content = userFile.read().split(';')
    S.users.append([
        S.userName,
        int(content[148]),
        int(content[149]),
        int(content[150]),
        int(content[118]),
        int(content[119]),
        int(content[120]),
        int(content[121]),
        int(content[122]),
        False
    ])
    S.levelBar = int(content[2])
    S.level = int(content[3])
    for a in range(9):
        if a == 0:
            S.skills['punch'][a] = content[a+4]
            S.skills['1'][a] = content[a+13]
            S.skills['2'][a] = content[a+22]
            S.skills['3'][a] = content[a+31]
            S.skills['4'][a] = content[a+40]
            S.skills['5'][a] = content[a+49]
            S.skills['6'][a] = content[a+58]
            S.skills['7'][a] = content[a+67]
            S.skills['8'][a] = content[a+76]
            S.skills['9'][a] = content[a+85]
        else:
            S.skills['punch'][a] = int(content[a+4])
            S.skills['1'][a] = int(content[a+13])
            S.skills['2'][a] = int(content[a+22])
            S.skills['3'][a] = int(content[a+31])
            S.skills['4'][a] = int(content[a+40])
            S.skills['5'][a] = int(content[a+49])
            S.skills['6'][a] = int(content[a+58])
            S.skills['7'][a] = int(content[a+67])
            S.skills['8'][a] = int(content[a+76])
            S.skills['9'][a] = int(content[a+85])
    S.manaTimer = int(content[94])
    S.Class1 = content[95]
    S.ClassLevel1 = int(content[96])
    S.Class2 = content[97]
    S.ClassLevel2 = int(content[98])
    S.Class3 = content[99]
    S.ClassLevel3 = int(content[100])
    S.Class4 = content[101]
    S.ClassLevel4 = int(content[102])
    S.life = int(content[103])
    S.mana = int(content[104])
    S.Pstat['strAD'] = int(content[105])
    S.Pstat['agiMS'] = int(content[106])
    S.Pstat['dexSC'] = int(content[107])
    S.Pstat['intMC'] = int(content[108])
    S.Pstat['magAD'] = int(content[109])
    S.Sstat['lifeMax'] = int(content[110])
    S.Sstat['manaMax'] = int(content[111])
    S.Sstat['attack'] = int(content[112])
    S.Sstat['defence'] = int(content[113])
    S.Sstat['speed'] = int(content[114])
    S.Sstat['miss'] = int(content[115])
    S.Sstat['critical'] = int(content[116])
    updateMap(
            content[117] ,int(content[148]),
        int(content[149]),int(content[150])
    )
    for a in range(24):
        temp = content[123+a].split('[')[1].split(']')[0].split(', ')
        S.inv[a][0] = temp[0][1:len(temp[0])-1]
        S.inv[a][1] = int(temp[1])
    S.opped = content[147]
    userFile = DTN_file(serverPath + 'users/' + S.userName + '.user')
    temp = ''
    for a in range(151):
        if a == 1:
            temp += 'Unable;'
        else:
            temp += content[a] + ';'
    userFile.write(temp)

def change(user,row,element):
    userFile = DTN_file(serverPath + 'users/' + user + '.user')
    content = userFile.read().split(';')
    toWrite = ''
    temp = ';'
    for a in range(len(content)):
        if a == len(content)-1:
            temp = ''
        if a != row:
            toWrite += content[a] + temp
        else:
            toWrite += element + temp
    userFile = DTN_file(serverPath + 'users/' + user + '.user')
    userFile.write(toWrite)

def getUserCoo():
    for u in S.users:
        if u[0] == S.userName:
            return u[1:4]

def calcLevelLimit():
    return int(((2*log(S.level+1))*(S.level+1))*2)



############################################### Interfaces ##################################################
def setKeys():
    S.menuText[0] = "Quit      : " + S.keys['quit']
    S.menuText[1] = "Up        : " + S.keys['up']
    S.menuText[2] = "Down      : " + S.keys['down']
    S.menuText[3] = "Left      : " + S.keys['left']
    S.menuText[4] = "Right     : " + S.keys['right']
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    changeKey = False
    stand = True
    while stand:
        if S.key == 'P' + S.keys['next'] and not changeKey:
            stand = False
        if not changeKey:
            if S.key == 'P' + S.keys['quit']\
               or S.key == 'P' + S.keys['up']\
               or S.key == 'P' + S.keys['down']\
               or S.key == 'P' + S.keys['left']\
               or S.key == 'P' + S.keys['right']:
                changeKey = True
        else:
            if S.key == 'P' + S.keys['quit']:
                S.keys['quit'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['up']:
                S.keys['up'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['down']:
                S.keys['down'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['left']:
                S.keys['left'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['right']:
                S.keys['right'] = S.key[1:]
                changeKey = False
        updateScreen(fps)
    S.menuText[0] = "Chat      : " + S.keys['chat']
    S.menuText[1] = "Stats     : " + S.keys['stats']
    S.menuText[2] = "Inventory : " + S.keys['inv']
    S.menuText[3] = "Save      : " + S.keys['save']
    S.menuText[4] = "Keys      : " + S.keys['keys']
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    S.key = ''
    sleep(0.4)
    stand = True
    while stand:
        if S.key == 'P' + S.keys['next'] and not changeKey:
            stand = False
        if not changeKey:
            if S.key == 'P' + S.keys['chat']\
               or S.key == 'P' + S.keys['stats']\
               or S.key == 'P' + S.keys['inv']\
               or S.key == 'P' + S.keys['save']\
               or S.key == 'P' + S.keys['keys']:
                changeKey = True
        else:
            if S.key == 'P' + S.keys['chat']:
                S.keys['chat'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['stats']:
                S.keys['stats'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['inv']:
                S.keys['inv'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['save']:
                S.keys['save'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['keys']:
                S.keys['keys'] = S.key[1:]
                changeKey = False
        updateScreen(fps)
    S.menuText[0] = "Fight     : " + S.keys['spell0']
    S.menuText[1] = "Spell 1   : " + S.keys['spell1']
    S.menuText[2] = "Spell 2   : " + S.keys['spell2']
    S.menuText[3] = "Spell 3   : " + S.keys['spell3']
    S.menuText[4] = "Spell 4   : " + S.keys['spell4']
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    S.key = ''
    sleep(0.4)
    stand = True
    while stand:
        if S.key == 'P' + S.keys['next'] and not changeKey:
            stand = False
        if not changeKey:
            if S.key == 'P' + S.keys['spell0']\
               or S.key == 'P' + S.keys['spell1']\
               or S.key == 'P' + S.keys['spell2']\
               or S.key == 'P' + S.keys['spell3']\
               or S.key == 'P' + S.keys['spell4']:
                changeKey = True
        else:
            if S.key == 'P' + S.keys['spell0']:
                S.keys['spell0'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['spell1']:
                S.keys['spell1'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['spell2']:
                S.keys['spell2'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['spell3']:
                S.keys['spell3'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['spell4']:
                S.keys['spell4'] = S.key[1:]
                changeKey = False
        updateScreen(fps)
    S.menuText[0] = "Spell 5   : " + S.keys['spell5']
    S.menuText[1] = "Spell 6   : " + S.keys['spell6']
    S.menuText[2] = "Spell 7   : " + S.keys['spell7']
    S.menuText[3] = "Spell 8   : " + S.keys['spell8']
    S.menuText[4] = "Spell 9   : " + S.keys['spell9']
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    S.key = ''
    sleep(0.4)
    stand = True
    while stand:
        if S.key == 'P' + S.keys['next'] and not changeKey:
            stand = False
        if not changeKey:
            if S.key == 'P' + S.keys['spell5']\
               or S.key == 'P' + S.keys['spell6']\
               or S.key == 'P' + S.keys['spell7']\
               or S.key == 'P' + S.keys['spell8']\
               or S.key == 'P' + S.keys['spell9']:
                changeKey = True
        else:
            if S.key == 'P' + S.keys['spell5']:
                S.keys['spell5'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['spell6']:
                S.keys['spell6'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['spell7']:
                S.keys['spell7'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['spell8']:
                S.keys['spell8'] = S.key[1:]
                changeKey = False
            elif S.key == 'P' + S.keys['spell9']:
                S.keys['spell9'] = S.key[1:]
                changeKey = False
        updateScreen(fps)
    S.menuText[0] = "          :"
    S.menuText[1] = "          :"
    S.menuText[2] = "          :"
    S.menuText[3] = "          :"
    S.menuText[4] = "next      : " + S.keys['next']
    S.menuText[5] = "press " + S.keys['quit'] + " to go back"
    S.key = ''
    sleep(0.4)
    stand = True
    while stand:
        if S.key == 'P' + S.keys['quit']:
            stand = False
        if not changeKey:
            if S.key == 'P' + S.keys['next']:
                changeKey = True
        else:
            if S.key == 'P' + S.keys['next']:
                S.keys['next'] = S.key[1:]
                changeKey = False
            #elif S.key == 'P' + S.keys["other"]:
        updateScreen(fps)
    sleep(0.4)
    for a in range(6):
        S.menuText[a] = ""
    updateScreen(fps)

def showStats():
    S.menuText[0] = "Vitality   : " + str(S.Sstat['lifeMax'] + S.Sstat['defence'])
    S.menuText[1] = "Dexterity  : " + str(S.Pstat['dexSC'])
    S.menuText[2] = "Inteligence: " + str(S.Pstat['intMC'])
    S.menuText[3] = "Magical    : " + str(S.Pstat['magAD'])
    S.menuText[4] = "Strenght   : " + str(S.Pstat['strAD'])
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    stand = True
    while stand:
        if S.key == 'P' + S.keys['next']:
            stand = False
        updateScreen(fps)
    S.menuText[0] = "Agility    : " + str(S.Pstat['agiMS'])
    S.menuText[1] = ""
    S.menuText[2] = ""
    S.menuText[3] = ""
    S.menuText[4] = ""
    S.menuText[5] = "press " + S.keys['quit'] + " to go back"
    S.key = ''
    sleep(0.4)
    stand = True
    while stand:
        if S.key == 'P' + S.keys['quit']:
            stand = False
        updateScreen(fps)
    sleep(0.4)
    for a in range(6):
        S.menuText[a] = ""

def allStats():
    S.menuText[0] = "Life Max : " + str(S.Sstat['lifeMax'])
    S.menuText[1] = "Mana Max : " + str(S.Sstat['manaMax'])
    S.menuText[2] = "Attack   : " + str(S.Sstat['attack'])
    S.menuText[3] = "Defence  : " + str(S.Sstat['defence'])
    S.menuText[4] = "Speed    : " + str(S.Sstat['speed'])
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    stand = True
    while stand:
        if S.key == 'P' + S.keys['next']:
            stand = False
        updateScreen(fps)
    S.menuText[0] = "Miss     : " + str(S.Sstat['miss'])
    S.menuText[1] = "Critical : " + str(S.Sstat['critical'])
    S.menuText[2] = ""
    S.menuText[3] = ""
    S.menuText[4] = ""
    S.menuText[5] = "press " + S.keys['quit'] + " to go back"
    S.key = ''
    sleep(0.4)
    stand = True
    while stand:
        if S.key == 'P' + S.keys['quit']:
            stand = False
        updateScreen(fps)
    sleep(0.4)
    for a in range(6):
        S.menuText[a] = ""
    updateScreen(fps)

def showInv():
    S.menuText[0] = "{0}[{1}|{2}|{3}|{4}|{5}|{6}]".format(S.names[0],
                                                          S.inv[0][0],S.inv[1][0],
                                                          S.inv[2][0],S.inv[3][0],
                                                          S.inv[4][0],S.inv[5][0])
    S.menuText[1] = "{0}[{1}|{2}|{3}|{4}|{5}|{6}]".format(S.names[1],
                                                          S.inv[6][0],S.inv[7][0],
                                                          S.inv[8][0],S.inv[9][0],
                                                          S.inv[10][0],S.inv[11][0])
    S.menuText[2] = "{0}[{1}|{2}|{3}|{4}|{5}|{6}]".format(S.names[3],
                                                          S.inv[12][0],S.inv[13][0],
                                                          S.inv[14][0],S.inv[15][0],
                                                          S.inv[16][0],S.inv[17][0])
    S.menuText[3] = "{0}[{1}|{2}|{3}|{4}|{5}|{6}]".format(S.names[4],S.
                                                          inv[18][0],S.inv[19][0],
                                                          S.inv[20][0],S.inv[21][0],
                                                          S.inv[22][0],S.inv[23][0])
    S.menuText[4] = ""
    S.menuText[5] = "press " + S.keys['quit'] + " to go back"
    stand = True
    while stand:
        if S.key == 'P' + S.keys['quit']:
            stand = False
        if S.mouseState == 'L':
            if S.mousePos[0] > 493 and S.mousePos[0] < 533: #red boxes
                if S.mousePos[1] > 289 and S.mousePos[1] < 329:
                    setEquipFromInv(0,unequip=True)
                elif S.mousePos[1] > 289+45 and S.mousePos[1] < 329+45:
                    setEquipFromInv(1,unequip=True)
                elif S.mousePos[1] > 289+45*2 and S.mousePos[1] < 329+45*2:
                    setEquipFromInv(2,unequip=True)
                elif S.mousePos[1] > 289+45*3 and S.mousePos[1] < 329+45*3:
                    setEquipFromInv(3)
            elif S.mousePos[0] > 493+45 and S.mousePos[0] < 533+45: #gray boxes
                if S.mousePos[1] > 289 and S.mousePos[1] < 329:
                    setEquipFromInv(0)
                elif S.mousePos[1] > 289+45 and S.mousePos[1] < 329+45:
                    setEquipFromInv(6)
                elif S.mousePos[1] > 289+45*2 and S.mousePos[1] < 329+45*2:
                    setEquipFromInv(12)
                elif S.mousePos[1] > 289+45*3 and S.mousePos[1] < 329+45*3:
                    setEquipFromInv(18)
            elif S.mousePos[0] > 493+45*2 and S.mousePos[0] < 533+45*2:
                if S.mousePos[1] > 289 and S.mousePos[1] < 329:
                    setEquipFromInv(1)
                elif S.mousePos[1] > 289+45 and S.mousePos[1] < 329+45:
                    setEquipFromInv(7)
                elif S.mousePos[1] > 289+45*2 and S.mousePos[1] < 329+45*2:
                    setEquipFromInv(13)
                elif S.mousePos[1] > 289+45*3 and S.mousePos[1] < 329+45*3:
                    setEquipFromInv(19)
            elif S.mousePos[0] > 493+45*3 and S.mousePos[0] < 533+45*3:
                if S.mousePos[1] > 289 and S.mousePos[1] < 329:
                    setEquipFromInv(2)
                elif S.mousePos[1] > 289+45 and S.mousePos[1] < 329+45:
                    setEquipFromInv(8)
                elif S.mousePos[1] > 289+45*2 and S.mousePos[1] < 329+45*2:
                    setEquipFromInv(14)
                elif S.mousePos[1] > 289+45*3 and S.mousePos[1] < 329+45*3:
                    setEquipFromInv(20)
            elif S.mousePos[0] > 493+45*4 and S.mousePos[0] < 533+45*4:
                if S.mousePos[1] > 289 and S.mousePos[1] < 329:
                    setEquipFromInv(3)
                elif S.mousePos[1] > 289+45 and S.mousePos[1] < 329+45:
                    setEquipFromInv(9)
                elif S.mousePos[1] > 289+45*2 and S.mousePos[1] < 329+45*2:
                    setEquipFromInv(15)
                elif S.mousePos[1] > 289+45*3 and S.mousePos[1] < 329+45*3:
                    setEquipFromInv(21)
            elif S.mousePos[0] > 493+45*5 and S.mousePos[0] < 533+45*5:
                if S.mousePos[1] > 289 and S.mousePos[1] < 329:
                    setEquipFromInv(4)
                elif S.mousePos[1] > 289+45 and S.mousePos[1] < 329+45:
                    setEquipFromInv(10)
                elif S.mousePos[1] > 289+45*2 and S.mousePos[1] < 329+45*2:
                    setEquipFromInv(16)
                elif S.mousePos[1] > 289+45*3 and S.mousePos[1] < 329+45*3:
                    setEquipFromInv(22)
            elif S.mousePos[0] > 493+45*6 and S.mousePos[0] < 533+45*6:
                if S.mousePos[1] > 289 and S.mousePos[1] < 329:
                    setEquipFromInv(5)
                elif S.mousePos[1] > 289+45 and S.mousePos[1] < 329+45:
                    setEquipFromInv(11)
                elif S.mousePos[1] > 289+45*2 and S.mousePos[1] < 329+45*2:
                    setEquipFromInv(17)
                elif S.mousePos[1] > 289+45*3 and S.mousePos[1] < 329+45*3:
                    setEquipFromInv(23)
        d2Dimg(648,376,S.invSprite)
        d2Drect(423,359,466,399,'red')
        try:
            d2Dimg(443,379,itemSprites[S.names[2]])
        except:
            pass
        cnt = 0 #for inv rows
        for cy in range(4):
            for cx in range(7):
                if cx == 0: #red boxes
                    d2Drect(493+45*cx,289+45*cy,533+45*cx,329+45*cy,'red')
                else:
                    cnt += 1
                    d2Drect(493+45*cx,289+45*cy,533+45*cx,329+45*cy,'grey60')
                try:
                    if cx == 0: #red boxes
                        if cy >= 2: #put off because of the arm
                            d2Dimg(513+45*cx,309+45*cy,itemSprites[S.names[cy+1]])
                        else:
                            d2Dimg(513+45*cx,309+45*cy,itemSprites[S.names[cy]])
                    else:
                        d2Dimg(513+45*cx,309+45*cy,itemSprites[S.inv[cnt-1][0]])
                except:
                    continue
        updateScreen(fps,inGame=False)
    sleep(0.4)
    for a in range(6):
        S.menuText[a] = ""
    updateScreen(fps)



################################################ Commands ###################################################
def commands(command):
    if command == '/help':
        updateChat("Look at the console window of the game.\n",onServer=False)
        print("\n/setStats <Pstat> <value> : Sets your primary stats.\n\
/setEquip <row> <value> : Sets your equipment(it operates only by ids !).\n\
/xp <amount> : Gives you experience points.\n\
/lvl <amount> : Gives you levels.\n\
/op <pseudo> : Changes a player to administrator.\n\
/deop <pseudo> : Changes a player to simple player.\n\
/heal : Heals you to your maximum.\n\
/tpCoo <x> <y> : Teleports you to (x;y).\n\
/tpMap <map> : Teleports you to a map.\n\
/tpPlayer <pseudo> : Teleports you to a player.\n\
/xy : Prints your coordonates.\n\
/give <row> <itemName> <amount> : Gives to you a quantity of an item stocked at an inventory row.\n\
/spawnMob <mobName> <x> <y> : Spawn a mob at (x;y). Input \'Normal\' to natural set.\n\
/allStats : shows all the stats (secondary stats).\n\
/debug : Toggle debug mode.\n\
/fusion <skill1Number> <skill2Number> : Fusion of two skills (result saved at the first).\n\
/save : Save the game.\n\
/end : Cancel command input\n")
        return '/end'
    elif command.startswith('/setStats'):
        try:
            command = command.split(' ')
            S.Pstat[command[1]] = int(command[2])
            updateChat("Stat changed !",onServer=False)
        except:
            updateChat("Cannot modify Primary stats.",onServer=False)
        return '/end'
    elif command.startswith('/setEquip'):
        try:
            command = command.split(' ')
            for u in range(len(S.users)):
                if S.users[u][0] == S.userName:
                    S.users[u][4+int(command[1])] = int(command[2])
                    break
            setEquip()
            try:
                setStats()
                updateChat("Equipment and stats set !",onServer=False)
            except:
                updateChat("Equipment set but unable to change your Stats.",onServer=False)
        except:
            updateChat("Unable to change your equipment.",onServer=False)
        return '/end'
    elif command.startswith('/xp'):
        try:
            S.levelBar += int(command[4:len(command)])
            updateXP()
            updateChat(command[4:len(command)] + " xp given !",onServer=False)
        except:
            updateChat("Amount " + command[4:len(command)] + " is not usable.",onServer=False)
        return '/end'
    elif command.startswith('/lvl'):
        try:
            S.level += int(command[4:len(command)])
            updateXP()
            updateChat(command[4:len(command)] + " levels given !",onServer=False)
        except:
            updateChat("Amount " + command[4:len(command)] + " is not usable.",onServer=False)
        return '/end'
    elif command.startswith('/op'):
        try:
            temp = command[4:]
            change(temp,147,'True')
            updateChat(command[4:len(command)] + " is now an administrator.",onServer=False)
        except:
            updateChat("No user " + temp + " founded.",onServer=False)
        return '/end'
    elif command.startswith('/deop'):
        try:
            temp = command[4:]
            change(temp,147,'False')
            updateChat(command[4:len(command)] + " is now a simple player.",onServer=False)
        except:
            updateChat("No user " + temp + " founded.",onServer=False)
        return '/end'
    elif command.startswith('/heal'):
        S.life = S.Sstat['lifeMax']
        save()
        updateChat("You're now regenerated !",onServer=False)
        return '/end'
    elif command.startswith('/tpCoo'):
        try:
            temp = command.split(' ')
            for u in range(len(S.users)):
                if S.users[u][0] == S.userName:
                    S.users[u][1] = int(temp[1])
                    S.users[u][2] = int(temp[2])
            updateChat("Teleported yourself at : ({0};{1})".format(temp[1],temp[2]),onServer=False)
        except:
            updateChat("Unknown coordonates : ({0};{1}).".format(temp[1],temp[2]),onServer=False)
        return '/end'
    elif command.startswith('/tpMap'):
        try:
            temp = command.split(' ')[1]
        except:
            pass
        if temp == 'Lobby(Skyens)' or temp == 'Skyens(North)'\
        or temp == 'Skyens(East)' or temp == 'Skyens(South)'\
        or temp == 'Skyens(West)' or temp == 'Elayl'\
        or temp == 'Elayl(West)' or temp == 'Elayl(East)'\
        or temp == 'Jyams' or temp == 'Jyams(North)'\
        or temp == 'Jyams(South)' or temp == 'Yolms'\
        or temp == 'Yolms(North)' or temp == 'Yolms(South)'\
        or temp == 'Shanke' or temp == 'Shanke(West)'\
        or temp == 'Shanke(East)' or temp == 'Zondemes'\
        or temp == 'Yaleas Dungeon':
            temp1 = getUserCoo()
            updateMap(temp,temp1[0],temp1[1],temp1[2])
            initInteracts()
            updateChat('Teleported yourself in ' + temp + '.',onServer=False)
        else:
            updateChat('Map not found : ' + temp + '.',onServer=False)
        return '/end'
    elif command.startswith('/tpPlayer'):
        try:
            temp = command[4:len(command)]
            tpToUser(temp)
            updateChat("Teleported {0} to {1} !".format(S.userName,temp),onServer=False)
        except:
            updateChat("Player {0} not found in {1}.".format(temp,S.Map),onServer=False)
        return '/end'
    elif command == '/xy':
        temp = getUserCoo()
        updateChat('Your position : ({0};{1})'.format(temp[0],temp[1]),onServer=False)
        return '/end'
    elif command == '/map':
        updateChat(S.Map,onServer=False)
        return '/end'
    elif command.startswith('/give'):
        try:
            temp = command.split(' ')
            name = ''
            row = 0
            for a in temp[2].split('_'):
                name += a + ' '
            row = int(temp[1])
            S.inv[row][0] = name[:len(name)-1]
            S.inv[row][1] = int(temp[3])
            updateChat("Given {0} {1}in row {2}.".format(temp[3],name,temp[1]),onServer=False)
        except:
            updateChat("Unable to give {0} {1}at the inventory row {2}.".format(temp[3],name,temp[1]),onServer=False)
        return '/end'
    elif command.startswith('/spawnMob'):
        try:
            temp = command.split(' ')
            spawnMob(choice=temp[1],x=int(temp[2]),y=int(temp[3]))
            updateChat("Succesfully spawned {0} at ({1};{2}).".format(temp[1],temp[2],temp[3]),onServer=False)
        except:
            updateChat("Unable to spawn {0} at ({1};{2}).".format(temp[1],temp[2],temp[3]),onServer=False)
        return '/end'
    elif command == '/allStats':
        allStats()
        return '/end'
    elif command == '/debug':
        S.debugger = not S.debugger
        if S.debugger:
            updateChat("Debug mode ON.",onServer=False)
        else:
            updateChat("Debug mode OFF.",onServer=False)
        return '/end'
    elif command.startswith('/fusion'):
        try:
            temp = command.split(' ')
            fusion(temp[1],temp[2],50,50)
            updateChat("Skill fusion completed !",onServer=False)
        except:
            updateChat("Cannot get fusion with these skills.",onServer=False)
        return '/end'
    elif command == '/save':
        save()
        updateChat("Game saved.",onServer=False)
        return '/end'
    #elif command == '/...':
        #try:
        #   do...
        #except:
        #   do...
        #return '/end'
    elif command != '/end':
        updateChat("Unknown command : " + command + ", please try again.",onServer=False)
        return '/end'
    return command

def tpToUser(name):
    found = False
    him = []
    for u in range(len(S.users)):
        if S.users[u][0] == name:
            found = True
            him.append(S.users[u][1])
            him.append(S.users[u][2])
    if not found:
        raise NameError
    for u in range(len(S.users)):
        if S.users[u][0] == S.userName:
            S.users[u][1] = him[0]
            S.users[u][2] = him[1]

def fusion(sk1Nbr,sk2Nbr,cc1,cc2): #Nbr are Strings and Sk2 will be reset
    if sk1Name == 'punch' or sk2Name == 'punch':
        raise TypeError
    tempSk = []
    S.menuText[0] = "Name of the future skill :"
    updateScreen(fps)
    tempSk.append(getinput())
    S.menuText[0] = ""
    tempSk.append(int(
        (cc1*S.Skills[sk1Nbr][1]+cc2*S.Skills[sk2Nbr][1])/(cc1+cc2)
        - (100*sin(pi/(cc2+1)))/cc1
    ))
    tempSk.append(0)
    tempSk.append(int(
        (cc1*S.Skills[sk1Nbr][3]+cc2*S.Skills[sk2Nbr][3])/(cc1+cc2)
        - (100*sin(pi/(cc2+1)))/cc1
    ))
    tempSk.append(int(
        (cc1*S.Skills[sk1Nbr][4]+cc2*S.Skills[sk2Nbr][4])/(cc1+cc2)
        + (100*sin(pi/(cc2+1)))/cc1
    ))
    tempSk.append(int(
        (cc1*S.Skills[sk1Nbr][5]+cc2*S.Skills[sk2Nbr][5])/(cc1+cc2)
        + (100*sin(pi/(cc2+1)))/cc1
    ))
    tempSk.append(int(
        (cc1*S.Skills[sk1Nbr][6]+cc2*S.Skills[sk2Nbr][6])/(cc1+cc2)
        - (400*sin(pi/(cc2+1)))/(cc1*10)
    ))
    tempSk.append(int(
        (cc1*S.Skills[sk1Nbr][7]+cc2*S.Skills[sk2Nbr][7])/(cc1+cc2)
        - (200*sin(pi/(cc2+1)))/(cc1*10)
    ))
    tempSk.append(int(
        (cc1*S.Skills[sk1Nbr][8]+cc2*S.Skills[sk2Nbr][8])/(cc1+cc2)
        + (200*sin(pi/(cc2+1)))/(cc1*10)
    ))
    S.Skills[str(min(int(sk1Nbr),int(sk2Nbr)))] = tempSk
    S.Skills[str(max(int(sk1Nbr),int(sk2Nbr)))] = ['',0,0,0,0,0,0,0,0]



####################################### Initialisation : Functions ##########################################
def setSprites():
    for d in directions:
        #users (default skins)
        defaultSkins['barbarian' + d] = PhotoImage(file='_data/sprites/skins/barbarian' + d + '.gif')
        defaultSkins['paladin'   + d] = PhotoImage(file='_data/sprites/skins/paladin'   + d + '.gif')
        defaultSkins['priest'    + d] = PhotoImage(file='_data/sprites/skins/priest'    + d + '.gif')
        defaultSkins['rogue'     + d] = PhotoImage(file='_data/sprites/skins/rogue'     + d + '.gif')
        defaultSkins['wizard'    + d] = PhotoImage(file='_data/sprites/skins/wizard'    + d + '.gif')
        #mobs
        mobSkins['Blob'         + d] = PhotoImage(file='_data/sprites/mobs/Plain/Blob'          + d + '.gif')
        mobSkins['Bear'         + d] = PhotoImage(file='_data/sprites/mobs/Plain/Bear'          + d + '.gif')
        mobSkins['RockBeater'   + d] = PhotoImage(file='_data/sprites/mobs/Plain/RockBeater'    + d + '.gif')
        mobSkins['Shuriker'     + d] = PhotoImage(file='_data/sprites/mobs/Ninja/Shuriker'      + d + '.gif')
        mobSkins['Thief'        + d] = PhotoImage(file='_data/sprites/mobs/Ninja/Thief'         + d + '.gif')
        mobSkins['SpiritReaper' + d] = PhotoImage(file='_data/sprites/mobs/Ninja/SpiritReaper'  + d + '.gif')
        mobSkins['Skeleton'     + d] = PhotoImage(file='_data/sprites/mobs/Magical/Skeleton'    + d + '.gif')
        mobSkins['Witch'        + d] = PhotoImage(file='_data/sprites/mobs/Magical/Witch'       + d + '.gif')
        mobSkins['Necromancer'  + d] = PhotoImage(file='_data/sprites/mobs/Magical/Necromancer' + d + '.gif')
        mobSkins['Gobelin'      + d] = PhotoImage(file='_data/sprites/mobs/Chaos/Gobelin'       + d + '.gif')
        mobSkins['Troll'        + d] = PhotoImage(file='_data/sprites/mobs/Chaos/Troll'         + d + '.gif')
        mobSkins['Dwarf'        + d] = PhotoImage(file='_data/sprites/mobs/Barbarian/Dwarf'     + d + '.gif')
        mobSkins['Orc'          + d] = PhotoImage(file='_data/sprites/mobs/Barbarian/Orc'       + d + '.gif')
        mobSkins['Viking'       + d] = PhotoImage(file='_data/sprites/mobs/Barbarian/Viking'    + d + '.gif')
    #maps
    for m in ['Lobby(Skyens)',
              'Skyens(West)', 'Skyens(East)',
              'Skyens(North)','Skyens(South)',
              'Elayl(West)',  'Elayl(East)',
              'Elayl',
              'Shanke(West)', 'Shanke(East)',
              'Shanke',
              'Yolms(North)', 'Yolms(South)',
              'Yolms',
              'Jyams(North)', 'Jyams(South)',
              'Jyams',
              'Zondemes',     'Yaleas Dungeon']:
        mapSprites[m] = PhotoImage(file='_data/sprites/maps/' + m + '.gif')
    #bosses
    mobSkins['Yaleas'] = PhotoImage(file='_data/sprites/mobs/Boss/Yaleas.gif')
    #equipment
    for equip in os.listdir('_data/sprites/equip/'):
        equipSprites[equip[:len(equip)-4]] = PhotoImage(file='_data/sprites/equip/' + equip)
    #notPlayerCharacters (npc)
    for npc in os.listdir('_data/sprites/npc/'):
        npcSprites[npc[:len(npc)-4]] = PhotoImage(file='_data/sprites/npc/' + npc)
    #sellers
    for seller in os.listdir('_data/sprites/sellers/'):
        sellersSprites[seller[:len(seller)-4]] = PhotoImage(file='_data/sprites/sellers/' + seller)
    #items
    for item in os.listdir('_data/sprites/items/'):
        itemSprites[item[:len(item)-4]] = PhotoImage(file='_data/sprites/items/' + item)
    #interfaces
    S.invSprite = PhotoImage(file='_data/sprites/interfaces/inventory.gif')

def initInteracts():
    if S.playing:
        iFile = open('_data/interacts/' + S.Map + '.i','r')
        content = iFile.read().split(';')
        iFile.close()
        S.interacts = []
        for a in range(int(len(content)/4)):
            S.interacts.append(content[4*a] + ';' + content[4*a+1] + ';' + content[4*a+2] + ';' + content[4*a+3])

def quitGame():
    if S.userName != 'not_connected':
        updateChat(S.userName + " left the game",update=False)
        updateChat("[Server]: " + S.userName + " left the game",onServer=False,update=False)
    try:
        userFile = DTN_file(serverPath + 'users/' + S.userName + '.user')
        content = userFile.read().split(';')
        temp = ''
        for a in range(151):
            if a == 1:
                temp += 'Able;'
            else:
                temp += content[a] + ';'
        userFile.write(temp)
        print("Thanks for playing !")
    except:
        print("Thanks for playing !")
    S.playing = False
    updateMap('No',0,0,0)
    sleep(2)
    display.destroy()
    game.destroy()
    directExit()



######################################### Initialisation : Vars #############################################
class Skiller:
    def __init__(self):
        self.playing = True
        self.serverUpdate = False
        self.serverMessage = ''
        self.timedUpdate = False
        self.keys = {
            'up':'z',    'right':'d', 'down':'s',  'left':'q',
            'inv':'b',   'next':'n',  'save':'l',  'keys':'k',
            'stats':'c', 'quit':'e',  'chat':'t',  'spell0':'0',
            'spell1':'1','spell2':'2','spell3':'3','spell4':'4',
            'spell5':'5','spell6':'6','spell7':'7','spell8':'8',
            'spell9':'9'
        }
        self.key = ''
        self.mouseState = ''
        self.mousePos = [0,0]
        self.userName = 'not_connected'
        self.password = ''
        self.users = [] #userName,x,y,d,equip[0,1,2,3,4],attacking
        self.Map = 'No'
        self.equip = [
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
        self.names = ['','','','','']
        self.invSprite = 0
        self.inv = [
            ['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],
            ['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],
            ['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],
            ['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],
            ['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0]
        ]
        self.Class1 = ''
        self.ClassLevel1 = 0
        self.Class2 = ''
        self.ClassLevel2 = 0
        self.Class3 = ''
        self.ClassLevel3 = 0
        self.Class4 = ''
        self.ClassLevel4 = 0
        self.level = 0
        self.levelBar = 0
        self.life = 80
        self.mana = 25
        self.manaTimer = 10
        self.Pstat = {'strAD':25,'agiMS':25,'dexSC':25,'intMC':25,'magAD':25}
        self.Sstat = {
            'lifeMax':80,'manaMax':25,'attack':0,
            'defence':0, 'speed':0,   'miss':0,
            'critical':0
        }
        self.skills = {
            'punch':["punch",0,0,5,0,0,0,0,0],'1':["",0,0,0,0,0,0,0,0],
            '2':["",0,0,0,0,0,0,0,0],         '3':["",0,0,0,0,0,0,0,0],
            '4':["",0,0,0,0,0,0,0,0],         '5':["",0,0,0,0,0,0,0,0],
            '6':["",0,0,0,0,0,0,0,0],         '7':["",0,0,0,0,0,0,0,0],
            '8':["",0,0,0,0,0,0,0,0],         '9':["",0,0,0,0,0,0,0,0]
        }
        self.interacts = []
        self.opped = 'False'
        self.chatText = ""
        self.menuText = ["","","","","",""]
        self.inBossBattle = False
        self.debugger = False

#global data
fps = 25
maxl = 1300
maxh = 600
outDiv = 10
directions = ['Up','Right','Down','Left']
positions = [
    [int(maxl/2),int(maxh/outDiv)],
    [int((outDiv-1)*maxl/outDiv),int(maxh/2)],
    [int(maxl/2),int((outDiv-1)*maxh/outDiv)],
    [int(maxl/outDiv),int(maxh/2)]
]
mapOuts = {                 #Up             #Right           #Down             #Left
    'Lobby(Skyens)' :["Skyens(North)", "Skyens(East)",  "Skyens(South)", "Skyens(West)"  ],
    'Skyens(West)'  :["",              "Lobby(Skyens)", "",              "Jyams"         ],
    'Skyens(East)'  :["",              "Yolms",         "",              "Lobby(Skyens)" ],
    'Skyens(North)' :["Elayl",         "",              "Lobby(Skyens)", ""              ],
    'Skyens(South)' :["Lobby(Skyens)", "",              "Shanke",        ""              ],
    'Elayl(West)'   :["",              "Elayl",         "",              "",             ],
    'Elayl(East)'   :["",              "",              "",              "Elayl",        ],
    'Elayl'         :["Zondemes",      "Elayl(East)",   "Skyens(North)", "Elayl(West)",  ],
    'Shanke(West)'  :["",              "Shanke",        "",              "",             ],
    'Shanke(East)'  :["",              "",              "",              "Shanke",       ],
    'Shanke'        :["Skyens(South)", "Shanke(East)",  "",              "Shanke(West)", ],
    'Yolms(North)'  :["",              "",              "Yolms",         "",             ],
    'Yolms(South)'  :["Yolms",         "",              "",              "",             ],
    'Yolms'         :["Yolms(North)",  "",              "Yolms(South)",  "Skyens(East)", ],
    'Jyams(North)'  :["",              "",              "Jyams",         "",             ],
    'Jyams(South)'  :["Jyams",         "",              "",              "",             ],
    'Jyams'         :["Jyams(North)",  "Skyens(West)",  "Jyams(South)",  "",             ],
    'Zondemes'      :["Yaleas Dungeon","",              "Elayl",         "",             ],
    'Yaleas Dungeon':["",              "",              "Zondemes",      "",             ]
}
mapSprites     = {}
defaultSkins   = {}
mobSkins       = {}
itemSprites    = {}
equipSprites   = {}
npcSprites     = {}
sellersSprites = {}
helmets = ['nothing','simple hat'    ,'witch hat'      ,'gladiator helmet','paladin helmet','barbarian helmet']
armors  = ['nothing','cheap tunic'   ,'ninja tunic'    ,'grass suit'      ,'paladin armor' ,'barbarian plate' ]
arms    = ['nothing','wooden sword'  ,'stick'          ,'aluminium sword' ,'iron sword'    ,'barbarian axe'   ]
amulets = ['nothing','pastas'        ,'aluminium chain','iron chain'  ]
rings   = ['nothing','aluminium ring','iron ring'      ,'platine ring']
S = Skiller()



######################################### Initialisation : Code #############################################
#server
server = socket(AF_INET,SOCK_STREAM)
serverUpdater = socket(AF_INET,SOCK_STREAM)
print("Accessing to the Server \"{0}\"...".format( serverPath[:int(len(serverPath)-1)] ))
server.connect((serverIp,mainPort))
serverUpdater.connect((serverIp,updaterPort))
print("Successfully connected to \"{0}\" !".format( serverPath[:int(len(serverPath)-1)] ))
#timed updates
timeUpdateThread = Thread(target=timeUpdate)
timeUpdateThread.start()
#graphics
game = Tk()
game.title('Skiller 2.4.0')
game.protocol('WM_DELETE_WINDOW',quitGame)
display = Canvas(game,width=maxl-1,height=maxh-1,background='DarkGoldenrod3')
display.bind('<KeyPress>',getKeyP)
display.bind('<KeyRelease>',getKeyR)
display.bind('<Button-1>',getLClick)
display.bind('<Button-2>',getMClick)
display.bind('<Button-3>',getRClick)
display.focus_set()
#start header
temp = [0,0,0]
temp[0] = Label(game,text="                                                                                                                                                                                                          S K I L L E R                                                                                                                                                                                                                ",bg='DarkGoldenrod3')
temp[1] = Label(game,text="                                                                                                                                                                                                    press " + S.keys['next'] + " to continue                                                                                                                                                                                                        ",background='DarkGoldenrod3')
temp[2] = Label(game,text=" by I.A. and JESUS                                                                                                                                                                                                                                                                                                                                                                                                               ",background='DarkGoldenrod3')
temp[0].pack()
temp[1].pack()
temp[2].pack()
display.pack()
display.update()



################################################# Start #####################################################
#start header
stand = True
while stand:
    if S.key == 'P' + S.keys['next']:
        stand = False
    updateScreen(fps,inGame=False)
temp[0].destroy()
temp[1].destroy()
temp[2].destroy()

#start menu
stand = True
state = 0
while stand:
    if state == 0:
        S.menuText[0] = "Log in        " + S.keys['up']
        S.menuText[1] = "Register      " + S.keys['down']
        for a in range(4):
            S.menuText[a+2] = ""
        stand1 = True
        while stand1:
            if S.key == 'P' + S.keys['up']:
                stand1 = False
                state = 1
                for a in range(6):
                    S.menuText[a] = ""
            elif S.key == 'P' + S.keys['down']:
                stand1 = False
                state = 2
                for a in range(6):
                    S.menuText[a] = ""
            updateScreen(fps,inGame=False)
    if state == 1: #log in
        stand1 = True
        while stand1:
            S.menuText[0] = "Please log in"
            S.menuText[1] = " username :"
            for a in range(4):
                S.menuText[a+2] = ""
            display.update()
            S.userName = getInput(inGame=False)
            sleep(0.2)
            S.menuText[0] = ""
            S.menuText[1] = "Password :"
            for a in range(4):
                S.menuText[a+2] = ""
            display.update()
            S.password = getInput(inGame=False)
            if tryLogIn():
                getUserInfo() #sets User Unable btw
                stand1 = False
                stand = False
            else:
                S.menuText[3] = ""
                S.menuText[4] = "retry      " + S.keys['next']
                S.menuText[5] = "main menu  " + S.keys['quit']
                stand2 = 1
                while stand2:
                    if S.key == 'P' + S.keys['next']:
                        stand2 = False
                    elif S.key == 'P' + S.keys['quit']:
                        stand2 = False
                        stand1 = False
                        state = 0
                    updateScreen(fps,inGame=False)
            updateScreen(fps,inGame=False)
    if state == 2: #Register
        stand1 = True
        while stand1:
            S.menuText[0] = "Please enter a username:"
            display.update()
            S.userName = getInput(inGame=False)
            sleep(0.2)
            try:
                temp = DTN_file(serverPath + 'users/' + S.userName + '.user')
            except:
                S.menuText[2] = ""
                S.menuText[0] = "Please enter a password:"
                display.update()
                S.password = getInput(inGame=False)
                S.menuText[0] = "Choose a class :\n"        #classDefinition
                S.menuText[1] = "- Barbarian    1"
                S.menuText[2] = "- Paladin       2"
                S.menuText[3] = "- Priest          3"
                S.menuText[4] = "- Rogue        4"
                S.menuText[5] = "- Wizard        5"
                stand2 = True
                while stand2:
                    if S.key == 'P1':
                        S.Class1 = 'barbarian'
                        S.Pstat['strAD'] += int(0.9*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.9*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.1*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.3*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.7*S.Pstat['magAD'])
                        stand2 = False
                    elif S.key == 'P2':
                        S.Class1 = 'paladin'
                        S.Pstat['strAD'] += int(0.7*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.9*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.9*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.3*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.1*S.Pstat['magAD'])
                        stand2 = False
                    elif S.key == 'P3':
                        S.Class1 = 'priest'
                        S.Pstat['strAD'] += int(0.1*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.3*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.7*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.9*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.9*S.Pstat['magAD'])
                        stand2 = False
                    elif S.key == 'P4':
                        S.Class1 = 'rogue'
                        S.Pstat['strAD'] += int(0.3*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.9*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.7*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.9*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.1*S.Pstat['magAD'])
                        stand2 = False
                    elif S.key == 'P5':
                        S.Class1 = 'wizard'
                        S.Pstat['strAD'] += int(0.3*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.7*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.9*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.1*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.9*S.Pstat['magAD'])
                        stand2 = False
                    updateScreen(fps,inGame=False)
                for a in range(6):
                    S.menuText[a] = ""
                S.menuText[0] = "Class defined : " + S.Class1
                S.menuText[1] = "press " + S.keys['next'] + " to continue"
                stand2 = True
                while stand2:
                    if S.key == 'P' + S.keys['next']:
                        stand2 = False
                        stand1 = False
                        stand = False
                        S.users.append([S.userName,int(maxl/2),int(maxh/2),3,0,0,0,0,0,False]) #user creation
                        updateMap('Lobby(Skyens)',int(maxl/2),int(maxh/2),3)
                        save(tryOpen=False)
                    updateScreen(fps,inGame=False)
            else:
                S.menuText[2] = "username already used."
            updateScreen(fps,inGame=False)
    updateScreen(fps,inGame=False)

#launching game
for a in range(6):
    S.menuText[a] = ""
updateThread = Thread(target=getServerUpdates)
updateThread.start()



################################################# Main ######################################################
#game init
setSprites()
updateChat(S.userName + " join the game")
updateChat("[Server]: " + S.userName + " join the game",onServer=False)
setEquip()
setStats()
attack = [] #attack
atkCnt = 0
atkCntMax = 2 #nbr of timedUpdates
step = 16
S.life = S.Sstat['lifeMax'] #regeneration at every logIn

#temp > default fixed values
MOB_ATK = 5
MOB_DEF = 15
MOB_SPD = 10
MOB_LIFE = 100
MOB_MISS = 20
MOB_CRTK = 5
MOB_XP_DROP = 5
BOSS_XP_DROP = 500

#main
stand = True
while stand:
    #DEATH
    if S.life < 0:
        if S.inBossBattle:
            S.levelBar += int(0.005*BOSS_XP_DROP)
        updatechat(S.userName + " died")
        updatechat("[Server]: " + S.userName + " died",onServer=False)
        updateMap('Lobby(Skyens)',int(maxl/2),int(maxh/2),3)
        S.life = S.Sstat['lifeMax']
        S.inBossBattle = False
        save(tryOpen=False)
    if S.key != '' or S.mouseState != '' or S.serverUpdate or S.timedUpdate: #in this statement, no while => no need to updateScreen()
        if S.timedUpdate:
            #print("timed update !")
            S.timedUpdate = False
            atkCnt -= 1
            if atkCnt == 0:
                updateAttack()
        elif S.key != '': #keyEvent analysis
            #print("Key pressed or released !")
            if S.key == 'P' + S.keys['up']:
                x,y = getUserCoo()[:2]
                y -= step
                limit = maxh/outDiv
                if y < limit:
                    y = limit
                    if x > maxl/2-100 and x < maxl/2+100 and not S.inBossBattle:
                        checkExit(1)
                else:
                    updatePos(x,y,1)
            elif S.key == 'P' + S.keys['down']:
                x,y = getUserCoo()[:2]
                y += step
                limit = (outDiv-1)*maxh/outDiv
                if y > limit:
                    y = limit
                    if x > maxl/2-100 and x < maxl/2+100 and not S.inBossBattle:
                        checkExit(3)
                else:
                    updatePos(x,y,3)
            elif S.key == 'P' + S.keys['left']:
                x,y = getUserCoo()[:2]
                x -= step
                limit = maxl/outDiv
                if x < limit:
                    x = limit
                    if y > maxh/2-100 and y < maxh/2+100 and not S.inBossBattle:
                        checkExit(4)
                else:
                    updatePos(x,y,4)
            elif S.key == 'P' + S.keys['right']:
                x,y = getUserCoo()[:2]
                x += step
                limit = (outDiv-1)*maxl/outDiv
                if x > limit:
                    x = limit
                    if y > maxh/2-100 and y < maxh/2+100 and not S.inBossBattle:
                        checkExit(2)
                else:
                    updatePos(x,y,2)
            elif S.key == 'P' + S.keys['chat']:
                command = ''
                while command != '/end':
                    command = getInput()
                    if command[0] == '/':
                        if S.opped == 'True':
                            command = commands(command)
                        else:
                            S.chatText = "Permition denied."
                            command = '/end'
                    else:
                        updateChat(command)
                        updateChat('[' + S.userName + ']: ' + command,onServer=False)
                        command = '/end'
            elif S.key == 'P' + S.keys['stats']:
                showStats()
            elif S.key == 'P' + S.keys['save']:
                save(tryOpen=False)
                S.chatText = "Party saved !\n"
            elif S.key == 'P' + S.keys['keys']:
                setKeys()
            elif S.key == 'P' + S.keys['inv']:
                showInv()
                setStats()
            elif S.key == 'P' + S.keys['quit']:
                S.menuText[0] = "Quit ?"
                S.menuText[1] = "yes  " + S.keys['up']
                S.menuText[2] = "no   " + S.keys['down']
                for a in range(3):
                    S.menuText[a+3] = ""
                stand1 = True
                stand2 = True
                while stand1:
                    if S.key == 'P' + S.keys['up']:
                        stand1 = False
                    elif S.key == 'P' + S.keys['down']:
                        stand1 = False
                        stand2 = False
                    updateScreen(fps)
                S.menuText[0] = "Save ?"
                S.menuText[1] = "yes  " + S.keys['up']
                S.menuText[2] = "no   " + S.keys['down']
                for a in range(3):
                    S.menuText[a+3] = ""
                S.key = ''
                sleep(0.4)
                while stand2:
                    if S.key == 'P' + S.keys['up']:
                        save()
                        quitGame()
                    elif S.key == 'P' + S.keys['down']:
                        quitGame()
                    updateScreen(fps)
                for a in range(6):
                    S.menuText[a] = ""
            elif atkCnt == 0:
                attack = []
                if S.key == 'P' + S.keys['spell0']:
                    attack = S.skills['punch'][:]
                    atkCnt = atkCntMax
                elif S.key == 'P' + S.keys['spell1']:
                    attack = S.skills['1'][:]
                    atkCnt = atkCntMax
                elif S.key == 'P' + S.keys['spell2']:
                    attack = S.skills['2'][:]
                    atkCnt = atkCntMax
                elif S.key == 'P' + S.keys['spell3']:
                    attack = S.skills['3'][:]
                    atkCnt = atkCntMax
                elif S.key == 'P' + S.keys['spell4']:
                    attack = S.skills['4'][:]
                    atkCnt = atkCntMax
                elif S.key == 'P' + S.keys['spell5']:
                    attack = S.skills['5'][:]
                    atkCnt = atkCntMax
                elif S.key == 'P' + S.keys['spell6']:
                    attack = S.skills['6'][:]
                    atkCnt = atkCntMax
                elif S.key == 'P' + S.keys['spell7']:
                    attack = S.skills['7'][:]
                    atkCnt = atkCntMax
                elif S.key == 'P' + S.keys['spell8']:
                    attack = S.skills['8'][:]
                    atkCnt = atkCntMax
                elif S.key == 'P' + S.keys['spell9']:
                    attack = S.skills['9'][:]
                    atkCnt = atkCntMax
                if attack != []:
                    updateAttack()
        elif S.mouseState != '': #mouseEvent analysis
            #print("Mouse clicked !")
            for i in S.interacts: #interacts
                temp = i.split(';')
                temp[0] = int(temp[0])
                temp[1] = int(temp[1])
                if temp[2] == 'npc':
                    if S.mouseState == 'L'\
                       and S.mousePos[0] >= temp[0]-20 and S.mousePos[0] <= temp[0]+20\
                       and S.mousePos[1] >= temp[1]-20 and S.mousePos[1] <= temp[1]+20:
                        npc(temp[3])
                elif temp[2] == 'seller':
                    if S.mouseState == 'L'\
                       and S.mousePos[0] >= temp[0]-20 and S.mousePos[0] <= temp[0]+20\
                       and S.mousePos[1] >= temp[1]-20 and S.mousePos[1] <= temp[1]+20:
                        print('Seller interaction with',temp[3]) #Code for sellers
        elif S.serverUpdate:
            S.serverUpdate = False
            #print("Server update !")
            if S.serverMessage != '':
                server.send(sizeIn4(S.serverMessage).encode())
                server.send(S.serverMessage.encode())
                S.serverMessage = ''
        updateScreen(fps)
    display.update()
    sleep(1/fps)
