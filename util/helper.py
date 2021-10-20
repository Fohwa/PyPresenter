import os

def setResolution(res):
    f = open(os.path.join('config', 'resolution.dat'), "w")
    f.write(res)
    f.close()