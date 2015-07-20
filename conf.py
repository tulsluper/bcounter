"""
config file for bcounters scripts
"""

import os


PROCESSES = 4 # number of processes for multiprocessing

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
TEMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp'))

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'bcounters'

CONNECTIONS = (
  # ('switch name', 'switch address'),
)

OIDS = {
  # OIDs are described in Fabric OS MIB Reference
  # 'oid number': 'counter name',
    '1.3.6.1.3.94.4.5.1.3':  'Error',
    '1.3.6.1.3.94.4.5.1.4':  'TxObjects',
    '1.3.6.1.3.94.4.5.1.5':  'RxObjects',
    '1.3.6.1.3.94.4.5.1.6':  'TxElements',
    '1.3.6.1.3.94.4.5.1.7':  'RxElements',
    '1.3.6.1.3.94.4.5.1.8':  'BBCreditZero',
    '1.3.6.1.3.94.4.5.1.20': 'Class2RxFrames',
    '1.3.6.1.3.94.4.5.1.26': 'Class3RxFrames',
    '1.3.6.1.3.94.4.5.1.28': 'Class3Discards',
    '1.3.6.1.3.94.4.5.1.29': 'RxMulticastObjects',
    '1.3.6.1.3.94.4.5.1.30': 'TxMulticastObjects',
    '1.3.6.1.3.94.4.5.1.33': 'RxLinkResets',
    '1.3.6.1.3.94.4.5.1.34': 'TxLinkResets',
    '1.3.6.1.3.94.4.5.1.36': 'RxOfflineSequences',
    '1.3.6.1.3.94.4.5.1.37': 'TxOfflineSequences',
    '1.3.6.1.3.94.4.5.1.39': 'LinkFailures',
    '1.3.6.1.3.94.4.5.1.40': 'InvalidCRC',
    '1.3.6.1.3.94.4.5.1.41': 'InvalidTxWords',
    '1.3.6.1.3.94.4.5.1.42': 'PrimitiveSequenceProtocolErrors',
    '1.3.6.1.3.94.4.5.1.43': 'LossofSignal',
    '1.3.6.1.3.94.4.5.1.44': 'LossofSynchronization',
    '1.3.6.1.3.94.4.5.1.45': 'InvalidOrderedSets',
    '1.3.6.1.3.94.4.5.1.46': 'FramesTooLong',
    '1.3.6.1.3.94.4.5.1.47': 'FramesTruncated',
    '1.3.6.1.3.94.4.5.1.48': 'AddressErrors',
    '1.3.6.1.3.94.4.5.1.49': 'DelimiterErrors',
    '1.3.6.1.3.94.4.5.1.50': 'EncodingDisparityErrors',
}

SCALES = {
    'pcs': 1,
    'T': 1000,
    'M': 1000000,
    'MB': 1048576,
    'TB': 1073741824,
}

INTEGERS = {
    's': {
        'Error': 'pcs/s',
        'TxObjects': 'M/s',
        'RxObjects': 'M/s',
        'TxElements': 'TB/s',
        'RxElements': 'TB/s',
        'BBCreditZero': 'M/s',
        'Class3RxFrames': 'M/s',
    },
    'p': {
        'Error': 'pcs/s',
        'TxObjects': 'T/s',
        'RxObjects': 'T/s',
        'TxElements': 'MB/s',
        'RxElements': 'MB/s',
        'BBCreditZero': 'pcs/s',
        'Class3RxFrames': 'T/s',
    }
}
