# color palette for walls
COLORS = ['aqua','aquamarine','azure','beige','bisque','black','blanchedalmond','blue','blueviolet','brown']

def frange(start, stop, step):
    while start < stop:
        # print(start)
        yield start
        start += step

def index2d(data, char):
    for x in range(len(data)):
        for y in range(len(data[0])):
            if data[x][y] == char:
                return x,y
    return -1,-1


