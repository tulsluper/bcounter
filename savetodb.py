#!/usr/bin/env python3

import os
import sys
import json
from collections import defaultdict
from pymongo import MongoClient
from datetime import datetime
from conf import DATA_DIR, SCALES, INTEGERS
from conf import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME
from defs import load_data, round_to_1


def check_and_fix(uid, value):
    counter = uid.split()[-1]
    if counter in ['BBCreditZero', 'Error', 'InvalidOrderedSets'] and value > 2*10**9:
        value = -2 # error code 2
    return value


def to_scale(values, deltas, counter, itype):
    if counter in INTEGERS[itype]:
        integer = INTEGERS[itype][counter]
        scale = SCALES[integer.split('/')[0]]
        newvalues = []
        for value, delta in zip(values, deltas):
            if value <= 0:
                newvalues.append(value)
            else:
                delta = 1 if integer[-1] == 'd' else delta
                newvalues.append(round_to_1(value/delta/scale))
        return newvalues
    else:
        return values


def sum_udiffs(dirpath):
    udiffs, xtimes, deltas = {}, [], []
    filenames = os.listdir(dirpath)
    zeros = [0 for _ in filenames]
    for num, filename in enumerate(sorted(filenames)):
        _, xtime, delta = filename.split('.')
        xtimes.append(xtime.split('-'))
        deltas.append(int(delta))        
        filepath = os.path.join(dirpath, filename)
        data = load_data(filepath, {})
        for uid, value in data.items():
            if not uid in udiffs:
                udiffs[uid] = zeros[:]
            value = check_and_fix(uid, value)
            udiffs[uid][num] = value
    return udiffs, xtimes, deltas


def calc_dicts(udiffs, deltas):
    cdicts = defaultdict(dict)
    pdicts = defaultdict(dict)
    sdicts = {}
    for uid, values in udiffs.items():
        swport, counter = uid.rsplit(' ', 1)
        if not counter in sdicts:
            sdicts[counter] = [0 for _ in deltas]
        if sum(values):
            sdicts[counter] = [x+y if y>0 else x for x,y in zip(sdicts[counter], values)]
            values = to_scale(values, deltas, counter, 'p')
            cdicts[counter][swport] = values
            pdicts[swport][counter] = values
    for counter, values in sdicts.items():
        sdicts[counter] = to_scale(values, deltas, counter, 's')
    return cdicts, pdicts, sdicts


def main():

    if len(sys.argv) > 1:
        datestring = sys.argv[1]
    else:
        datestring = datetime.now().strftime('%Y-%m-%d') 

    dirpath = os.path.join(DATA_DIR, datestring)

    if not os.path.exists(dirpath):
        print('No data for %s' %datestring)
        sys.exit()

    udiffs, xtimes, deltas = sum_udiffs(dirpath)
    cdicts, pdicts, sdicts = calc_dicts(udiffs, deltas)

    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DBNAME]
    db.xtimes.update({datestring: {'$exists': True}}, {datestring: xtimes}, True)
    db.deltas.update({datestring: {'$exists': True}}, {datestring: deltas}, True)
    db.cdicts.update({datestring: {'$exists': True}}, {datestring: cdicts}, True)
    db.pdicts.update({datestring: {'$exists': True}}, {datestring: pdicts}, True)
    db.sdicts.update({datestring: {'$exists': True}}, {datestring: sdicts}, True)
    db.integers.update({datestring: {'$exists': True}}, {datestring: INTEGERS}, True)

    print(xtimes, deltas)

    client.close()


if __name__ == '__main__':
    main()
