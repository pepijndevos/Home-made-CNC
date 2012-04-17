import parallel
from time import sleep
import numpy as np

X = 1
Y = 2
Z = 4
prf = 64
strobe = 128

p = parallel.Parallel()

def direction(m):
    p.setData(m)
    p.setData(m+strobe)
    p.setData(m)

def step(m):
    p.setData(m)
    p.setData(m+prf)

def to_byte(a):
    shifts = np.arange(a.size)
    shifted = np.left_shift(np.abs(a.astype('int')), shifts)
    return np.sum(shifted)

def line(p1, p2):
    pp = p1.astype('float') 
    p = p1.astype('float')
    d = p2 - p1
    N = np.max(np.abs(d))
    s = d.astype('float') / N
    for i in range(int(N)):
        p += s
        r = np.round(p)
        yield to_byte(r - pp)
        pp = r

def get_dir(pos, p):
    dir = 0
    for i, d in enumerate(p-pos):
        if d > 0:
            dir += 1<<i
    return dir    

def to(pos, p):
    direction(get_dir(pos, p))
    l = line(pos, p)
    for s in l:
        step(s)
        sleep(0.003)

    return p

def arc(p, c):
    pass

if __name__ == "__main__":
    pos = np.array([0, 0, 0]) #x, y, z
    pos = to(pos, np.array([1000,0,0]))
    pos = to(pos, np.array([1000,0,200]))
    pos = to(pos, np.array([6000,3500,200]))
    pos = to(pos, np.array([0,3500,200]))
    pos = to(pos, np.array([5000,0,200]))
    pos = to(pos, np.array([3000,5000,200]))
    pos = to(pos, np.array([1000,0,200]))
    pos = to(pos, np.array([1000,0,0]))
    pos = to(pos, np.array([0,0,0]))
