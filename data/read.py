#!/usr/bin/python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:


import codecs
import re
import string
counter = 1
f = codecs.open('szemeszet.dat','r','utf8')

#line = f.readline()
for line in f:
    #sor végi LF karakter!
    counter -= 1
    linesplit = line.split(' ')
    pattern = r'^([^{|]+)(.+)'

    for token in linesplit:
        szo = re.sub(pattern, r'\1', token)
        elemzesek = re.sub(pattern, r'\2', token)

        elemzesek = string.replace(elemzesek, '{{', '')
        elemzesek = string.replace(elemzesek, '}}', '')
        elemzeslista = elemzesek.split('||')

        if (len(elemzeslista) == 1):
            if (szo != elemzesek):
                szo += elemzesek

        print "szó string:", szo, ", szó start:", counter, ", szó vége:" , counter+len(szo), ", szó hossza:", len(szo)
           
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
                print elemzes,
        else:
            print "elemzéslista: üres"
        print ""
        print ""

        #print "új szóhossz:", len(szo)
        counter += len(szo)
        counter += 1

f.close()

 
