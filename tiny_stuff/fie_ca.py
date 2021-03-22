#!/usr/bin/env python

import random

FIE_CA = 'Fie ca'
SPATIU = ' '
SI = 'si'
VIRGULA = ','
SA_VA_ADUCA = 'sa va aduca'
FINAL = 'Sarbatori fericite!'

CINE = [
    'frumusetea iernii',
    'Mos Craciun',
    'nasterea Domnului',
    'cei trei crai',
    'steaua care a rasarit',
    'sarbatorile de iarna'
]
CE = [
    'sanatate',
    'fericire',
    'implinirea tuturor dorintelor',
    'pace',
    'intelepciune',
    'bucurie in viata'
]

nr_cine = random.randint(1,CINE.__len__())
sample_cine = random.sample(CINE, nr_cine)
nr_ce = random.randint(1,6)
sample_ce = random.sample(CE, nr_ce)

result = FIE_CA + SPATIU
for index, cine in enumerate(sample_cine):
    result = result + cine
    if (index == sample_cine.__len__()-2):
        result = result  + SPATIU+ SI + SPATIU
    elif (index == sample_cine.__len__() - 1):
        result = result + SPATIU
    else:
        result = result + VIRGULA + SPATIU

result = result + SA_VA_ADUCA + SPATIU

for index, ce in enumerate(sample_ce):
    result = result + ce
    if (index == sample_ce.__len__()-2):
        result = result + SPATIU + SI + SPATIU
    elif (index == sample_ce.__len__() -1):
        result = result
    else:
        result = result + VIRGULA + SPATIU

result = result + '!' + SPATIU + FINAL

print result
