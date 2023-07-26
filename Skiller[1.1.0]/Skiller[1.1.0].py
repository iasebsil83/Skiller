# -*- coding: cp1252 -*-
from glob import glob
from math import log
from random import randint
from time import sleep
from tkinter import *
from sys import exit as directExit

# BUGS : PHANTOM MOB APPEARING IN Jyams(South) and Yolms(North)
# DO THE CLICK IN INVENTORY
# DO THE PLAYER SPEED (atkCnt = 0)
# DO THE BOSS_XP_DROP
# DO AND ADD SOME MOB INFOS (IN '.MOB' FILES) (MOB_ATK, MOB_DEF,...)
"""
******************************************************************************************

    LICENSE :

    Skiller_Python
    Copyright (C) 2017  Sebastien SILVANO
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see <https://www.gnu.org/licenses/>.
"""

#Functions
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

def setSprites():
    directions = ['Up','Right','Down','Left']
    cnt = 1
    for d in directions:
        #player
        try:
            S.skin[str(cnt)] = PhotoImage(file=serverPath + 'users/' + userName + d + '.gif')
        except:
            S.skin[str(cnt)] = PhotoImage(file='_data/sprites/skins/' + S.Class1 + d + '.gif')
        cnt += 1
        #defaultSkins
        defaultSkins['barbarian' + d] = PhotoImage(file='_data/sprites/skins/barbarian' + d + '.gif')
        defaultSkins['paladin' + d] = PhotoImage(file='_data/sprites/skins/paladin' + d + '.gif')
        defaultSkins['priest' + d] = PhotoImage(file='_data/sprites/skins/priest' + d + '.gif')
        defaultSkins['rogue' + d] = PhotoImage(file='_data/sprites/skins/rogue' + d + '.gif')
        defaultSkins['wizard' + d] = PhotoImage(file='_data/sprites/skins/wizard' + d + '.gif')
        #mobs
        mobSkins['Blob' + d] = PhotoImage(file='_data/sprites/mobs/Plain/Blob' + d + '.gif')
        mobSkins['Bear' + d] = PhotoImage(file='_data/sprites/mobs/Plain/Bear' + d + '.gif')
        mobSkins['RockBeater' + d] = PhotoImage(file='_data/sprites/mobs/Plain/RockBeater' + d + '.gif')
        mobSkins['Shuriker' + d] = PhotoImage(file='_data/sprites/mobs/Ninja/Shuriker' + d + '.gif')
        mobSkins['Thief' + d] = PhotoImage(file='_data/sprites/mobs/Ninja/Thief' + d + '.gif')
        mobSkins['SpiritReaper' + d] = PhotoImage(file='_data/sprites/mobs/Ninja/SpiritReaper' + d + '.gif')
        mobSkins['Skeleton' + d] = PhotoImage(file='_data/sprites/mobs/Magical/Skeleton' + d + '.gif')
        mobSkins['Witch' + d] = PhotoImage(file='_data/sprites/mobs/Magical/Witch' + d + '.gif')
        mobSkins['Necromancer' + d] = PhotoImage(file='_data/sprites/mobs/Magical/Necromancer' + d + '.gif')
        mobSkins['Gobelin' + d] = PhotoImage(file='_data/sprites/mobs/Chaos/Gobelin' + d + '.gif')
        mobSkins['Troll' + d] = PhotoImage(file='_data/sprites/mobs/Chaos/Troll' + d + '.gif')
        mobSkins['Dwarf' + d] = PhotoImage(file='_data/sprites/mobs/Barbarian/Dwarf' + d + '.gif')
        mobSkins['Orc' + d] = PhotoImage(file='_data/sprites/mobs/Barbarian/Orc' + d + '.gif')
        mobSkins['Viking' + d] = PhotoImage(file='_data/sprites/mobs/Barbarian/Viking' + d + '.gif')
    mobSkins['Yaleas'] = PhotoImage(file='_data/sprites/mobs/Boss/Yaleas.gif')
    #equipment
    for b in glob('_data/sprites/equip/*'):
        equip = b.split('\\')[1]
        equipSprites[equip[:len(equip)-4]] = PhotoImage(file='_data/sprites/equip/' + equip)
    #notPlayerCharacters
    for b in glob('_data/sprites/npc/*'):
        npc = b.split('\\')[1]
        npcSprites[npc[:len(npc)-4]] = PhotoImage(file='_data/sprites/npc/' + npc)
    #Sellers
    for b in glob('_data/sprites/sellers/*'):
        seller = b.split('\\')[1]
        sellersSprites[seller[:len(seller)-4]] = PhotoImage(file='_data/sprites/sellers/' + seller)
    #items
    for b in glob('_data/sprites/items/*'):
        item = b.split('\\')[1]
        itemSprites[item[:len(item)-4]] = PhotoImage(file='_data/sprites/items/' + item)
    #
    S.invSprite = PhotoImage(file='_data/sprites/interfaces/inventory.gif')
    S.background = PhotoImage(file='_data/sprites/maps/' + S.Map + '.gif')

def d2Drect(x1,y1,x2,y2,color):
    display.create_rectangle(x1,y1,x2,y2,fill=color,outline=color)

def d2Dimg(x,y,img):
    display.create_image(x,y,image=img)

def quitGame():
    try:
        userFile = open(serverPath + 'users/' + userName + '.user','r')
        content = userFile.read().split(';')
        userFile.close()
        userFile = open(serverPath + 'users/' + userName + '.user','w')
        temp = ''
        for a in range(149):
            if a == 1:
                temp += 'Able;'
            else:
                temp += content[a] + ';'
        userFile.write(temp)
        userFile.close()
        cntFile = open(serverPath + S.Map + '/Boss.cnt','r+')
        if cntFile.read().split(';')[1] == userName:
            cntFile.write('0;')
        cntFile.close()
        print("Thanks for playing !")
    except:
        print("Thanks for playing !")
    sleep(2)
    game.destroy()
    directExit()

def setEquip():
    #setHelmet
    helmetFile = open('_data/equip/helmets.equip','r')
    content = helmetFile.read().split(';')
    helmetFile.close()
    content = content[S.equipNo[0]].split(':')
    S.names[0] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[0][a] = int(content[a])
    #setArmor
    armorFile = open('_data/equip/armors.equip','r')
    content = armorFile.read().split(';')
    armorFile.close()
    content = content[S.equipNo[1]].split(':')
    S.names[1] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[1][a] = int(content[a])
    #setArm
    armFile = open('_data/equip/arms.equip','r')
    content = armFile.read().split(';')
    armFile.close()
    content = content[S.equipNo[2]].split(':')
    S.names[2] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[2][a] = int(content[a])
    #setAmulet
    amuletFile = open('_data/equip/amulets.equip','r')
    content = amuletFile.read().split(';')
    amuletFile.close()
    content = content[S.equipNo[3]].split(':')
    S.names[3] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[3][a] = int(content[a])
    #setRing
    ringFile = open('_data/equip/rings.equip','r')
    content = ringFile.read().split(';')
    ringFile.close()
    content = content[S.equipNo[4]].split(':')
    S.names[4] = content[0]
    content = content[1].split(',')
    for a in range(5):
        S.equip[4][a] = int(content[a])

def setStats():
    S.Sstat['attack'] = int((S.equip[2][0] + S.equip[2][0]*S.equip[0][0] + S.equip[2][0]*S.equip[1][0] + S.equip[2][0]*S.equip[3][0] + S.equip[2][0]*S.equip[4][0])*(0.55*S.Pstat['strAD'] + 0.5*S.Pstat['magAD']))
    S.Sstat['defence'] = int((S.equip[1][1] + S.equip[1][1]*S.equip[2][1] + S.equip[1][1]*S.equip[3][1] + S.equip[1][1]*S.equip[4][1] + S.equip[0][1] + S.equip[0][1]*S.equip[2][1] + S.equip[0][1]*S.equip[3][1] + S.equip[0][1]*S.equip[4][1])*(0.45*S.Pstat['strAD'] + 0.5*S.Pstat['magAD']))
    S.Sstat['speed'] = int((S.equip[1][2] + S.equip[1][2]*S.equip[0][2] + S.equip[1][2]*S.equip[2][2] + S.equip[1][2]*S.equip[3][2] + S.equip[1][2]*S.equip[4][2])*(0.35*S.Pstat['agiMS'] + 0.85*S.Pstat['dexSC']))
    S.Sstat['miss'] = int((S.equip[0][3] + S.equip[1][3] + S.equip[2][3] + S.equip[3][3] + S.equip[4][3])*(0.65*S.Pstat['agiMS'] + 0.75*S.Pstat['intMC']))
    S.Sstat['critical'] = int((S.equip[0][4] + S.equip[1][4] + S.equip[2][4] + S.equip[3][4] + S.equip[4][4])*(0.15*S.Pstat['dexSC'] + 0.25*S.Pstat['intMC']))
    if S.Sstat['speed'] > 100:
        S.Sstat['speed'] = 100
    if S.Sstat['miss'] > 100:
        S.Sstat['miss'] = 100
    if S.Sstat['critical'] > 100:
        S.Sstat['critical'] = 100

def showStats():
    S.menuText[0] = "Vitality   : " + str(S.Sstat['lifeMax'] + S.Sstat['defence'])
    S.menuText[1] = "Dexterity  : " + str(S.Pstat['dexSC'])
    S.menuText[2] = "Inteligence: " + str(S.Pstat['intMC'])
    S.menuText[3] = "Magical    : " + str(S.Pstat['magAD'])
    S.menuText[4] = "Strenght   : " + str(S.Pstat['strAD'])
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['next']:
            stand = 0
        clean(fps)
    S.menuText[0] = "Agility    : " + str(S.Pstat['agiMS'])
    S.menuText[1] = ""
    S.menuText[2] = ""
    S.menuText[3] = ""
    S.menuText[4] = ""
    S.menuText[5] = "press " + S.keys['quit'] + " to go back"
    S.key = ''
    sleep(0.4)
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['quit']:
            stand = 0
        clean(fps)
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
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['next']:
            stand = 0
        clean(fps)
    S.menuText[0] = "Miss     : " + str(S.Sstat['miss'])
    S.menuText[1] = "Critical : " + str(S.Sstat['critical'])
    S.menuText[2] = ""
    S.menuText[3] = ""
    S.menuText[4] = ""
    S.menuText[5] = "press " + S.keys['quit'] + " to go back"
    S.key = ''
    sleep(0.4)
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['quit']:
            stand = 0
        clean(fps)
    sleep(0.4)
    for a in range(6):
        S.menuText[a] = ""

def showInv():
    S.menuText[0] = "{0}[{1}|{2}|{3}|{4}|{5}|{6}]".format(S.names[0],S.inv[0][0],S.inv[1][0],S.inv[2][0],S.inv[3][0],S.inv[4][0],S.inv[5][0])
    S.menuText[1] = "{0}[{1}|{2}|{3}|{4}|{5}|{6}]".format(S.names[1],S.inv[6][0],S.inv[7][0],S.inv[8][0],S.inv[9][0],S.inv[10][0],S.inv[11][0])
    S.menuText[2] = "{0}[{1}|{2}|{3}|{4}|{5}|{6}]".format(S.names[3],S.inv[12][0],S.inv[13][0],S.inv[14][0],S.inv[15][0],S.inv[16][0],S.inv[17][0])
    S.menuText[3] = "{0}[{1}|{2}|{3}|{4}|{5}|{6}]".format(S.names[4],S.inv[18][0],S.inv[19][0],S.inv[20][0],S.inv[21][0],S.inv[22][0],S.inv[23][0])
    S.menuText[4] = ""
    S.menuText[5] = "press " + S.keys['quit'] + " to go back"
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['quit']:
            stand = 0
        d2Dimg(maxl/2,maxh/2,S.background)
        d2Dimg(648,376,S.invSprite)
        d2Drect(423,359,466,399,'red')
        try:
            d2Dimg(443,379,itemSprites[S.names[2]])
        except:
            None
        cnt = -1
        for cy in range(4):
            for cx in range(7):
                cnt += 1
                if cx == 0:
                    d2Drect(493+45*cx,289+45*cy,533+45*cx,329+45*cy,'red')
                else:
                    d2Drect(493+45*cx,289+45*cy,533+45*cx,329+45*cy,'grey60')
                try:
                    if cx == 0:
                        d2Dimg(513+45*cx,309+45*cy,itemSprites[S.names[cy]])
                    else:
                        d2Dimg(513+45*cx,309+45*cy,itemSprites[S.inv[cnt][0]])
                except:
                    continue
        clean(fps,active=False)
    sleep(0.4)
    for a in range(6):
        S.menuText[a] = ""

def save():
    content = '{0};Unable;{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14};{15};{16};{17};{18};{19};{20};{21};{22};{23};{24};{25};{26};{27};{28};{29};{30};{31};{32};{33};{34};{35};{36};{37};{38};{39};{40};{41};{42};{43};{44};{45};{46};{47};{48};{49};{50};{51};{52};{53};{54};{55};{56};{57};{58};{59};{60};{61};{62};{63};{64};{65};{66};{67};{68};{69};{70};{71};{72};{73};{74};{75};{76};{77};{78};{79};{80};{81};{82};{83};{84};{85};{86};{87};{88};{89};{90};{91};{92};{93};{94};{95};{96};{97};{98};{99};{100};{101};{102};{103};{104};{105};{106};{107};{108};{109};{110};{111};{112};{113};{114};{115};{116};{117};{118};{119};{120};{121};{122};{123};{124};{125};{126};{127};{128};{129};{130};{131};{132};{133};{134};{135};{136};{137};{138};{139};{140};{141};{142};{143};{144};{145};{146};{147}'.format(password,S.levelBar,S.level,S.skills['punch'][0],S.skills['punch'][1],S.skills['punch'][2],S.skills['punch'][3],S.skills['punch'][4],S.skills['punch'][5],S.skills['punch'][6],S.skills['punch'][7],S.skills['punch'][8],S.skills['1'][0],S.skills['1'][1],S.skills['1'][2],S.skills['1'][3],S.skills['1'][4],S.skills['1'][5],S.skills['1'][6],S.skills['1'][7],S.skills['1'][8],S.skills['2'][0],S.skills['2'][1],S.skills['2'][2],S.skills['2'][3],S.skills['2'][4],S.skills['2'][5],S.skills['2'][6],S.skills['2'][7],S.skills['2'][8],S.skills['3'][0],S.skills['3'][1],S.skills['3'][2],S.skills['3'][3],S.skills['3'][4],S.skills['3'][5],S.skills['3'][6],S.skills['3'][7],S.skills['3'][8],S.skills['4'][0],S.skills['4'][1],S.skills['4'][2],S.skills['4'][3],S.skills['4'][4],S.skills['4'][5],S.skills['4'][6],S.skills['4'][7],S.skills['4'][8],S.skills['5'][0],S.skills['5'][1],S.skills['5'][2],S.skills['5'][3],S.skills['5'][4],S.skills['5'][5],S.skills['5'][6],S.skills['5'][7],S.skills['5'][8],S.skills['6'][0],S.skills['6'][1],S.skills['6'][2],S.skills['6'][3],S.skills['6'][4],S.skills['6'][5],S.skills['6'][6],S.skills['6'][7],S.skills['6'][8],S.skills['7'][0],S.skills['7'][1],S.skills['7'][2],S.skills['7'][3],S.skills['7'][4],S.skills['7'][5],S.skills['7'][6],S.skills['7'][7],S.skills['7'][8],S.skills['8'][0],S.skills['8'][1],S.skills['8'][2],S.skills['8'][3],S.skills['8'][4],S.skills['8'][5],S.skills['8'][6],S.skills['8'][7],S.skills['8'][8],S.skills['9'][0],S.skills['9'][1],S.skills['9'][2],S.skills['9'][3],S.skills['9'][4],S.skills['9'][5],S.skills['9'][6],S.skills['9'][7],S.skills['9'][8],S.manaTimer,S.Class1,S.ClassLevel1,S.Class2,S.ClassLevel2,S.Class3,S.ClassLevel3,S.Class4,S.ClassLevel4,S.life,S.mana,S.Pstat['strAD'],S.Pstat['agiMS'],S.Pstat['dexSC'],S.Pstat['intMC'],S.Pstat['magAD'],S.Sstat['lifeMax'],S.Sstat['manaMax'],S.Sstat['attack'],S.Sstat['defence'],S.Sstat['speed'],S.Sstat['miss'],S.Sstat['critical'],S.Map,S.equipNo[0],S.equipNo[1],S.equipNo[2],S.equipNo[3],S.equipNo[4],S.inv[0],S.inv[1],S.inv[2],S.inv[3],S.inv[4],S.inv[5],S.inv[6],S.inv[7],S.inv[8],S.inv[9],S.inv[10],S.inv[11],S.inv[12],S.inv[13],S.inv[14],S.inv[15],S.inv[16],S.inv[17],S.inv[18],S.inv[19],S.inv[20],S.inv[21],S.inv[22],S.inv[23],S.opped,S.chatAble)
    saveFile = open('_data/userTemp.dat','w')
    saveFile.write(content)
    saveFile.close()
    userFile = open(serverPath + 'users/' + userName + '.user','w')
    userFile.write(content)
    userFile.close()

def setKeys():
    S.menuText[0] = "Quit      : " + S.keys['quit']
    S.menuText[1] = "Up        : " + S.keys['up']
    S.menuText[2] = "Down      : " + S.keys['down']
    S.menuText[3] = "Left      : " + S.keys['left']
    S.menuText[4] = "Right     : " + S.keys['right']
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    changeKey = 0
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['next'] and changeKey == 0:
            stand = 0
        if changeKey == 0:
            if S.key == 'P' + S.keys['quit'] or S.key == 'P' + S.keys['up'] or S.key == 'P' + S.keys['down'] or S.key == 'P' + S.keys['left'] or S.key == 'P' + S.keys['right']:
                changeKey = 1
        else:
            if S.key == 'P' + S.keys['quit']:
                S.keys['quit'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['up']:
                S.keys['up'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['down']:
                S.keys['down'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['left']:
                S.keys['left'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['right']:
                S.keys['right'] = S.key[1:]
                changeKey = 0
        clear(fps)
    S.menuText[0] = "Chat      : " + S.keys['chat']
    S.menuText[1] = "Stats     : " + S.keys['stats']
    S.menuText[2] = "Inventory : " + S.keys['inv']
    S.menuText[3] = "Save      : " + S.keys['save']
    S.menuText[4] = "Keys      : " + S.keys['keys']
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    S.key = ''
    sleep(0.4)
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['next'] and changeKey == 0:
            stand = 0
        if changeKey == 0:
            if S.key == 'P' + S.keys['chat'] or S.key == 'P' + S.keys['stats'] or S.key == 'P' + S.keys['inv'] or S.key == 'P' + S.keys['save'] or S.key == 'P' + S.keys['keys']:
                changeKey = 1
        else:
            if S.key == 'P' + S.keys['chat']:
                S.keys['chat'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['stats']:
                S.keys['stats'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['inv']:
                S.keys['inv'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['save']:
                S.keys['save'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['keys']:
                S.keys['keys'] = S.key[1:]
                changeKey = 0
        clear(fps)
    S.menuText[0] = "Fight     : " + S.keys['spell0']
    S.menuText[1] = "Spell 1   : " + S.keys['spell1']
    S.menuText[2] = "Spell 2   : " + S.keys['spell2']
    S.menuText[3] = "Spell 3   : " + S.keys['spell3']
    S.menuText[4] = "Spell 4   : " + S.keys['spell4']
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    S.key = ''
    sleep(0.4)
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['next'] and changeKey == 0:
            stand = 0
        if changeKey == 0:
            if S.key == 'P' + S.keys['spell0'] or S.key == 'P' + S.keys['spell1'] or S.key == 'P' + S.keys['spell2'] or S.key == 'P' + S.keys['spell3'] or S.key == 'P' + S.keys['spell4']:
                changeKey = 1
        else:
            if S.key == 'P' + S.keys['spell0']:
                S.keys['spell0'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['spell1']:
                S.keys['spell1'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['spell2']:
                S.keys['spell2'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['spell3']:
                S.keys['spell3'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['spell4']:
                S.keys['spell4'] = S.key[1:]
                changeKey = 0
        clear(fps)
    S.menuText[0] = "Spell 5   : " + S.keys['spell5']
    S.menuText[1] = "Spell 6   : " + S.keys['spell6']
    S.menuText[2] = "Spell 7   : " + S.keys['spell7']
    S.menuText[3] = "Spell 8   : " + S.keys['spell8']
    S.menuText[4] = "Spell 9   : " + S.keys['spell9']
    S.menuText[5] = "press " + S.keys['next'] + " to continue"
    S.key = ''
    sleep(0.4)
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['next'] and changeKey == 0:
            stand = 0
        if changeKey == 0:
            if S.key == 'P' + S.keys['spell5'] or S.key == 'P' + S.keys['spell6'] or S.key == 'P' + S.keys['spell7'] or S.key == 'P' + S.keys['spell8'] or S.key == 'P' + S.keys['spell9']:
                changeKey = 1
        else:
            if S.key == 'P' + S.keys['spell5']:
                S.keys['spell5'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['spell6']:
                S.keys['spell6'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['spell7']:
                S.keys['spell7'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['spell8']:
                S.keys['spell8'] = S.key[1:]
                changeKey = 0
            elif S.key == 'P' + S.keys['spell9']:
                S.keys['spell9'] = S.key[1:]
                changeKey = 0
        clear(fps)
    S.menuText[0] = "          :"
    S.menuText[1] = "          :"
    S.menuText[2] = "          :"
    S.menuText[3] = "          :"
    S.menuText[4] = "next      : " + S.keys['next']
    S.menuText[5] = "press " + S.keys['quit'] + " to go back"
    S.key = ''
    sleep(0.4)
    stand = 1
    while stand:
        if S.key == 'P' + S.keys['quit']:
            stand = 0
        if changeKey == 0:
            if S.key == 'P' + S.keys['next']:
                changeKey = 1
        else:
            if S.key == 'P' + S.keys['next']:
                S.keys['next'] = S.key[1:]
                changeKey = 0
            #elif S.key == 'P' + S.keys["other"]:
        clear(fps)
    sleep(0.4)
    for a in range(6):
        S.menuText[a] = ""

def checkUserName():
    try:
        userFile = open(serverPath + 'users/' + userName + '.user','r')
        userFile.close()
    except:
        return False
    return True

def checkUserPassword():
    try:
        userFile = open(serverPath + 'users/' + userName + '.user','r')
        content = userFile.read().split(';')
        userFile.close()
    except:
        return False
    if content[0] == password:
        return True
    else:
        return False

def getUserInfo():
    userFile = open(serverPath + 'users/' + userName + '.user','r')
    #decompil#
    content = userFile.read().split(';')
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
    S.Map = content[117]
    for a in range(5):
        S.equipNo[a] = int(content[118+a])
    for a in range(24):
        temp = content[123+a].split('[')[1].split(']')[0].split(', ')
        S.inv[a][0] = temp[0][1:len(temp[0])-1]
        S.inv[a][1] = int(temp[1])
    S.opped = content[147]
    S.chatAble = False
    userFile.close()
    userFile = open(serverPath + 'users/' + userName + '.user','w')
    temp = ''
    for a in range(149):
        if a == 1:
            temp += 'Unable;'
        else:
            temp += content[a] + ';'
    userFile.write(temp)
    userFile.close()

def change(user,row,element):
    userFile = open(serverPath + 'users/' + user + '.user','r')
    content = userFile.read().split(';')
    userFile.close()
    toWrite = ''
    temp = ';'
    for a in range(len(content)):
        if a == len(content)-1:
            temp = ''
        if a != row:
            toWrite += content[a] + temp
        else:
            toWrite += element + temp
    userFile = open(serverPath + 'users/' + user + '.user','w')
    userFile.write(toWrite)
    userFile.close()

def setInfo():
    userFile = open(serverPath + 'users/' + userName + '.info','w')
    userFile.write('{0};{1};{2};{3};{4};{5};{6};{7}'.format(S.direction,int(S.x),int(S.y),S.Class1,S.names[0],S.names[1],S.names[2],S.armedCnt))
    userFile.close()

def checkForUsers():
    users = []
    All = glob(serverPath + 'users/*.user')
    for a in range(len(All)):
        userFile = open(All[a],'r')
        content = userFile.read().split(';')
        userFile.close()
        if All[a][len(serverPath)+6:len(All[a])-5] != userName:
            try:
                if content[117] == S.Map and content[1] == 'Unable':
                    users.append(All[a][len(serverPath)+6:len(All[a])-5])
            except:
                None
    return users

def getUserAbility(u):
    try:
        userFile = open(serverPath + 'users/' + u + '.user','r')
        content = userFile.read().split(';')
        userFile.close()
        if content[1] == 'Able':
            return True
    except:
        return True
    return False

def getUsersInfo(u):
    stand = True
    while stand:
        try:
            userFile = open(serverPath + 'users/' + u + '.info','r')
            content = userFile.read().split(';')
            userFile.close()
            direction = int(content[0])
            x = int(content[1])
            y = int(content[2])
            Class1 = content[3]
            helmet = content[4]
            armor = content[5]
            arm = content[6]
            armedCnt = int(content[7])
            stand = False
        except:
            return 'No'
    return [direction,x,y,Class1,helmet,armor,arm,armedCnt]

def getUsersFocus(u):
    stand = True
    while stand:
        try:
            userFile = open(serverPath + 'users/' + u + '.info','r')
            content = userFile.read().split(';')
            userFile.close()
            focus = []
            for a in range(mobCap):
                focus.append(int(content[8+a]))
            stand = False
        except:
            return 'No'
    return focus

def checkExit():
    mapFile = open(serverPath + S.Map + '/' + S.Map + '.map','r')
    content = mapFile.read().split(';')
    mapFile.close()
    end = int(content[1])
    a = 0
    while end > 0:
        if S.direction == 1 or S.direction == 3:
            mcx = int(content[2+a])-64
            Mcx = int(content[2+a])+64
            mcy = int(content[3+a])-32
            Mcy = int(content[3+a])+32
        else:
            mcx = int(content[2+a])-32
            Mcx = int(content[2+a])+32
            mcy = int(content[3+a])-64
            Mcy = int(content[3+a])+64
        if S.x >= mcx and S.x <= Mcx and S.y >= mcy and S.y <= Mcy:
            S.Map = content[4+a]
            S.background = PhotoImage(file='_data/sprites/maps/' + S.Map + '.gif')
            S.x = int(content[5+a])
            S.y = int(content[6+a])
            for a in range(mobCap):
                S.focus[a] = 0
            S.chatText = S.Map
            break
        a += 5
        end -= 1
    initInteracts()

def tp(name):
    userFile = open(serverPath + 'users/' + name + '.user','r')
    content1 = userFile.read().split(';')
    userFile.close()
    userFile = open(serverPath + 'users/' + name + '.pos','r')
    content2 = userFile.read().split(';')
    userFile.close()
    S.Map = content1[119]
    initInteracts()
    S.x = int(content2[0])
    S.y = int(content2[1])

def checkChatAble():
    userFile = open(serverPath + 'users/' + userName + '.user','r')
    content = userFile.read().split(';')
    userFile.close()
    if content[148] == 'True':
        return True
    else:
        return False

def spawnMob(choice='Normal',x='Normal',y='Normal'):
    mobFile = open(serverPath + S.Map + '/mobs.dat','r')
    content = mobFile.read().split(';')
    mobFile.close()
    mapFile = open(serverPath + S.Map + '/' + S.Map + '.map','r')
    mobType = mapFile.read().split(';')[0]
    mapFile.close()
    if mobType != 'Unable':
        try:
            toWrite = str(int(content[(int(len(content)/13)-1)*13])+1) + ';' #Get the current mobNbr +1 (=The new mobNbr)
        except:
            toWrite = '0;'
        if choice == 'Normal':
            temp = randint(1,8)
            if mobType == 'Plain':
                if temp == 1:
                    toWrite += 'RockBeater;'
                elif temp >= 3 and temp < 6:
                    toWrite += 'Blob;'
                else:
                    toWrite += 'Bear;'
            elif mobType == 'Barbarian':
                if temp == 1:
                    toWrite += 'Orc;'
                elif temp >= 3 and temp < 6:
                    toWrite += 'Dwarf;'
                else:
                    toWrite += 'Viking;'
            elif mobType == 'Ninja':
                if temp == 1:
                    toWrite += 'SpiritReaper;'
                elif temp >= 3 and temp < 6:
                    toWrite += 'Shuriker;'
                else:
                    toWrite += 'Thief;'
            elif mobType == 'Magical':
                if temp == 1:
                    toWrite += 'Necromancer;'
                elif temp >= 3 and temp < 6:
                    toWrite += 'Skeleton;'
                else:
                    toWrite += 'Witch;'
            elif mobType == 'Chaos':
                if temp <= 4:
                    toWrite += 'Troll;'
                else:
                    toWrite += 'Gobelin;'
        else:
            toWrite += choice + ';'
        if x == 'Normal':
            x = randint(16,624)
        if y == 'Normal':
            y = randint(64,384)
        toWrite += '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}'.format(randint(1,4),x,y,MOB_LIFE,MOB_ATK,MOB_DEF,S.level+randint(-2,2),MOB_LIFE,MOB_MISS,MOB_SPD,MOB_CRTK) #replace by getting mob infos from '_data/mobs/#mobName#.mob'
        temp = ''
        for a in range(len(content)):
            if len(content) != 1:
                temp += content[a] + ';'
        toWrite = temp + toWrite
        mobFile = open(serverPath + S.Map + '/mobs.dat','w')
        mobFile.write(toWrite)
        mobFile.close()

def listMobs():
    mobFile = open(serverPath + S.Map + '/mobs.dat','r')
    content = mobFile.read().split(';')
    mobFile.close()
    temp = []
    try:
        for a in range(int(len(content)/13)):
            temp.append(content[13*a+1])
        return temp
    except:
        return []

def getMobInfo(nbr):
    mobFile = open(serverPath + S.Map + '/mobs.dat','r')
    content = mobFile.read().split(';')
    mobFile.close()
    temp = content[13*nbr:13*(nbr+1)]
    for a in range(11):
        temp[a+2] = int(temp[a+2])
    return temp

def changeMob(mobNo,direction,x,y,mobLife):
    mobFile = open(serverPath + S.Map + '/mobs.dat','r')
    content = mobFile.read().split(';')
    mobFile.close()
    toWrite = ''
    for a in range(int(len(content)/13)):
        if content[13*a] == str(mobNo):
            toWrite += '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12}'.format(content[13*a],content[13*a+1],direction,x,y,mobLife,content[13*a+6],content[13*a+7],content[13*a+8],content[13*a+9],content[13*a+10],content[13*a+11],content[13*a+12])
        else:
            toWrite += '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12}'.format(content[13*a],content[13*a+1],content[13*a+2],content[13*a+3],content[13*a+4],content[13*a+5],content[13*a+6],content[13*a+7],content[13*a+8],content[13*a+9],content[13*a+10],content[13*a+11],content[13*a+12])
        if a != int(len(content)/13)-1:
            toWrite += ';'
    mobFile = open(serverPath + S.Map + '/mobs.dat','w')
    mobFile.write(toWrite)
    mobFile.close()

def delMob(mobNo):
    mobFile = open(serverPath + S.Map + '/mobs.dat','r')
    content = mobFile.read().split(';')
    mobFile.close()
    toWrite = ''
    try:
        for a in range(int(len(content)/13)):
            nbr = int(content[13*a])
            if nbr != mobNo:
                if nbr > mobNo:
                    nbr -= 1
                toWrite += '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12}'.format(nbr,content[13*a+1],content[13*a+2],content[13*a+3],content[13*a+4],content[13*a+5],content[13*a+6],content[13*a+7],content[13*a+8],content[13*a+9],content[13*a+10],content[13*a+11],content[13*a+12])
            if a != int(len(content)/13)-1 and a != mobNo:
                toWrite += ';'
        mobFile = open(serverPath + S.Map + '/mobs.dat','w')
        mobFile.write(toWrite)
        mobFile.close()
    except:
        None

def drawMobSprite(mobNo,mobX,mobY):
    mobFile = open(serverPath + S.Map + '/mobs.dat','r')
    content = mobFile.read().split(';')
    mobFile.close()
    for a in range(int(len(content)/13)):
        if content[13*a] == str(mobNo):
            name = content[13*a+1]
            direction = int(content[13*a+2])
    directions = ['Up','Right','Down','Left']
    try:
        d2Dimg(mobX,mobY,mobSkins[name + directions[direction-1]])
    except:
        None

def initInteracts():
    iFile = open('_data/interacts/' + S.Map + '.i','r')
    content = iFile.read().split(';')
    iFile.close()
    S.interacts = []
    for a in range(int(len(content)/4)):
       S.interacts.append(content[4*a] + ';' + content[4*a+1] + ';' + content[4*a+2] + ';' + content[4*a+3])

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
            clean(fps)
    for a in range(6):
        S.menuText[a] = ""

def mobs():
    mobT = randint(0,600)
    mobList = listMobs()
    if mobT == 300 and len(mobList) < mobCap:
        spawnMob()
    mobList = listMobs()
    dieds = []
    for m in range(len(mobList)):
        temp = getMobInfo(m)
        diffX = max(S.x,temp[3]) - min(S.x,temp[3])
        diffY = max(S.y,temp[4]) - min(S.y,temp[4])
        if temp[5] <= 0: #Look for a died mob
            dieds.append(m)
        else:
            if S.focus[m] != 0:
                if diffX > 50: #focus move
                    if S.x > temp[3]:
                        temp[0] = 2
                        changeMob(m,1,temp[3]+1,temp[4],temp[5])
                    else:
                        temp[2] = 1
                        changeMob(m,0,temp[3]-1,temp[4],temp[5])
                elif diffY > 40:
                    if S.y > temp[4]:
                        temp[2] = 4
                        changeMob(m,3,temp[3],temp[4]+1,temp[5])
                    else:
                        temp[2] = 3
                        changeMob(m,2,temp[3],temp[4]-1,temp[5])
                if S.focus[m] == 1:
                    S.focus[m] = int(1000-10*temp[6]) #Mob speed
                    if diffX < 80 and diffY < 80:
                        if randint(1,100) > S.Sstat['miss']+1:
                            if randint(0,100) > temp[12]:
                                damages = abs(int((temp[6]+randint(-15,15))-S.Sstat['defence']))
                                S.life -= damages
                                save()
                                S.chatText = "{0} attacks. -{1} hp.".format(temp[1],damages)
                            else:
                                damages = abs(int((temp[6]+randint(-15,15))*1.5-S.Sstat['defence']))
                                S.life -= damages
                                save()
                                S.chatText = "{0} attacks. -{1} hp, CRITICAL !".format(temp[1],damages)
                        else:
                            S.chatText = temp[1] + " miss."
                S.focus[m] -= 1
            else:
                move = randint(1,400) #free move
                if move == 399 and temp[3] < maxl-64:
                    temp[2] = 2
                    changeMob(m,1,temp[3]+2,temp[4],temp[5])
                elif move == 2 and temp[3] > 32:
                    temp[2] = 1
                    changeMob(m,0,temp[3]-2,temp[4],temp[5])
                elif move == 398 and temp[4] < maxh-66:
                    temp[2] = 4
                    changeMob(m,3,temp[3],temp[4]+2,temp[5])
                elif move == 3 and temp[4] > 62:
                    temp[2] = 3
                    changeMob(m,2,temp[3],temp[4]-2,temp[5])
            focusOk = True
            users = checkForUsers()
            for u in users:
                uFocus = 'No'
                while uFocus == 'No':
                    uFocus = getUsersFocus(u)
                    if type(uFocus) == list and uFocus[m] != 0:
                        focusOk = False
            if diffX < 80 and diffY < 80 and S.focus[m] == 0 and focusOk:
                S.focus[m] = 110
                S.chatText = "Focused by a {0} ! {1} hp, level {2}.".format(temp[1],temp[5],temp[8])
            inLeftZone  = S.x+32 <= temp[3]+32 and S.x+32 >= temp[3]+32-48
            inRightZone = S.x+32 >= temp[3]+32 and S.x+32 <= temp[3]+32+48
            inUpZone    = S.y+32 <= temp[4]+32 and S.y+32 >= temp[4]+32-48
            inDownZone  = S.y+32 >= temp[4]+32 and S.y+32 <= temp[4]+32+48
            inLargeX = inLeftZone or inRightZone
            inLargeY = inUpZone or inDownZone
            if S.debugger:
                if inLargeY:
                    if inLeftZone and S.direction == 2:
                        print("inLeftZone")
                    if inRightZone and S.direction == 4:
                        print("inRightZone")
                if inLargeX:
                    if inUpZone and S.direction == 3:
                        print("inUpZone")
                    if inDownZone and S.direction == 1:
                        print("inDownZone")
                if S.direction == 1:
                    d2Drect(temp[3]+32-48,temp[4]+32,temp[3]+32+48,temp[4]+32+48,'magenta')
                elif S.direction == 2:
                    d2Drect(temp[3]+32-48,temp[4]+32-48,temp[3]+32,temp[4]+32+48,'magenta')
                elif S.direction == 3:
                    d2Drect(temp[3]+32-48,temp[4]+32-48,temp[3]+32+48,temp[4]+32,'magenta')
                else:
                    d2Drect(temp[3]+32,temp[4]+32-48,temp[3]+32+48,temp[4]+32+48,'magenta')
            if attack != [] and ( (S.direction == 1 and inDownZone and inLargeX) or (S.direction == 3 and inUpZone and inLargeX) or (S.direction == 2 and inLeftZone and inLargeY) or (S.direction == 4 and inRightZone and inLargeY) ) and focusOk:
                if S.focus[m] == 0:
                    S.focus[m] = 110
                    S.chatText = "Focused by a {0} ! {1} hp, level {2}.".format(temp[1],temp[5],temp[8])
                if randint(0,100) > temp[10]:
                    if randint(0,100) > S.Sstat['critical']/10:
                        damages = abs(int((S.Sstat['attack']+randint(-15,15))*attack[3]-temp[7]))
                        changeMob(m,temp[2],temp[3],temp[4],temp[5]-damages)
                        S.chatText = "You use {0}. -{1} hp.".format(attack[0],damages)
                    else:
                        damages = abs(int((S.Sstat['attack']+randint(-15,15))*1.5*attack[3]-temp[7]))
                        changeMob(m,temp[2],temp[3],temp[4],temp[5]-damages)
                        S.chatText = "You use {0}. -{1} hp, CRITICAL !".format(attack[0],damages)
                else:
                    S.chatText = "You miss."
            drawMobSprite(m,temp[3]+32,temp[4]+32)
            if S.debugger:
                d2Drect(temp[3]+32,temp[4]+32,temp[3]+32,temp[4]+32,'red')
            d2Drect(temp[3]+16,temp[4],temp[3]+48,temp[4]+3,'darkRed')
            if temp[5] > 0:
                d2Drect(temp[3]+16,temp[4],temp[3]+16+int(32*temp[5]/temp[9]),temp[4]+3,'red')
    #CheckForDiedMobs
    for a in dieds:
        S.levelBar += MOB_XP_DROP
        S.chatText = "You earn " + str(MOB_XP_DROP) + " experience points !"
        save()
        delMob(a)
        try:
            for b in range(mobCap+1): #We force undirectly the error to be threw
                S.focus[a+b] = S.focus[a+b+1]
        except:
            S.focus[mobCap-1] = 0

def delFromBoss():
    usersFile = open(serverPath + S.Map + '/Boss.users','r')
    content = usersFile.read().split(';')
    usersFile.close()
    usersFile = open(serverPath + S.Map + '/Boss.users','w')
    toWrite = ''
    for u in content:
        if u != userName:
            toWrite += ';' + u
    usersFile.write(toWrite[1:])
    usersFile.close()
    cntFile = open(serverPath + S.Map + '/Boss.cnt','r')
    temp = cntFile.read().split(';')
    cntFile.close()
    if temp[1] == userName: #If I'm the boss admin
        if len(content) > 1: #If there is somebody fighting
            cntFile = open(serverPath + S.Map + '/Boss.cnt','w')
            cntFile.write(temp[0] + ';' + content[2]) #The boss admin is the next focused
            cntFile.close()
        else:
            cntFile = open(serverPath + S.Map + '/Boss.cnt','w')
            cntFile.write('0;') #Restart the cnter
            cntFile.close()

def delBoss(xp,bossName):
    bossFile = open(serverPath + S.Map + '/BossBLANK.info','r')
    content = bossFile.read()
    bossFile.close()
    bossFile = open(serverPath + S.Map + '/Boss.info','w')
    bossFile.write(content)
    bossFile.close()
    usersFile = open(serverPath + S.Map + '/Boss.users','r')
    content = usersFile.read().split(';')
    usersFile.close()
    usersFile = open(serverPath + S.Map + '/Boss.users','w')
    toWrite = ''
    for u in content:
        if u == userName:
            S.levelBar += xp
        else:
            toWrite += ';' + u
    usersFile.write(toWrite[1:])
    usersFile.close()
    cntFile = open(serverPath + S.Map + '/Boss.cnt','w')
    cntFile.write('0;')
    cntFile.close()
    S.chatText = "You have defeated " + bossName + " ! Congratulation !"

def changeBoss(x,y,bossLife):
    bossFile = open(serverPath + S.Map + '/Boss.info','r')
    content = bossFile.read().split(';')
    bossFile.close()
    toWrite = '{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}'.format(content[0],x,y,bossLife,content[4],content[5],content[6],content[7],content[8],content[9],content[10])
    bossFile = open(serverPath + S.Map + '/Boss.info','w')
    bossFile.write(toWrite)
    bossFile.close()

def boss(): #focused <=> leader of the boss cnt
    cnt = 0
    bossAdmin = ''
    bossFile = open(serverPath + S.Map + '/Boss.info','r')
    temp = bossFile.read().split(';')
    bossFile.close()
    for a in range(8):
        temp[a+1] = int(temp[a+1])
    temp[9] = int(temp[9])
    temp[10] = int(temp[10])
    bossT = randint(0,600)
    if bossT == 300 and not temp[9]: # = spawnBoss()
        bossFile = open(serverPath + S.Map + '/BossBLANK.info','r')
        temp1 = bossFile.read().split(';')
        bossFile.close()
        bossFile = open(serverPath + S.Map + '/Boss.info','w')
        bossFile.write('{0};{1};{2};{3};{4};{5};{6};{7};{8};1;{3}'.format(temp1[0],randint(0,maxl-128),randint(0,maxh-128),temp1[3],temp1[4],temp1[5],temp1[6],temp1[7],temp1[8])) #set active
        bossFile.close()
    if temp[9]: #If boss spawned (= active)
        cntFile = open(serverPath + S.Map + '/Boss.cnt','r')
        cnt, bossAdmin = cntFile.read().split(';') #RISK OF CRASH BECAUSE OF THE OVERFLOW (resolve with a while-try loop (using continue))
        cntFile.close()
        cnt = int(cnt)
        usersFile = open(serverPath + S.Map + '/Boss.users','r')
        users = usersFile.read().split(';')
        usersFile.close()
        if users.count(userName) != 0: #if focused
            diffX = max(S.x,temp[1]) - min(S.x,temp[1])
            diffY = max(S.y,temp[2]) - min(S.y,temp[2])
            if diffX > 50: #focus move
                if S.x > temp[1]:
                    changeBoss(temp[1]+2,temp[2],temp[3])
                else:
                    changeBoss(temp[1]-2,temp[2],temp[3])
            elif diffY > 40:
                if S.y > temp[2]:
                    changeBoss(temp[1],temp[2]+1,temp[3])
                else:
                    changeBoss(temp[1],temp[2]-1,temp[3])
            if cnt == int(1000-10*temp[6]): #Boss speed
                if diffX < 115 and diffY < 115:
                    if randint(1,100) > S.Sstat['miss']+1:
                        if randint(0,100) > temp[8]:
                            damages = abs(int((temp[4]+randint(-15,15))-S.Sstat['defence']))
                            S.life -= damages
                            save()
                            S.chatText = "{0} attacks. -{1} hp.".format(temp[0],damages)
                        else:
                            damages = abs(int((temp[4]+randint(-15,15))*1.5-S.Sstat['defence']))
                            S.life -= damages
                            save()
                            S.chatText = "{0} attacks. -{1} hp, CRITICAL !".format(temp[0],damages)
                    else:
                        S.chatText = temp[0] + " miss."
            inLeftZone  = S.x+32 <= temp[1]+64 and S.x+32 >= temp[1]+64-155
            inRightZone = S.x+32 >= temp[1]+64 and S.x+32 <= temp[1]+64+155
            inUpZone    = S.y+32 <= temp[2]+64 and S.y+32 >= temp[2]+64-155
            inDownZone  = S.y+32 >= temp[2]+64 and S.y+32 <= temp[2]+64+155
            inLargeX = inLeftZone or inRightZone
            inLargeY = inUpZone or inDownZone
            if S.debugger:
                if inLargeY:
                    if inLeftZone and S.direction == 2:
                        print("inLeftZone")
                    if inRightZone and S.direction == 4:
                        print("inRightZone")
                if inLargeX:
                    if inUpZone and S.direction == 3:
                        print("inUpZone")
                    if inDownZone and S.direction == 1:
                        print("inDownZone")
                if S.direction == 1:
                    d2Drect(temp[1]+64-155,temp[2]+64,temp[1]+64+155,temp[2]+64+155,'magenta')
                elif S.direction == 2:
                    d2Drect(temp[1]+64-155,temp[2]+64-155,temp[1]+64,temp[2]+64+155,'magenta')
                elif S.direction == 3:
                    d2Drect(temp[1]+64-155,temp[2]+64-155,temp[1]+64+155,temp[2]+64,'magenta')
                else:
                    d2Drect(temp[1]+64,temp[2]+64-155,temp[1]+64+155,temp[2]+64+155,'magenta')
            if attack != [] and ( (S.direction == 1 and inDownZone and inLargeX) or (S.direction == 3 and inUpZone and inLargeX) or (S.direction == 2 and inLeftZone and inLargeY) or (S.direction == 4 and inRightZone and inLargeY) ):
                if randint(0,100) > temp[7]:
                    if randint(0,100) > S.Sstat['critical']/10:
                        damages = abs(int((S.Sstat['attack']+randint(-15,15))*attack[3]-temp[5]))
                        changeBoss(temp[1],temp[2],temp[3]-damages)
                        S.chatText = "You use {0}. -{1} hp.".format(attack[0],damages)
                    else:
                        damages = abs(int((S.Sstat['attack']+randint(-15,15))*1.5*attack[3]-temp[5]))
                        changeBoss(temp[1],temp[2],temp[3]-damages)
                        S.chatText = "You use {0}. -{1} hp, CRITICAL !".format(attack[0],damages)
                else:
                    S.chatText = "You miss."
            if bossAdmin == userName: #If I'm the admin => Isz bossCnt
                cntFile = open(serverPath + S.Map + '/Boss.cnt','w')
                if cnt == int(1000-10*temp[6]):
                    cnt = -1
                cntFile.write(str(cnt+1) + ';' + userName)
                cntFile.close()
        else: #not focused
            move = randint(1,400) #free move
            if move == 399 and temp[1] < maxl-64:
                changeBoss(temp[1]+2,temp[2],temp[3])
            elif move == 2 and temp[1] > 32:
                changeBoss(temp[1]-2,temp[2],temp[3])
            elif move == 398 and temp[2] < maxh-66:
                changeBoss(temp[1],temp[2]+2,temp[3])
            elif move == 3 and temp[2] > 62:
                changeBoss(temp[1],temp[2]-2,temp[3])
            inLeftZone  = S.x+32 <= temp[1]+64 and S.x+32 >= temp[1]+64-155
            inRightZone = S.x+32 >= temp[1]+64 and S.x+32 <= temp[1]+64+155
            inUpZone    = S.y+32 <= temp[2]+64 and S.y+32 >= temp[2]+64-155
            inDownZone  = S.y+32 >= temp[2]+64 and S.y+32 <= temp[2]+64+155
            inLargeX = inLeftZone or inRightZone
            inLargeY = inUpZone or inDownZone
            if S.debugger:
                if inLargeY:
                    if inLeftZone and S.direction == 2:
                        print("inLeftZone")
                    if inRightZone and S.direction == 4:
                        print("inRightZone")
                if inLargeX:
                    if inUpZone and S.direction == 3:
                        print("inUpZone")
                    if inDownZone and S.direction == 1:
                        print("inDownZone")
                if S.direction == 1:
                    d2Drect(temp[1]+64-155,temp[2]+64,temp[1]+64+155,temp[2]+64+155,'magenta')
                elif S.direction == 2:
                    d2Drect(temp[1]+64-155,temp[2]+64-155,temp[1]+64,temp[2]+64+155,'magenta')
                elif S.direction == 3:
                    d2Drect(temp[1]+64-155,temp[2]+64-155,temp[1]+64+155,temp[2]+64,'magenta')
                else:
                    d2Drect(temp[1]+64,temp[2]+64-155,temp[1]+64+155,temp[2]+64+155,'magenta')
            if attack != [] and ( (S.direction == 1 and inDownZone and inLargeX) or (S.direction == 3 and inUpZone and inLargeX) or (S.direction == 2 and inLeftZone and inLargeY) or (S.direction == 4 and inRightZone and inLargeY) ):
                S.chatText = "Focused by {0} ! {1} hp.".format(temp[0],temp[3])
                usersFile = open(serverPath + S.Map + '/Boss.users','r')
                content = usersFile.read()
                usersFile.close()
                usersFile = open(serverPath + S.Map + '/Boss.users','w')
                if len(content) == 0:
                    usersFile.write(userName)
                    cntFile = open(serverPath + S.Map + '/Boss.cnt','w')
                    cntFile.write('0;' + userName)
                    cntFile.close()
                else:
                    usersFile.write(';' + userName)
                usersFile.close()
                S.inBossBattle = True
        if temp[3] <= 0: #check for died boss
            S.inBossBattle = False
            delBoss(MOB_XP_DROP,temp[0]) #SET BOSS XP
        d2Dimg(temp[1]+64,temp[2]+64,mobSkins[temp[0]])
        if S.debugger:
            d2Drect(temp[1]+64,temp[2]+64,temp[1]+64,temp[2]+64,'red')
        d2Drect(temp[1]+32,temp[2],temp[1]+96,temp[2]+3,'purple4')
        if temp[3] > 0:
            d2Drect(temp[1]+32,temp[2],temp[1]+32+int(64*temp[3]/temp[10]),temp[2]+3,'purple3')

def commands(command):
    if command == '/help':
        S.chatText = "Look at the console window of the game.\n"
        print("\n/setStats <Pstat> <value>: Sets your primary stats.\n/setEquip <row> <value>: Sets your equipment(it operates only by ids !).\n/xp <amount>: Gives you experience points.\n/lvl <amount>: Gives you levels.\n/op <pseudo>: Changes a player to administrator.\n/deop <pseudo>: Changes a player to simple player.\n/heal: Heals you to your maximum.\n/tpCoo <x> <y>: Teleports you to (x;y).\n/tpMap <map>: Teleports you to a map.\n/tpPlayer <pseudo>: Teleports you to a player.\n/xy: Prints your coordonates.\n/give <row> <itemName> : Gives to you an item stocked at an inventory row.\n/spawnMob <mobName> <x> <y> : Spawn a mob at (x;y). Input \'Normal\' to natural set.\n/allStats : shows all the stats (secondary stats).\n/debug : Toggle debugging mode.\n/fusion <skill1> <skill2> : Fusion of the two skills (result saved at the first).\n/end: Cancel command input\n")
        return '/end'
    elif command.startswith('/setStats'):
        try:
            command = command.split(' ')
            S.Pstat[command[1]] = int(command[2])
            S.chatText = "Stat changed !"
        except:
            S.chatText = "cannot modify Primary stats."
        return '/end'
    elif command.startswith('/setEquip'):
        try:
            command = command.split(' ')
            S.equipNo[int(command[1])] = int(command[2])
            setEquip()
            try:
                setStats()
                S.chatText = "Equipment and stats set !"
            except:
                S.chatText = "Equipment set but unable to change your Stats."
        except:
            S.chatText = "Unable to change your equipment."
        return '/end'
    elif command.startswith('/xp'):
        try:
            S.levelBar += int(command[4:len(command)])
            save()
            S.chatText = command[4:len(command)] + " xp given !"
        except:
            S.chatText = "amount " + command[4:len(command)] + " is not usable."
        return '/end'
    elif command.startswith('/lvl'):
        try:
            S.level += int(command[4:len(command)])
            save()
            S.chatText = command[4:len(command)] + " levels given !"
        except:
            S.chatText = "amount " + command[4:len(command)] + " is not usable."
        return '/end'
    elif command.startswith('/op'):
        try:
            temp = command[4:]
            change(temp,147,'True')
            S.chatText = command[4:len(command)] + " is now an administrator."
        except:
            S.chatText = "No user " + temp + " founded."
        return '/end'
    elif command.startswith('/deop'):
        try:
            temp = command[4:]
            change(temp,147,'False')
            S.chatText = command[4:len(command)] + " is now a simple player."
        except:
            S.chatText = "No user " + temp + " founded."
        return '/end'
    elif command == '/heal':
        S.life = S.Sstat['lifeMax']
        save()
        S.chatText = "You're now regenerated !"
        return '/end'
    elif command.startswith('/tpCoo'):
        try:
            temp = command.split(' ')
            S.x = int(temp[1])
            S.y = int(temp[2])
            S.chatText = "Teleported yourself at : ({0};{1})".format(S.x,S.y)
        except:
            S.chatText = "Unknown coordonates : ({0};{1}).".format(temp[1],temp[2])
        return '/end'
    elif command.startswith('/tpMap'):
        try:
            temp = command.split(' ')
            temp = temp[1]
        except:
            None
        if temp == 'Lobby(Skyens)' or temp == 'Skyens(North)' or temp == 'Skyens(East)' or temp == 'Skyens(South)' or temp == 'Skyens(West)' or temp == 'Elayl' or temp == 'Elayl(West)' or temp == 'Elayl(East)' or temp == 'Jyams' or temp == 'Jyams(North)' or temp == 'Jyams(South)' or temp == 'Yolms' or temp == 'Yolms(North)' or temp == 'Yolms(South)' or temp == 'Shanke' or temp == 'Shanke(West)' or temp == 'Shanke(East)' or temp == 'Zondemes' or temp == 'Yaleas Dungeon':
            S.Map = temp
            initInteracts()
            S.chatText = 'Teleported yourself in ' + temp + '.'
        else:
            S.chatText = 'Map not found : ' + temp + '.'
        return '/end'
    elif command.startswith('/tpPlayer'):
        try:
            tp(command[4:len(command)])
            S.chatText = "Teleported {0} to {1} !".format(userName,command[4:len(command)])
        except:
            S.chatText = "Unable to teleport yourself."
        return '/end'
    elif command == '/xy':
        S.chatText = 'Your position : ({0};{1})'.format(S.x,S.y)
        return '/end'
    elif command == '/map':
        S.chatText = S.Map
        return '/end'
    elif command.startswith('/give'):
        try:
            temp = command.split(' ')
            temp1 = ''
            for a in temp[2].split('_'):
                temp1 += a + ' '
            if len(temp[2].split('_')) == 1:
                temp1 = temp[2] + ' '
            S.inv[int(temp[1])][0] = temp1[:len(temp1)-1]
            S.chatText = "Given {0} in row {1}.".format(temp1,temp[1])
        except:
            S.chatText = "Invalid inventory row : ." + temp[1]
        return '/end'
    elif command.startswith('/spawnMob'):
        try:
            temp = command.split(' ')
            spawnMob(choice=temp[1],x=int(temp[2]),y=int(temp[3]))
            S.chatText = "Succesfully spawned {0} at ({1};{2}).".format(temp[1],temp[2],temp[3])
        except:
            S.chatText = "Unable to spawn {0} at ({1};{2}).".format(temp[1],temp[2],temp[3])
        return '/end'
    elif command == '/allStats':
        allStats()
        return '/end'
    elif command == '/debug':
        if S.debugger:
            S.debugger = False
        else:
            S.debugger = True
        return '/end'
    elif command.startswith('/fusion'):
        try:
            temp = command.split(' ')
            fusion(temp[1],temp[2],50,50)
            S.chatText = "Skill's fusion completed !"
        except:
            S.chatText = "Cannot get fusion with these skills."
        return '/end'
    #elif command == '/...':
        #try:
        #   do...
        #except:
        #   do...
        #return '/end'
    elif command != '/end':
        S.chatText = "Unknown command : " + command + ", please try again."
        return '/end'
    return command

def fusion(sk1Name,sk2Name,cc1,cc2): #Sk2 will be reset
    tempSk = []
    S.menuText[0] = "Name of the future skill :"
    tempSk.append(getinput())
    S.menuText[0] = ""
    tempSk.append(int((cc1*S.Skills[sk1Name][1]+cc2*S.Skills[sk2Name][1])/(cc1+cc2) - (100*sin(pi/(cc2+1)))/cc1))
    tempSk.append(0)
    tempSk.append(int((cc1*S.Skills[sk1Name][3]+cc2*S.Skills[sk2Name][3])/(cc1+cc2) - (100*sin(pi/(cc2+1)))/cc1))
    tempSk.append(int((cc1*S.Skills[sk1Name][4]+cc2*S.Skills[sk2Name][4])/(cc1+cc2) + (100*sin(pi/(cc2+1)))/cc1))
    tempSk.append(int((cc1*S.Skills[sk1Name][5]+cc2*S.Skills[sk2Name][5])/(cc1+cc2) + (100*sin(pi/(cc2+1)))/cc1))
    tempSk.append(int((cc1*S.Skills[sk1Name][6]+cc2*S.Skills[sk2Name][6])/(cc1+cc2) - (400*sin(pi/(cc2+1)))/(cc1*10)))
    tempSk.append(int((cc1*S.Skills[sk1Name][7]+cc2*S.Skills[sk2Name][7])/(cc1+cc2) - (200*sin(pi/(cc2+1)))/(cc1*10)))
    tempSk.append(int((cc1*S.Skills[sk1Name][8]+cc2*S.Skills[sk2Name][8])/(cc1+cc2) + (200*sin(pi/(cc2+1)))/(cc1*10)))
    S.Skills[str(min(int(sk1Name),int(sk2Name)))] = tempSk
    S.Skills[str(min(int(sk1Name),int(sk2Name)))] = ['',0,0,0,0,0,0,0,0]

def getInput(active=True):
    e = Entry(game)
    e.pack()
    e.bind('<Return>',getReturn)
    while not (S.key == 'return'):
        e.focus_set()
        clean(fps,active=active)
    text = e.get()
    e.destroy()
    display.focus_set()
    if text == '':
        return ' '
    else:
        return text

def clean(x,active=True,bg=True):
    if active:
        if bg:
            d2Dimg(maxl/2,maxh/2+30,S.background)
            #WAITING FOR MAP SPRITES
            d2Dimg(632,74,tempImg)
            d2Dimg(632,698,tempImg)
            d2Dimg(32,420,tempImg)
            d2Dimg(1244,420,tempImg)
        if False: #S.debugger:
            d = [(),(),(),()]
            if S.direction == 1 or S.direction == 3:
                mcx = int(content[2+a])-64
                Mcx = int(content[2+a])+64
                mcy = int(content[3+a])-32
                Mcy = int(content[3+a])+32
            else:
                mcx = int(content[2+a])-32
                Mcx = int(content[2+a])+32
                mcy = int(content[3+a])-64
                Mcy = int(content[3+a])+64
            d2Drect(640,62,'yellow') #UpOutZone
            d2Drect(640,686,'yellow') #DownOutZone
            d2Drect(32,398,'yellow') #LeftOutZone
            d2Drect(1232,398,'yellow') #RightOutZone
        #INTERACTS
        for a in S.interacts:
            temp = a.split(';')
            temp[0] = int(temp[0])
            temp[1] = int(temp[1])
            if temp[2] == 'npc':
                d2Dimg(temp[0],temp[1],npcSprites[temp[3]])
            elif temp[2] == 'seller':
                d2Dimg(temp[0],temp[1],sellersSprites[temp[3]])
        #XP
        levelLimit = int(((2*log(S.level+1))*(S.level+1))*2)
        if S.levelBar >= levelLimit:
            S.level += 1
            S.levelBar -= levelLimit
            setStats()
            save()
            if S.level != 1:
                S.chatText = "You grow to level " + str(S.level) + " !"
        #CHAT
        chatAble = checkChatAble()
        if chatAble == True:
            chatFile = open(serverPath + S.Map + '/chat.txt','r')
            S.chatText = chatFile.read()
            chatFile.close()
            change(userName,148,'False')
        #OTHER PLAYERS
        users = checkForUsers()
        if len(users) != 0:
            for u in range(len(users)):
                temp = getUsersInfo(users[u])
                if temp != 'No':
                    d2Dimg(temp[1]+32,temp[2]+32,defaultSkins[temp[3] + directions[temp[0]-1]])
                    try:
                        d2Dimg(temp[1]+32,temp[2]+32,equipSprites[temp[4] + directions[S.direction-1]])
                    except:
                        None
                    try:
                        d2Dimg(temp[1]+32,temp[2]+32,equipSprites[temp[5] + directions[S.direction-1]])
                    except:
                        None
                    try:
                        if temp[7] == 0:
                            d2Dimg(temp[1]+32,temp[2]+32,equipSprites[temp[6] + directions[S.direction-1]]) #ADD THE 4 DIRECTIONS
                        else:
                            d2Dimg(temp[1]+64,temp[2]+32,equipSprites[temp[6] + 'Armed' + directions[S.direction-1]]) #ADD THE 4 DIRECTIONS 
                    except:
                        None
        d2Dimg(S.x+32,S.y+32,S.skin[str(S.direction)])
        if S.armedCnt != 0:
            S.armedCnt -= 1
            if S.direction == 2 or S.direction == 3:
                temp = 32
            else:
                temp = -32
            try:
                d2Dimg(S.x+32+temp,S.y+32,equipSprites[S.names[2] + 'Armed' + directions[S.direction-1]])
            except:
                None
        else:
            try:
                d2Dimg(S.x+32,S.y+32,equipSprites[S.names[2] + directions[S.direction-1]])
            except:
                None
        d2Drect(0,0,408,15,'darkRed')
        d2Drect(0,0,int(408*S.life/S.Sstat['lifeMax']),15,'red')
        d2Drect(0,15,408,30,'darkBlue')
        d2Drect(0,15,int(408*S.mana/S.Sstat['manaMax']),30,'blue')
        d2Drect(0,30,maxl,45,'darkGreen')
        d2Drect(0,30,int(maxl*S.levelBar/(levelLimit+1)),45,'green')
        try:
            d2Dimg(S.x+32,S.y+32,equipSprites[S.names[0] + directions[S.direction-1]])
        except:
            None
        try:
            d2Dimg(S.x+32,S.y+32,equipSprites[S.names[1] + directions[S.direction-1]])
        except:
            None
        if S.debugger:
            d2Drect(S.x+32,S.y+32,S.x+32,S.y+32,'red')
    S.mouseState = ''
    display.create_text(maxl/2,maxh+50,text=S.chatText,fill='yellow',font='yellow')
    for a in range(6):
        display.create_text(maxl/2,maxh+10+20*(a+3),text=S.menuText[a],fill='grey20',font='grey20')
    display.update()
    display.delete(ALL)
    sleep(1/x)

#INITIALISATION
class Skiller:
    def __init__(self):
        self.key = ''
        self.mouseState = ''
        self.mousePos = [0,0]
        self.direction = 3
        self.Class1 = ''
        self.ClassLevel1 = 0
        self.Class2 = ''
        self.ClassLevel2 = 0
        self.Class3 = ''
        self.ClassLevel3 = 0
        self.Class4 = ''
        self.ClassLevel4 = 0
        self.life = 80
        self.mana = 25
        self.keys = {'up':'z','right':'d','down':'s','left':'q','inv':'b','next':'n','save':'l','keys':'k','stats':'c','quit':'e','chat':'t','spell0':'0','spell1':'1','spell2':'2','spell3':'3','spell4':'4','spell5':'5','spell6':'6','spell7':'7','spell8':'8','spell9':'9'}
        self.Pstat = {'strAD':25,'agiMS':25,'dexSC':25,'intMC':25,'magAD':25}
        self.Sstat = {'lifeMax':80,'manaMax':25,'attack':0,'defence':0,'speed':0,'miss':0,'critical':0}
        self.equip = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        self.equipNo = [0,0,0,0,0]
        self.names = ['','','','','']
        self.invSprite = 0
        self.inv = [['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0],['nothing',0]]
        self.Map = 'Lobby(Skyens)'
        self.focus = []
        self.chatAble = False
        self.x = 808
        self.y = 424
        self.level = 0
        self.levelBar = 0
        self.skills = {'punch':["punch",0,0,5,0,0,0,0,0],'1':["",0,0,0,0,0,0,0,0],'2':["",0,0,0,0,0,0,0,0],'3':["",0,0,0,0,0,0,0,0],'4':["",0,0,0,0,0,0,0,0],'5':["",0,0,0,0,0,0,0,0],'6':["",0,0,0,0,0,0,0,0],'7':["",0,0,0,0,0,0,0,0],'8':["",0,0,0,0,0,0,0,0],'9':["",0,0,0,0,0,0,0,0]}
        self.manaTimer = 10
        self.armedCnt = 0
        self.interacts = []
        self.opped = 'False'
        self.chatText = ""
        self.menuText = ["","","","","",""]
        self.background = ''
        self.skin = {'1':'','2':'','3':'','4':''}
        self.inBossBattle = False
        self.debugger = False
global serverPath,game,display,maxl,maxh,userName,password,Class,opped,chatAble
temp = open('_data/server.path','r')
serverPath = temp.read()
temp.close()
fps = 60
maxl = 1296
maxh = 752
game = Tk()
game.title('Skiller[1.1.0]')
game.protocol('WM_DELETE_WINDOW',quitGame)
display = Canvas(game,width=maxl-1,height=maxh-1+180,background='DarkGoldenrod3')
display.bind('<KeyPress>',getKeyP)
display.bind('<KeyRelease>',getKeyR)
display.bind('<Button-1>',getLClick)
display.bind('<Button-2>',getMClick)
display.bind('<Button-3>',getRClick)
display.focus_set()
defaultSkins = {}
mobSkins = {}
itemSprites = {}
equipSprites = {}
npcSprites = {}
sellersSprites = {}
S = Skiller()
temp = [0,0,0]
temp[0] = Label(game,text="                                                                                                                                                                                                          S K I L L E R                                                                                                                                                                                                                ",bg='DarkGoldenrod3')
temp[1] = Label(game,text="                                                                                                                                                                                                    press " + S.keys['next'] + " to continue                                                                                                                                                                                                        ",background='DarkGoldenrod3')
temp[2] = Label(game,text=" by I.A. and JESUS                                                                                                                                                                                                                                                                                                                                                                                                               ",background='DarkGoldenrod3')
#packing
temp[0].pack()
temp[1].pack()
temp[2].pack()
display.pack()
display.update()

tempImg = PhotoImage(file='_data/sprites/tempOuts.gif') #Waiting for map's sprites

#START#
stand = 1
while stand:
    if S.key == 'P' + S.keys['next']:
        stand = 0
    clean(fps,active=False)
temp[0].destroy()
temp[1].destroy()
temp[2].destroy()
stand = 1
state = 0
while stand:
    if state == 0:
        S.menuText[0] = "Log in        " + S.keys['up']
        S.menuText[1] = "Register      " + S.keys['down']
        for a in range(4):
            S.menuText[a+2] = ""
        stand1 = 1
        while stand1:
            if S.key == 'P' + S.keys['up']:
                stand1 = 0
                state = 1
                for a in range(6):
                    S.menuText[a] = ""
            elif S.key == 'P' + S.keys['down']:
                stand1 = 0
                state = 2
                for a in range(6):
                    S.menuText[a] = ""
            clean(fps,active=False)
    if state == 1:
        stand1 = 1
        while stand1:
            S.menuText[0] = "Please log in"
            S.menuText[1] = "Username :"
            for a in range(4):
                S.menuText[a+2] = ""
            display.update()
            userName = getInput(active=False)
            sleep(0.2)
            S.menuText[0] = ""
            S.menuText[1] = "Password :"
            for a in range(4):
                S.menuText[a+2] = ""
            display.update()
            password = getInput(active=False)
            if checkUserName() and checkUserPassword() and getUserAbility(userName):
                getUserInfo()#sets User Unable btw
                save()
                stand1 = 0
                stand = 0
            else:
                S.menuText[3] = ""
                S.menuText[4] = "retry      " + S.keys['next']
                S.menuText[5] = "main menu  " + S.keys['quit']
                stand2 = 1
                while stand2:
                    if S.key == 'P' + S.keys['next']:
                        stand2 = 0
                    elif S.key == 'P' + S.keys['quit']:
                        stand2 = 0
                        stand1 = 0
                        state = 0
                    clean(fps,active=False)
            clean(fps,active=False)
    if state == 2:
        stand1 = 1
        while stand1:
            S.menuText[0] = "Please enter a username:"
            display.update()
            userName = getInput(active=False)
            sleep(0.2)
            if not checkUserName():
                S.menuText[0] = "Please enter a password:"
                display.update()
                password = getInput(active=False)
                S.menuText[0] = "Choose a class :\n"         #classDefinition
                S.menuText[1] = "- Barbarian    1"
                S.menuText[2] = "- Paladin       2"
                S.menuText[3] = "- Priest          3"
                S.menuText[4] = "- Rogue        4"
                S.menuText[5] = "- Wizard        5"
                stand2 = 1
                while stand2:
                    if S.key == 'P1':
                        S.Class1 = 'barbarian'
                        S.Pstat['strAD'] += int(0.7*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.7*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.7*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.7*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.7*S.Pstat['magAD'])
                        stand2 = 0
                    elif S.key == 'P2':
                        S.Class1 = 'paladin'
                        S.Pstat['strAD'] += int(0.6*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.6*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.6*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.6*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.7*S.Pstat['magAD'])
                        stand2 = 0
                    elif S.key == 'P3':
                        S.Class1 = 'priest'
                        S.Pstat['strAD'] += int(0.5*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.5*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.5*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.5*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.5*S.Pstat['magAD'])
                        stand2 = 0
                    elif S.key == 'P4':
                        S.Class1 = 'rogue'
                        S.Pstat['strAD'] += int(0.4*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.4*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.4*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.4*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.4*S.Pstat['magAD'])
                        stand2 = 0
                    elif S.key == 'P5':
                        S.Class1 = 'wizard'
                        S.Pstat['strAD'] += int(0.3*S.Pstat['strAD'])
                        S.Pstat['agiMS'] += int(0.3*S.Pstat['agiMS'])
                        S.Pstat['dexSC'] += int(0.3*S.Pstat['dexSC'])
                        S.Pstat['intMC'] += int(0.3*S.Pstat['intMC'])
                        S.Pstat['magAD'] += int(0.3*S.Pstat['magAD'])
                        stand2 = 0
                    clean(fps,active=False)
                for a in range(6):
                    S.menuText[a] = ""
                S.menuText[0] = "Class defined : " + S.Class1
                S.menuText[1] = "press " + S.keys['next'] + " to continue"
                stand2 = 1
                while stand2:
                    if S.key == 'P' + S.keys['next']:
                        stand2 = 0
                        stand1 = 0
                        stand = 0
                        save()
                    clean(fps,active=False)
            else:
                S.menuText[2] = "Username already used."
            clean(fps,active=False)
    clean(fps,active=False)
if userName == 'I.A.':
    S.opped = 'True'
    save()
for a in range(6):
    S.menuText[a] = ""
########################################################################################################### MAIN ###########################################################################################################################
if S.Class1 == 'wizard':
    S.skills['1'] = ["Deus Might",40,0,10,100,0,0,5,10]

setSprites()
S.Sstat['lifeMax'] = 80
S.x = maxl/2-8
S.y = maxh/2-8
S.Map = 'Lobby(Skyens)'
mobCap = 5
for a in range(mobCap):
    S.focus.append(0)
setEquip()
setStats()
initInteracts()
MOB_ATK = 5
MOB_DEF = 15
MOB_SPD = 10
MOB_LIFE = 100
MOB_MISS = 20
MOB_CRTK = 5
MOB_XP_DROP = 5
BOSS_XP_DROP = 500
running = 0
step = 0
stepping = False
attack = []
check = 0
directions = ['Up','Right','Down','Left']
stand = 1
while stand:
    d2Dimg(maxl/2,maxh/2+30,S.background)
    #WAITING FOR MAP SPRITES
    d2Dimg(632,74,tempImg)
    d2Dimg(632,698,tempImg)
    d2Dimg(32,420,tempImg)
    d2Dimg(1244,420,tempImg)
    #
    if running == 0:
        if S.key == 'P' + S.keys['up']:
            S.direction = 1
            if S.y > 62:
                running = 1
            elif not S.inBossBattle:
                checkExit()
                save()
        elif S.key == 'P' + S.keys['down']:
            S.direction = 3
            if S.y < maxh-66:
                running = 3
            elif not S.inBossBattle:
                checkExit()
                save()
        elif S.key == 'P' + S.keys['left']:
            S.direction = 4
            if S.x > 32:
                running = 4
            elif not S.inBossBattle:
                checkExit()
                save()
        elif S.key == 'P' + S.keys['right']:
            S.direction = 2
            if S.x < maxl-64:
                running = 2
            elif not S.inBossBattle:
                checkExit()
                save()
        elif S.key == 'P' + S.keys['spell0']:
            attack = S.skills['punch']
        elif S.key == 'P' + S.keys['spell1']:
            attack = S.skills['1']
        elif S.key == 'P' + S.keys['spell2']:
            attack = S.skills['2']
        elif S.key == 'P' + S.keys['spell3']:
            attack = S.skills['3']
        elif S.key == 'P' + S.keys['spell4']:
            attack = S.skills['4']
        elif S.key == 'P' + S.keys['spell5']:
            attack = S.skills['5']
        elif S.key == 'P' + S.keys['spell6']:
            attack = S.skills['6']
        elif S.key == 'P' + S.keys['spell7']:
            attack = S.skills['7']
        elif S.key == 'P' + S.keys['spell8']:
            attack = S.skills['8']
        elif S.key == 'P' + S.keys['spell9']:
            attack = S.skills['9']
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
                    chatFile = open(serverPath + S.Map + '/chat.txt','w')
                    chatFile.write(command)
                    chatFile.close()
                    change(userName,148,'True')
                    users = checkForUsers()
                    for u in range(len(users)):
                        try:
                            change(users[u],148,'True')
                        except:
                            continue
                    command = '/end'
        elif S.key == 'P' + S.keys['stats']:
            showStats()
        elif S.key == 'P' + S.keys['save']:
            save()
            S.chatText = "Party saved !\n"
        elif S.key == 'P' + S.keys['keys']:
            setKeys()
        elif S.key == 'P' + S.keys['inv']:
            showInv()
            setStats()
        elif S.key == 'P' + S.keys['quit']:
            S.menuText[0] = "quit ?"
            S.menuText[1] = "yes  " + S.keys['up']
            S.menuText[2] = "no   " + S.keys['down']
            for a in range(3):
                S.menuText[a+3] = ""
            stand1 = 1
            stand2 = 1
            while stand1:
                if S.key == 'P' + S.keys['up']:
                    stand1 = 0
                elif S.key == 'P' + S.keys['down']:
                    stand1 = 0
                    stand2 = 0
                clean(fps)
            S.menuText[0] = "save ?"
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
                clean(fps)
            for a in range(6):
                S.menuText[a] = ""
    #DEATH
    if S.life < 0:
        delFromBoss()
        if S.inBossBattle:
            S.chatText = "You died. But get a little bit of xp ;D !"
            S.levelBar += int(0.005*BOSS_XP_DROP)
        else:
            S.chatText = "You died."
        S.inBossBattle = False
        S.Map = 'Lobby(Skyens)'
        S.focus = [0,0,0,0,0]
        S.life = S.Sstat['lifeMax']
        save()
    #INTERACTS
    for a in S.interacts:
        temp = a.split(';')
        temp[0] = int(temp[0])
        temp[1] = int(temp[1])
        if temp[2] == 'npc':
            if S.mouseState == 'L' and S.mousePos[0] >= temp[0]-20 and S.mousePos[0] <= temp[0]+20 and S.mousePos[1] >= temp[1]-20 and S.mousePos[1] <= temp[1]+20:
                npc(temp[3])
        elif temp[2] == 'seller':
            if S.mouseState == 'L' and S.mousePos[0] >= temp[0]-20 and S.mousePos[0] <= temp[0]+20 and S.mousePos[1] >= temp[1]-20 and S.mousePos[1] <= temp[1]+20:
                print('Seller interaction with',temp[3]) #Code for sellers
    #
    setInfo()
    if S.Map == 'Yaleas Dungeon':
        boss()
    else:
        mobs()
    if running == 1 and S.y > 62:
        S.y -= 2
    elif running == 2 and S.x < maxl-64:
        S.x += 2
    elif running == 3 and S.y < maxh-66:
        S.y += 2
    elif running == 4 and S.x > 32:
        S.x -= 2
    if running != 0:
        step += 4
    if (S.key == 'R' + S.keys['up'] and running == 1) or (S.key == 'R' + S.keys['right'] and running == 2) or (S.key == 'R' + S.keys['down'] and running == 3) or (S.key == 'R' + S.keys['left'] and running == 4):
        stepping = True
    if stepping and step % 16 == 0:
        step = 0
        stepping = False
        running = 0
    if attack != []:
        attack = []
        S.armedCnt = 10
    clean(8*fps,bg=False)
