'''

'''


# Works with Python 3.9.6
import sys
import codecs
import re
import string

arg1_rec1 = sys.argv[1]
arg2_pops = sys.argv[2]

print("command argument 1 is: "+arg1_rec1)
print("command argument 2 is: "+arg2_pops)

regexValues = {"rec1File": '(\d{5}\w+\s{0,1}-{0,1}\w+)', "postnumber": '(\d{5})', "address": '(\D+\w+\s{0,1}\w+)'}

# read and parse the pops file

filePostnumberPops = codecs.open(arg2_pops, mode='r', encoding='utf-8', errors='strict')

zzzdbArray = []
for line in filePostnumberPops.readlines():
    zzzdbArray.append(line.strip().upper())

distinctList1 = set(zzzdbArray)

# read and parse the sweden postnumber file

filePostnumberSweden = codecs.open(arg1_rec1, mode='r', encoding='utf-8', errors='strict')

postnumberrec1File = []
for line in filePostnumberSweden.readlines():
    regularexp = re.search(regexValues["rec1File"], line)
    postnumberrec1File.append(regularexp.group(1).upper())

distinctList2 = set(postnumberrec1File)

# find differences

missingPostnumbersInPops = distinctList2 - distinctList1
obsoletePostnumbersInPops = distinctList1 - distinctList2

for val in missingPostnumbersInPops:
    postnumber = re.search(regexValues["postnumber"], val)
    address = re.search(regexValues["address"], val)
    try:
        temp = string.Template('INSERT INTO TPostNumber(PostNumber_Number, PostNumber_Name, PostNumber_Country) values (\'$postnumber\',\'$address\',\'SE\')')
        insertIntoSQL = temp.substitute(postnumber=postnumber.group(1), address=address.group(1))
        print(insertIntoSQL)
    except AttributeError:
        temp = string.Template('The value "$val" cannot be parsed with regex "$regExPostnumber" and/or $regExAdress')
        print(temp.substitute(val=val, regExPostnumber=regexValues["postnumber"], regExAdress=regexValues["address"]))

for val in obsoletePostnumbersInPops:
    postnumber = re.search(regexValues["postnumber"], val)
    try:
        temp = string.Template('SELECT PostNumber_Id,PostNumber_Number,PostNumber_Name FROM TPostNumber with(nolock) WHERE PostNumber_Number = \'$postnumber\' and PostNumber_Country = \'SE\'')
        selectSQL = temp.substitute(postnumber=postnumber.group(1))
        print(selectSQL)
    except AttributeError:
        temp = string.Template('The value "$val" cannot be parsed with regex "$regExPostnumber"')
        print(temp.substitute(val=val, regExPostnumber=regexValues["postnumber"]))
