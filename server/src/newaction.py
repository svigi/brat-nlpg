#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:

from __future__ import with_statement

'''
Functionality related to external entity management.

Author:     Balázs Svigruha	<svigruha.balazs@hallgato.ppke.hu>
Version:    2012-07-09
'''
from config import DATA_DIR
#DATA_DIR = '/home/sviba/brat/brat-v1.2_The_Larch/data/'

from logging import info as log_info
from codecs import open as codecs_open
from functools import partial
from itertools import chain
from os import utime
from time import time
from os.path import join as path_join
from os.path import basename, splitext

from common import ProtocolError
from filelock import file_lock
from message import Messager

from pysqlite2 import dbapi2 as sqlite

import simplejson as json

import sys
import os
import codecs
import re
import string
import unicodedata


def collection_str(collection):
    if isinstance(collection, list):
        brackets = '[%s]'
        single_add = ''
    elif isinstance(collection, tuple):
        brackets = '(%s)'
        single_add =','
    else:
        return str(collection)
    items = ', '.join([collection_str(x) for x in collection])
    if len(collection) == 1:
        items += single_add
    return brackets % items


class Wordentity(object):
    def __init__(self, word=None, order=None):
        self.word = word
        self.order = order

def encode_list(lista):
    outstr = ''
    for idx in range(len(lista)):
        outstr += lista[idx]
        if (idx != len(lista)-1):
            outstr += '||'
        
    return outstr

def encode_entity(szo, lista):
    outstr = szo
    if (len(lista)!=0):
        outstr += '{{' + encode_list(lista) + '}}'
    
    return outstr

def save_list_to_file(start, end, docname, lista):
    separator = ' '
    response = {}
    startpos = int(start)
    endpos = int(end)
    szo = ''
    line_out = ''
    log_info(type(startpos))
    log_info(startpos)
    log_info(type(endpos))
    log_info(endpos)
    utvonal = path_join(DATA_DIR, docname + '.dat')
    utvonaluj = path_join(DATA_DIR, docname + '.tmp')
    
    
    log_info('opening file: ' + utvonal)
    file_in = codecs.open(utvonal, 'r', 'utf8')
    log_info('file opened')

    log_info('opening file: ' + utvonaluj)
    file_out = codecs.open(utvonaluj, 'w', 'utf8')
    log_info('file opened for writing')

    counter = int(1)
    
    for line in file_in:
        counter -= 1
        linesplit = line.split(' ')
        pattern = r'^([^{|]+)(.+)'
    
        for idx in range(len(linesplit)):
            line_out = ''
            token = linesplit[idx]
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
                elemzesek = ''
                    
            #log_info(szo)
            #print "ellenorzes"
            szohossz = len(szo)
            endpos2 = counter + szohossz
            #print "startpos", startpos, "endpos", endpos, "counters", counter, endpos2
            #if (counter == startpos):
            
            #sys.stdout.write("token: ")
            #sys.stdout.write(token)
            #sys.stdout.write('\n')
            #sys.stdout.write('szo: ')
            #sys.stdout.write(szo)
            #sys.stdout.write('\n')
            #sys.stdout.write('elemzes: ')
            #sys.stdout.write(elemzesek)
            #sys.stdout.write('\n')
            

            if (counter == startpos and endpos2 == endpos):
                encoded_list = encode_entity(szo, lista)
                line_out += encoded_list
                #sys.stdout.write('újrakódolt: ')
                #sys.stdout.write(encoded_list)
                #sys.stdout.write('\n')
                
                
            else:
                line_out = token
                #sys.stdout.write('átmásolt: ')
                #sys.stdout.write(token)
                #sys.stdout.write('\n')
            
            #sor végére ne rakjon be még egy szeparátort
            if (idx != len(linesplit)-1):
                line_out += separator
             
            counter += len(szo)
            counter += 1
            
            #sys.stdout.write(line_out)
            
            #sys.stdout.write('fájlba: ')
            #sys.stdout.write(line_out)
            #sys.stdout.write('\n')
            #sys.stdout.write('\n')
            file_out.write(line_out)
            #soron belüli for vége 
        
        #új sor kiírása
        #külön nem kell, azt is átmásolja
        #soronkénti for vége
        
    file_in.close()
    log_info('infile closed')
    file_out.flush()
    file_out.close()
    log_info('outfile closed')
    os.rename(utvonaluj, utvonal)
    log_info('file renamed')

    
    return response

        
def read_list_from_file(start, end, docname):
    
    #startpos = int(start)
    #endpos = int(end)
    
    #startpos = int(start.encode('ascii'))
    #endpos = int(end.encode('ascii'))
    
    startpos = int(start)
    endpos = int(end)
    szo = ''
    log_info(type(startpos))
    log_info(startpos)
    log_info(type(endpos))
    log_info(endpos)
    
    utvonal = path_join(DATA_DIR, docname + '.dat')
    
    log_info('opening file: ' + utvonal)
    f = codecs.open(utvonal, 'r', 'utf8')
    log_info('file opened')
    lista = []

    counter = int(1)
    for line in f:
        #log_info('sor olvasva')
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
    
            #log_info(szo)
            #print "ellenorzes"
            szohossz = len(szo)
            endpos2 = counter + szohossz
            #print "startpos", startpos, "endpos", endpos, "counters", counter, endpos2
            #if (counter == startpos):
            
            
            if (counter == startpos and endpos2 == endpos):
               #print "megvan!!!"
               #print "szó string:", szo, ", szó start:", counter, ", szó vége:" , counter + len(szo), ", szó hossza:", len(szo)
               #if (len(elemzeslista) != 1):
                   #print "elemzés string:", elemzesek, ", start: ", counter, "hossz: ", len(elemzesek)
               #else:
                   #print "elemzés string: nincs elemzés"
    
               elemzeslista = elemzesek.split('||')
               elemzesek = string.replace(elemzesek, '{{', '')
               elemzesek = string.replace(elemzesek, '}}', '')
    
               #print "elemzések száma:", len(elemzeslista)
    
    
               if (len(elemzeslista) != 1):
                   #print "elemzéslista:",
                   for elemzes in elemzeslista:
                       #print elemzes,
                       lista.append(elemzes)
                       log_info(elemzes)
               else:
                       lista.append(szo)
                       log_info(szo)
                   #print "elemzéslista: üres"
               #print ""
    
               
            else:
                #print "nincs egyezés"
                #print "szó string:", szo, ", szó start:", counter, ", szó vége:" , counter + len(szo), ", szó hossza:", len(szo)
                pass
    
            
            #új sornál
            counter += len(szo)
            counter += 1
        
    log_info('file closed')
    f.close()
    
    if (len(lista)==0):
        if (szo != '\n'):
            lista.append(szo)
            log_info('nincs elemzés')
            log_info(szo)

    return lista

def get_entities(start, end, docname):
    response = {}
    response['test'] = 'Választ kaptam a szervertől'
    lista = read_list_from_file(start, end, docname)
    #collstr = collection_str(lista)
    #log_info(collstr)
    response['entities'] = lista
    return response

def set_entities(start, end, docname, words):
    log_info('set_entities start')
    lista = json.JSONDecoder().decode(words)
    log_info('lista_len')
    log_info(len(lista))
    response = {}
    #lista = []
    #lista.append('egyik')
    #lista.append('másik')
    response['test'] = 'Választ kaptam a szervertől'
    save_list_to_file(start, end, docname, lista)
    log_info('saved')
    return response
    
def get_entitiesold(start, end):
    response = {}
    response['test'] = 'Választ kaptam a szervertől';
    lista = []
    conn = sqlite.connect('/home/sviba/test.db')
#    try:        
#        conn = sqlite.connect('test.db')
        
#    except sqlite.OperationalError:
#        #Messager.error(msg) 
#        response['test'] = os.path.dirname(__file__)
#        return response
        
        
    # memoryConnection = sqlite.connect(':memory:')
    cur = conn.cursor()
    #cursor.execute('CREATE TABLE names (id INTEGER PRIMARY KEY, name VARCHAR(50), email VARCHAR(50))')
    #cursor.execute('INSERT INTO names VALUES (null, "John Doe", "jdoe@jdoe.zz")')
    #cursor.execute('INSERT INTO names VALUES (null, "Mary Sue", "msue@msue.yy")')
    #print "last row id: {0}".format(cursor.lastrowid)
    #name = "Luke Skywalker"
    #email ="use@the.force"
    #cursor.execute('INSERT INTO names VALUES (null, ?, ?)', (name, email))
    #connection.commit()
    
    cur.execute('SELECT * from names')
    
    row = cur.fetchone()
    while row is not None:
        lista2 = []
        lista2.append(row[0])
        lista2.append(row[1])
        #lista.append('bejegyzes')
        lista.append(lista2)
        row = cur.fetchone()
       
    cur.close()
    conn.close()
        #w = Wordentity('alma', 1)

    #print w.word
    #lista.append(Wordentity('alma', '1'));
#    lista.append('alma')
#    lista.append('körte')
#    lista.append(1)
    response['entities'] = lista;
    # + value;
    return response

def new_action(value):
    response = {}
    response['test'] = 'Válasz a szervertől';
    lista = []

    w = Wordentity('alma', 1)
    lista2 = []
    lista2.append(w.word)
    lista2.append(w.order)
    lista.append(lista2)
    #print w.word
    #lista.append(Wordentity('alma', '1'));
#    lista.append('alma')
#    lista.append('körte')
#    lista.append(1)
    response['entities'] = lista;
    # + value;
    return response


if __name__ == '__main__':
    #TODO: Unit-testing
    pass

#teszt
#start 16
#end 31
#INFO:root:szemhéjtoilette
#INFO:root:dzemhéjtoilette
#INFO:root:hszemhéjtoilette
#INFO:root:szemhéjnoilette
#INFO:root:szemhéqjtoilette
#INFO:root:szemséjtoilette
#INFO:root:szemhéjtowilette
#INFO:root:szemhéjtoitlette
#INFO:root:szemhéjtoilettde
#INFO:root:szeómhéjtoilette
#testlist = []

#testlist.append('újszó')
#testlist.append('dzemhéjtoilette')
#testlist.append('szemhéjtoilettemássorrend')
#testlist.append('szemhéjtoilette')
#testlist.append('dzemhéjtoilette')
#testlist.append('hszemhéjtoilette')
#testlist.append('szemhéjnoilette')
#testlist.append('szemhéqjtoilette')
#testlist.append('szemséjtoilette')
#testlist.append('szemhéjtowilette')
#testlist.append('szemhéjtoitlette')
#testlist.append('szemhéjtoilettde')
#testlist.append('szeómhéjtoilette')

#ureslista = []
#print "calling"
#save_list_to_file(16, 31, 'szemeszet', ureslista)
#print "called"

#set_entities(u'5', u'13', u'szemeszet', u'["egyik","m\xe1sik"]')
