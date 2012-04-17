import fileinput
from time import sleep
import numpy as np
from cnc import to

def param_pos(p):
    return np.array([p['X'], p['Y'], p['Z']])

def steps(p):
    a = param_pos(p)
    if p['distmode'] == 'mm':
        return a * p['mmmul']
    else:
        return a * p['inmul']

def move(params):
    s = steps(params)
    p = params['pos']
    if params['posmode'] == 'abs':
        params['pos'] = to(p, s)
    else:
        params['pos'] = to(p, p + s)

def dwell(params):
    sleep(params['P'] / 1000.)

def set_inch(params):
    params['distmode'] = 'in'

def set_mm(params):
    params['distmode'] = 'mm'

def to_origin(params):
    p = params['pos']
    params['X'] = 0
    params['Y'] = 0
    params['Z'] = 0
    params['pos'] = to(p, np.array([0, 0, 0]))

def set_absolute(params):
    params['posmode'] = 'abs'

def set_relative(params):
    params['posmode'] = 'rel'

def set_home(params):
    params['pos'] = np.array([0, 0, 0])
    

commands = {
    0: move,
    1: move,
    4: dwell,
    20: set_inch,
    21: set_mm,
    28: to_origin,
    90: set_absolute,
    91: set_relative,
    92: set_home,
}

# 6000 =
# 187 mm
# 7.36 in
params = {
    'mmmul': 6000 / 187.,
    'inmul': 6000 / 7.36,
    'distmode': 'mm',
    'posmode': 'abs',
    'pos': np.array([0, 0, 0]), #x, y, z
}

def num (s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def interpret(line):
    words = line.split()
    for w in words:
        label = w[0]
        value = num(w[1:])
        params[label] = value

    try:
        cmd = commands[params['G']]
        cmd(params)
    except KeyError:
        pass

if __name__ == "__main__":
    print "intepreting gcode"
    for line in fileinput.input():
	print line
        interpret(line)
