#!/usr/bin/python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:

import codecs
import re
import string
import sys

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
print "startpos", startpos
print "endpos", endpos

#line = f.readline()
lista = []

for line in f:
    #sor végi LF karaktert ne számoljuk!
    counter -= 1
    linesplit = line.split(' ')
    pattern = r'^([^{|]+)(.+)'

    for token in linesplit:
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
        print "startpos", startpos, "endpos", endpos, "counters", counter, endpos2
        
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

        
        #új sornál
        counter += len(szo)
        counter += 1

f.close()

print collection_str(lista)

