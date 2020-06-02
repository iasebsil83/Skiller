from time import sleep
from glob import glob

pathFile = open('_data/server.path','r')
serverPath = pathFile.read()
pathFile.close()
All = glob(serverPath + 'users/*.user')
for a in range(len(All)):
    userFile = open(All[a],'r')
    content = userFile.read().split(';')
    userFile.close()
    toWrite = ''
    userFile = open(All[a],'w')
    for b in range(len(content)):
        if b != 1:
            toWrite += content[b]
            if b != len(content)-1:
                toWrite += ';'
        else:
            toWrite += 'Able;'
    userFile.write(toWrite)
    userFile.close()
All = glob(serverPath + '*')
for a in range(len(All)):
    if not All[a].endswith('users'):
        mobFile = open(All[a] + '/mobs.dat','w')
        mobFile.write('')
        mobFile.close()
Bosses = []
Bosses.append(
    ( open(serverPath + 'Yaleas Dungeon/Boss.info','w'),
      open(serverPath + 'Yaleas Dungeon/BossBLANK.info','r'),
      open(serverPath + 'Yaleas Dungeon/Boss.users','w'),
      open(serverPath + 'Yaleas Dungeon/Boss.cnt','w')       )
    )
'''
Bosses.append(
    ( open(serverPath + '#bossName#/Boss.info','w'),
      open(serverPath + '#bossName#/BossBLANK.info','r'),
      open(serverPath + '#bossName#/Boss.users','w'),
      open(serverPath + '#bossName#/Boss.cnt','w')       )
    )
'''
for a in range(len(Bosses)):
    Bosses[a][0].write(Bosses[a][1].read()) #fill the .info with the BLANK's .info
    Bosses[a][0].close()
    Bosses[a][1].close()
    Bosses[a][2].write('') #reset users
    Bosses[a][2].close()
    Bosses[a][3].write('0;') #reset cnts
    Bosses[a][3].close()
print('Everybody disconnected and all mobs killed.\nSkiller repaired !')
sleep(3)
