#!/usr/bin/env python3
'''
nethack assistant(cheater)
by petergu
'''

import os
import sys
import subprocess
import re

print('Welcome to nha -- nethack assistant')
sts, gameexe = subprocess.getstatusoutput('which nethack')
if sts != 0:
    print('nethack not found!')
    sys.exit(1)
else:
    print('nethack executable(or symlink) found at %s' % gameexe)
gamesaveroot = '/var/games/nethack'
savedir = '~/.nha'
cmdshowscore = 'nethack -s -v'
cmdrungame = 'nethack'
cmdgamediscover = 'nethack -X'
cmdgamedebug = 'nethack -D'
cmdmk_nha_dir = '''
if [ ! -d ~/.nha ]; then
	mkdir ~/.nha
	if '$?' != '0'; then
		echo "mkdir ~/.nha failed!"
		exit 1
	fi
fi
echo "~/.nha exists"
exit 0
'''
cmddelete = 'rm -rf ' + savedir
dscrbfile = 'dscrb.txt'
timefile = 'time.txt'
cmdgettime = 'date'
homedir = os.getenv('HOME')
user = os.getenv('USER')
uid = str(os.getuid())
ufile = uid + user

print('game save root is set to %s' % gamesaveroot)
print('user %s, uid %s, save file name %s' % (user, uid, ufile))
print('saves are at %s(if nothing wrong)' % savedir)


def help():
    print('#Script cmds')
    print('q -- quit')
    print('l -- clear screen')
    print('h -- show this help msg')

    print('\n#Save Repo Cmds')
    print('ll -- list save repos')
    print('u -- use a save repo')
    print('n -- new save repo')
    print('x -- delete a save repo')
    # print('aa -- apply all, restore saved game save dir[W:Cover old file!]')

    print('\n#Save Cmds(to current save repo)')
    print('ls -- list saves')
    print('d -- delete a save')
    print('s -- save from game(now from %s)' % gamesaveroot)
    print('a -- apply a change from saves to game[old save backuped, old backup overwriten]')
    print('e -- edit a save description')

    print('\n#Dir Cmds')
    print('b -- back up whole game save dir(%s)' % gamesaveroot)
    print('tg -- tree game save root %s(tree should be installed)' % gamesaveroot)
    print('ts -- tree save dir %s(tree should be installed)' % savedir)
    print('dd -- delete dir %s, which includes all saves(%s)[W:rm -rf!!!]' % (savedir, cmddelete))

    print('\n#Game Cmds')
    print('S -- show high score(%s)' % cmdshowscore)
    print('R -- run game(%s)' % cmdrungame)
    print('X -- run game in discover mode(%s)' % cmdgamediscover)
    print('D -- run game in wizard(debug) mode, root required')
    print('T -- trash current save(trash should be installed)')
def runcmd(cmd, msg = 'Command returned a non-zero value, maybe something wrong happened'):
    sts, out = subprocess.getstatusoutput(cmd)
    print(out)
    if sts != 0:
        print('Hint: %s' % msg)
    return sts
def mkdefaultrepo():
    runcmd(r'mkdir ~/.nha/0 && echo "default save repo" >> ~/.nha/0/dscrb.txt')
def isnumber(s):
    if re.match(r'^[0-9]+$', s) != None:
        return 1
    else:
        return 0

runcmd(cmdmk_nha_dir)

running = 1
reponum = int(subprocess.getstatusoutput(r'ls ~/.nha | egrep "[0-9]+" | wc -l')[1])
if reponum == 0:
    print('No save found, create default repo')
    mkdefaultrepo()
    reponum = 1
repouse = reponum - 1
print('use latest repo ' + str(reponum - 1))
while running:
    reponum = int(subprocess.getstatusoutput(r'ls ~/.nha | egrep "[0-9]+" | wc -l')[1])
    if reponum == 0:
        mkdefaultrepo()
        reponum = 1
    # print('use latest repo ' + str(reponum - 1))
    savenum = int(subprocess.getstatusoutput('ls ~/.nha/' + str(repouse) + r' | egrep "[0-9]+" | wc -l')[1])
    print('nha:%d>' % repouse, end='')
    cmd = input()
    #Script cmds
    if cmd == 'q':
        running = 0
    elif cmd == 'h':
        help()
    elif cmd == 'l':
        os.system('clear')
    #Save Repo Cmds
    elif cmd == 'll':
        print('Total %d save repos.' % reponum)
        for i in range(reponum):
            print('Repo %d' % i)
            print('\tDescription: ', end='')
            runcmd('cat ~/.nha/' + str(i) + '/' + dscrbfile, 'No description found')
    elif cmd == 'u':
        print('Which repo to use?>', end='')
        rid = input()
        if isnumber(rid):
            rid2 = int(rid)
            if rid2 in range(reponum):
                repouse = rid2
            else:
                print('You may have the wrong id')
        else:
            print('Not a number')
    elif cmd == 'n':
        runcmd('mkdir ~/.nha/' + str(reponum))
        print('Enter a description>', end='')
        dscrb = input()
        if dscrb == '':
            print('canceled')
            runcmd('rmdir ~/.nha/' + str(reponum))
            continue
        #need absolute path here
        #write describe file
        file2write = homedir + '/.nha/' + str(reponum) + '/' + dscrbfile
        fout = open(file2write, 'w')
        fout.write(dscrb)
        fout.write('\n')
        fout.close()
        print('ok')
    elif cmd == 'x':
        print('Which repo to delete?>', end='')
        isdeled = 0
        did = input()
        print('Sure to delete?[N/y]', end='')
        jdg = input()
        if jdg != 'y':
            print('nothing done')
            continue
        if isnumber(did):
            did2 = int(did)
            if repouse == did2:
                #repo in use deleted!
                repouse = reponum - 2
                #if no repo left, 0 will be created automaticly
                if repouse < 0:
                    repouse = 0
            if did2 in range(reponum):
                runcmd('rm -rf ~/.nha/' + str(did2))
                for i in range(did2 + 1,reponum):
                    runcmd('mv ~/.nha/' + str(i) + ' ' + '~/.nha/' + str(i - 1))
                isdeled = 1
                #savenum should -1 but not need
        if isdeled == 0:
            print('Nothing done. You may inputed a wrong save id')
    #Save Cmds
    elif cmd == 'ls':
        print('Total %d saves.' % savenum)
        for i in range(savenum):
            print(str(i) + ':')
            print('\tName: ', end='')
            runcmd('ls ~/.nha/' + str(repouse) + '/' + str(i) + '/ | grep -v ' + dscrbfile)
            print('\tDescription: ', end='')
            runcmd('cat ~/.nha/' + str(repouse) + '/' + str(i) + '/' + dscrbfile, 'No description found')
            print('\tTime: ', end='')
            runcmd('cat ~/.nha/' + str(repouse) + '/' + str(i) + '/' + timefile + ' 2>/dev/null', 'No time record found')
    elif cmd == 'd':
        print('Which save to delete?>', end='')
        isdeled = 0
        did = input()
        if isnumber(did):
            did2 = int(did)
            if did2 in range(savenum):
                runcmd('rm -rf ~/.nha/' + str(repouse) + '/' + str(did2))
                for i in range(did2 + 1,savenum):
                    runcmd('mv ~/.nha/' + str(repouse) + '/' + str(i) + ' ' + '~/.nha/' + str(repouse) + '/' + str(i - 1))
                isdeled = 1
                #savenum should -1 but not need
        if isdeled == 0:
            print('Nothing done. You may inputed a wrong save id')
    elif cmd == 's':
        print('Enter a description>', end='')
        dscrb = input()
        if dscrb == '':
            print('canceled')
            continue
        runcmd('mkdir ~/.nha/' + str(repouse) + '/' + str(savenum))
        sts = runcmd('sudo cp -a ' + gamesaveroot + '/save/' + ufile + '.gz ~/.nha/' + str(repouse) + '/' + str(savenum) + '/', \
                'May be you have no saved game?')
        if sts != 0:
            runcmd('rmdir ~/.nha/' + str(repouse) + '/' + str(savenum))
            continue
        #need absolute path here
        #write describe file
        file2write = homedir + '/.nha/' + str(repouse) + '/' + str(savenum) + '/' + dscrbfile
        fout = open(file2write, 'w')
        fout.write(dscrb)
        fout.write('\n')
        fout.close()
        #write time record file
        file2write = homedir + '/.nha/' + str(repouse) + '/' + str(savenum) + '/' + timefile
        fout = open(file2write, 'w')
        fout.write(str(subprocess.getstatusoutput(cmdgettime)[0]))
        fout.write('\n')
        fout.close()
        print('saved')
    elif cmd == 'a':
        print('Which save to apply?>', end='')
        isapld = 0
        aid = input()
        if isnumber(aid):
            aid2 = int(aid)
            if aid2 in range(savenum):
                print('old save will be backuped')
                runcmd('sudo cp -a ' + gamesaveroot + '/save/' + ufile + '.gz ' \
                        + gamesaveroot + '/save/' + ufile + '.gz.bak'\
                        , 'may be you have no previous save? or something went wrong?')
                runcmd('sudo cp -a ~/.nha/' + str(repouse) + '/' + str(aid2) + '/' + ufile + '.gz ' + gamesaveroot + '/save/')
            isapld = 1
        if isapld == 0:
            print('Nothing done. You may inputed a wrong save id')
    elif cmd == 'e':
        print('Which save description to edit?>', end='')
        isedted = 0
        eid = input()
        if isnumber(eid):
            eid2 = int(eid)
            if eid2 in range(savenum):
                #at here, output is need to be seen, and subprocess is not OK
                os.system('vi ~/.nha/' + str(repouse) + '/' + str(eid2) + '/dscrb.txt')
            isedted = 1
        if isedted == 0:
            print('Nothing done. You may inputed a wrong save id')
    #Dir Cmds
    elif cmd == 'b':
        runcmd('gzip ' + gamesaveroot + ' -c > ~/.nha/bkup.gz')
    elif cmd == 'tg':
        os.system('tree ' + gamesaveroot)
    elif cmd == 'ts':
        os.system('tree ' + savedir)
    elif cmd == 'dd':
        print('Sure to delete?[N/y]', end='')
        jdg = input()
        if jdg == 'y':
            runcmd(cmddelete)
            print('done')
            sys.exit(0)
        else:
            print('Nothing is done')
    #Game Cmds
    elif cmd == 'S':
        runcmd(cmdshowscore)
    elif cmd == 'R':
        os.system(cmdrungame)
    elif cmd == 'X':
        os.system(cmdgamediscover)
    elif cmd == 'D':
        os.system(cmdgamedebug)
    elif cmd == 'T':
        runcmd('sudo trash ' + gamesaveroot + '/save/' + ufile + '.gz', 'Something wrong? May be trash not installed?')
    else:
        print('command not recognized, h for help')
    
print('goodbye')

