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
