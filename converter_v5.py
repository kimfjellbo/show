'''
Example input:
zzz    123
length   :  100
width   : 50

zzz    322
length   :  300
width   : 440
etc...

Example output:
zzz;length;width
123;100;50
322;300;440
'''



#!/usr/bin/python3
import sys
import re
import csv

if len(sys.argv) < 2:
    sys.exit("Need 2 arguments, zzz.py {file}")
else:
    file1 = sys.argv[1]
    file2 = sys.argv[2]

zzzLines = []
dic = dict()
dicTable = dict()

splitChar = "|X|"

with open(file1, 'r') as zzz_all_zzz:
    lineNumber = 1
    for line in zzz_all_zzz:
        dic[lineNumber] = line.strip()
        job = re.search('(ZZZ)',line)
        if job:
            zzzLines.append(lineNumber)
        lineNumber = lineNumber + 1

# generic method to check if the index in a array exist

def checkNext(arr,number):
    try:
        arr[number]
        return True
    except:
        return False

# Create dictionary with the splitChar between the values

for iter in range (1,len(zzzLines)):
    if ( checkNext(zzzLines,1) ):
        temp1 = zzzLines[0]
        temp2 = zzzLines[1]
        zzzLines.pop(0)
        appendLines = []
        for n in range(temp1,temp2):
            appendLines.append(dic[n])
        string = splitChar.join(appendLines)
        dicTable[iter] = string


# splitSplit() that returns the zzz name and value and tests

def splitSplit(text, splitChar, textSearch):
    splitted = text.split(splitChar)
    attr = ""
    val = ""
    for valueSplitted in splitted:
        if ( re.search('(zzz)',textSearch) ):
            attr = valueSplitted[0:19].strip()
            val = valueSplitted[19:len(valueSplitted)].strip()
            break
        
        indexColumnInText = valueSplitted.strip().find(":")
        attributeName = valueSplitted.strip()[0:indexColumnInText]
        value = valueSplitted.strip()[indexColumnInText+1:len(valueSplitted)]
        if( attributeName.strip() == textSearch.strip() ):
            attr = attributeName.strip()
            val = value.strip()
            break
    return attr, val


def setAllAttributesAndValues(fileout):
    arr = dict()
    with open(f"{fileout}", 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = [
            'zzz',
            'length',
            'width',
            ]
        csvWriter = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
        csvWriter.writeheader()
        for iter in dicTable:
            lineSplit = dicTable[iter].split(splitChar)
            ATTRIBUTES_job = re.search('(zzz)',lineSplit[0])
            if( ATTRIBUTES_job ):
                zzz = splitSplit(dicTable[iter], splitChar, "zzz")[1]
                length = splitSplit(dicTable[iter], splitChar, "length")[1]
                width = splitSplit(dicTable[iter], splitChar, "width")[1]
                csvWriter.writerow(
                    {
                    'zzz':zzz,
                    'length':length,
                    'width':width
                    }
                    )

setAllAttributesAndValues(file2)



'''
TEST method splitSplit

https://www.online-python.com/

import re

dicTable = {1:"zzz    123|X|length   :  100|X|width   : 440"}

def splitSplit(text, splitChar, textSearch):
    splitted = text.split(splitChar)
    attr = ""
    val = ""
    for valueSplitted in splitted:
        if ( re.search('(zzz)',textSearch) ):
            attr = valueSplitted[0:19].strip()
            val = valueSplitted[19:len(valueSplitted)].strip()
            break
        
        indexColumnInText = valueSplitted.strip().find(":")
        attributeName = valueSplitted.strip()[0:indexColumnInText]
        value = valueSplitted.strip()[indexColumnInText+1:len(valueSplitted)]
        if( attributeName.strip() == textSearch.strip() ):
            attr = attributeName.strip()
            val = value.strip()
            break
    return attr, val


#print(dicTable[1])

for iter in dicTable:
    zzz_val = splitSplit(dicTable[iter], "|X|", "length")[1]
    zzz_atr = splitSplit(dicTable[iter], "|X|", "length")[0]


print(f"attribute {zzz_atr} has the value {zzz_val}")

============================
console output:

attribute length has the value 100


** Process exited - Return Code: 0 **
Press Enter to exit terminal

'''
