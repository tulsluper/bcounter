#!/usr/bin/env python3

import os
import sys
import json
from datetime import datetime
from time import time
from itertools import chain, product
from multiprocessing import Pool
from pysnmp.entity.rfc3413.oneliner import cmdgen
from conf import DATA_DIR, TEMP_DIR, PROCESSES, CONNECTIONS, OIDS
from defs import load_data, dump_data


def snmpwalk(args, oids=OIDS):
    """
    perform snmpwalk command and return counters values;
    """
    system, address = args
    values = {}
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.nextCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget((address, 161)),
        *list(OIDS.keys()))
    if errorIndication:
        print(system, errorIndication)
    for varBind in varBinds:
        for oidnumport, value in varBind:
            items = oidnumport.prettyPrint().split('.')
            counter = oids.get('.'.join(items[:10]), '?')
            port = items[-1]
            value = int(value.prettyPrint(), 16)
            if value:
                values['%s %s %s' %(system, port, counter)] = value
    return system, values


def multisnmpwalk(oids, switches, processes):
    """
    run snmpwalk processes and concatenate results;
    """
    pool = Pool(processes=processes)
    acc = 0
    argsnum = len(switches)
    results = {}
    for system, result in pool.imap_unordered(snmpwalk, switches):
        acc +=1
        sys.stdout.write('Data collection progress: {}/{} {:<20}\r'.format(acc, argsnum, system))
        sys.stdout.flush()
        results.update(result)
    sys.stdout.write('Data collection finished: {}/{} {:<25}\n'.format(acc, argsnum, ''))

    return time(), results


def diffcalc(snmp_values, temp_values):
    """
    calculate differences between snmp values and temp values;
    """
    udiffs = {}
    for key, snmpvalue in snmp_values.items():
        tempvalue = temp_values.get(key, None)
        if tempvalue:
            counter = key.split()[2]
            diff = snmpvalue - tempvalue
        else:
            diff = -1 # error code 1
        if diff:
            udiffs[key] = diff
    return udiffs


def do_temp(snmp_values):
    """
    read data from temp file and rewrite new data;
    """
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    filepath = os.path.join(TEMP_DIR, 'values.json')
    temp_dt = os.path.getmtime(filepath) if os.path.exists(filepath) else None
    temp_values = load_data(filepath, {})
    dump_data(filepath, snmp_values)
    return temp_dt, temp_values


def safe_diffs(udiffs, snmp_dt, temp_dt):
    """
    save diffs;
    """
    
    delta = int(snmp_dt - temp_dt)
    dt1 = datetime.fromtimestamp(temp_dt).strftime('%Y-%m-%d.%H-%M-%S')
    dt2 = datetime.fromtimestamp(snmp_dt).strftime('%Y-%m-%d.%H-%M-%S')
    dt1date, dt1time = dt1.split('.')
    
    
    dt2date, dt2time = dt2.split('.')

    dirpath = os.path.join(DATA_DIR, dt1date)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    filename = '{}.{}.{}'.format(dt1time, dt2time, delta)
    filepath = os.path.join(dirpath, filename)
    with open(filepath, 'w') as f:
        json.dump(udiffs, f)
    return


def main():
    """
    main function
    """
    snmp_dt, snmp_values = multisnmpwalk(OIDS, CONNECTIONS, PROCESSES)
    temp_dt, temp_values = do_temp(snmp_values)
    if temp_dt:
        udiffs = diffcalc(snmp_values, temp_values)
        safe_diffs(udiffs, snmp_dt, temp_dt)
    return


if __name__ == '__main__':
    main()
