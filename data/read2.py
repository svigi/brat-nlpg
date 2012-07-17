#!/usr/bin/python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:


import codecs
import re
import string
import sys

# Functions and classes

def collection_str(collection):
    if isinstance(collection, list):
        brackets = '[%s]'
        single_add = ''
    elif isinstance(collection, tuple):
        brackets = '(%s)'
        single_add = ','
    else:
        return str(collection)
    items = ', '.join([collection_str(x) for x in collection])
    if len(collection) == 1:
        items += single_add
    return brackets % items


class Szoelemzes(object):
    def __init__(self, token=None, elemzes=None):
        self.token = token
        self.elemzes = elemzes
        


def check_id_token(token):
    checkpattern = r'({=[^}]+})'
    matcher = re.match(checkpattern, token, 0)
    if (matcher == None):
        print "Ez a token nem ID:", token
        return False
    
    print "ID-t találtam:", token
    return True


# Main program

counter = 1
#print len(sys.argv)
#exit(2)
startpos = -1
endpos = -1
if (len(sys.argv) == 3):
    startpos = int(sys.argv[1])
    endpos = int(sys.argv[2])
else:
    exit(2)

f = codecs.open('szemeszet.dat', 'r', 'utf8')
#f = codecs.open('szemeszetnincsspace1.dat', 'r', 'utf8')
print "startpos", startpos
print "endpos", endpos

#line = f.readline()
lista = []
tokencounter = 0

for line in f:
    print "Új sort olvastam"
    #utolsokarakter = line[len(line)-2] + line[len(line)-1]
    utolsokarakter = line[len(line)-2].encode('utf8').encode('hex')
    #print "Utolsó karakter: {0}\n".format(utolsokarakter.encode('utf8').encode('hex')) 
    if (utolsokarakter == '20'):
        print "Szóköz van a végén"
    else:
        print "Nincs szóköz a végén"
        line += ' '
    #sor végi LF karaktert ne számoljuk!
    tokencounter = 0
    counter -= 1
    linesplit = line.split(' ')
    pattern = r'^([^{|]+)(.+)'
    linesplit_len = len(linesplit)
    for idx in range(linesplit_len):
        token = linesplit[idx]
        if (tokencounter == 0):
            tokencounter += 1
            if (check_id_token(token)):
                continue
        
        #tokencounter += 1
        szo = re.sub(pattern, r'\1', token)
        elemzesek = re.sub(pattern, r'\2', token)

        elemzesek = string.replace(elemzesek, '{{', '')
        elemzesek = string.replace(elemzesek, '}}', '')
        elemzeslista = elemzesek.split('||')

        #workaround
        #rossz a regexp?
        if (len(elemzeslista) == 1):
            if (szo != elemzesek):
                szo += elemzesek

        #print "ellenorzes"
        szohossz = len(szo)
        endpos2 = counter + szohossz
        print "startpos", startpos, "endpos", endpos, "counters", counter, endpos2, token
        
        if (counter == startpos and endpos2 != endpos):
           print "startpos egyezik, de endpos nem, részleges szó?"
           print ""
           print "bejegyzés:", token
           print "szó string:", szo, ", szó start:", counter, ", szó vége:" , counter + len(szo), ", szó hossza:", len(szo)
           if (len(elemzeslista) != 1):
               print "elemzés string:", elemzesek, ", start: ", counter, "hossz: ", len(elemzesek)
           else:
               print "elemzés string: nincs elemzés"

           elemzeslista = elemzesek.split('||')
           elemzesek = string.replace(elemzesek, '{{', '')
           elemzesek = string.replace(elemzesek, '}}', '')

           print "elemzések száma:", len(elemzeslista)

           #print "elemzesek szama", len(elemzeslista)


           if (len(elemzeslista) != 1):
               print "elemzéslista:",
               for elemzes in elemzeslista:
                   #print elemzes,
                   lista.append(elemzes)
           else:
               print "elemzéslista: üres"
               lista.append(szo)
           print ""

        
        if (counter == startpos and endpos2 == endpos):
           print "megvan!!!"
           print "szó string:", szo, ", szó start:", counter, ", szó vége:" , counter + len(szo), ", szó hossza:", len(szo)
           if (len(elemzeslista) != 1):
               print "elemzés string:", elemzesek, ", start: ", counter, "hossz: ", len(elemzesek)
           else:
               print "elemzés string: nincs elemzés"

           elemzeslista = elemzesek.split('||')
           elemzesek = string.replace(elemzesek, '{{', '')
           elemzesek = string.replace(elemzesek, '}}', '')

           print "elemzések száma:", len(elemzeslista)

           #print "elemzesek szama", len(elemzeslista)


           if (len(elemzeslista) != 1):
               print "elemzéslista:",
               for elemzes in elemzeslista:
                   #print elemzes,
                   lista.append(elemzes)
           else:
               print "elemzéslista: üres"
               lista.append(szo)
           print ""

           
        #else:
            #print "nincs egyezés"
            #print "szó string:", szo, ", szó start:", counter, ", szó vége:" , counter + len(szo), ", szó hossza:", len(szo)
            #pass

        if (idx>=linesplit_len-3):
            kimenet = u'{0}/{1} token: {2}\n'.format(idx, linesplit_len, token.encode('utf8').encode('hex'))
            sys.stdout.write(kimenet + '\n')
        
        #új sornál
        counter += len(szo)
        counter += 1

f.close()

print lista
#print collection_str(lista)
