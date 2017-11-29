# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 19:17:05 2017

@author: Sony
"""

def read_GolfData():
    file = open("GolfDataSet.txt", 'r')
    text = file.read()
    data = []
    file.close()
    ligne = text.split('data ')
    ligne = ligne[1]
    ligne = ligne.split()
    for seq in ligne:
        datarow = seq.split(',')
        classe = datarow.pop(len(datarow)-1)
        datarow.insert(0,classe)
        data.append(datarow)
        
    attributes = {}
    order_attribs = []
    atts = text.split(' @attribute ')
    last = atts.pop(len(atts)-1)
    last = last.split(' @data')
    last = last[0]
    atts.append(last)
    atts = atts[1:]
    for attrib in atts :
        key = (attrib.split())[0]
        order_attribs.append(key)
        if key == 'play' :
            key = key + '_CLASS'
        features = ((attrib.split(' {')[1]).split('}')[0]).split(', ')
        attributes[key] = features
        
    return data, attributes, order_attribs

def read_SoybeanData():
    file = open("SoybeanDataSet.txt", 'r')
    text = file.read()
    data = []
    attributes = {}
    order_attribs = []
    file.close()
    begin = False
    text = text.split('\n')
    for line in text :
        if '@ATTRIBUTE' in line and not 'class' in line :
            order_attribs.append(line.split()[1])
            line = (line.split())[2:]
            line = line[0].split('{')[1]
            line = line.split('}')[0]
            attributes[order_attribs[len(order_attribs) - 1]] = line.split(',')
        if '@ATTRIBUTE' in line and 'class' in line :
            order_attribs.append(line.split()[1])
            line = (line.split())[2:]
            line = [line[i].rstrip(',') for i in range(len(line))]
            line = [line[i].rstrip('}') for i in range(len(line))]
            line = [line[i].strip('{') for i in range(len(line))]
            attributes[order_attribs[len(order_attribs) - 1] + '_CLASS'] = line
            
        if line == '@DATA' :
            begin = True
        if begin :
            if line == '' or '?' in line:
                continue
            line = line.split(', ')
            data.append(line)
    for datarow in data:
        classe = datarow.pop(len(datarow)-1)
        datarow.insert(0,classe)

    return data[1:len(data)-1], attributes, order_attribs

#a,b,c = read_SoybeanData()
#print('2-4-d-injury' in a)