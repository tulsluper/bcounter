# ==============================================================================

import json

def load_data(filepath, default=None):
    try:
        with open(filepath) as f:
            return json.load(f)
    except:
        return default


def dump_data(filepath, data):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f)
        return True
    except:
        return False

# ==============================================================================

from math import log10, floor

def round_to_1(value):
    if 0 < value < 1:
        return round(value, -int(floor(log10(value))))
    else:
        return int(value)

# ==============================================================================
