import random, math

qwerty = [192, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 189, 187, 8,
            9, 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 219, 221, 220,
            65, 83, 68, 70, 71, 72, 74, 75, 76, 186, 222, 13,
            90, 88, 67, 86, 66, 78, 77, 190, 188, 190, 32]

toCode = {0: 192, 1: 49, 2: 50, 3: 51, 4: 52, 5: 53, 6: 54, 7: 55, 8: 56, 9: 57, 10: 48, 11: 189, 12: 187, 13: 8, 14: 9, 15: 81, 
    16: 87, 17: 69, 18: 82, 19: 84, 20: 89, 21: 85, 22: 73, 23: 79, 24: 80, 25: 219, 26: 221, 27: 220, 28: 65, 29: 83, 30: 68, 
    31: 70, 32: 71, 33: 72, 34: 74, 35: 75, 36: 76, 37: 186, 38: 222, 39: 13, 40: 90, 41: 88, 42: 67, 43: 86, 44: 66, 45: 78, 
    46: 77, 47: 190, 48: 188, 49: 190, 50: 32}

toIndex = {8: 13, 9: 14, 13: 39, 32: 50, 48: 10, 49: 1, 50: 2, 51: 3, 52: 4, 53: 5, 54: 6, 55: 7, 56: 8, 57: 9, 186: 37, 187: 12, 
    188: 48, 189: 11, 190: 49, 192: 0, 65: 28, 66: 44, 67: 42, 68: 30, 69: 17, 70: 31, 71: 32, 72: 33, 73: 22, 74: 34, 75: 35, 76: 36, 
    77: 46, 78: 45, 79: 23, 80: 24, 81: 15, 82: 18, 83: 29, 84: 19, 85: 21, 86: 43, 87: 16, 88: 41, 89: 20, 90: 40, 219: 25, 
    220: 27, 221: 26, 222: 38}


def layout():
    return random.sample(range(51), 51)

def create_pool(size):
    pool = []
    #check to make sure each layout is unique!!
    for i in range(size):
        pool.append(layout())
    return pool

key_lhf = {
    0:[0, 0, 0, 0], 1:[0, 1, 0, 0], 2:[0, 2, 0, 1], 3:[0, 3, 0, 2], 4:[0, 4, 0, 3], 5:[0, 5, 0, 3], 
    6: [0, 6, 1, 3], 7:[0, 7, 1, 3], 8:[0, 8, 1, 2], 9:[0, 9, 1, 1], 10:[0, 10, 1, 0], 11:[0, 11, 1, 0], 12:[0, 12, 1, 0], 13:[0, 13, 1, 0], 

    14:[1, 0, 0, 0], 15:[1, 1, 0, 0], 16:[1, 2, 0, 1], 17:[1, 3, 0, 2], 18:[1, 4, 0, 3], 19:[1, 5, 0, 3], 
    20:[1, 6, 1, 3], 21:[1, 7, 1, 3], 22:[1, 8, 1, 2], 23:[1, 9, 1, 1], 24:[1, 10, 1, 0], 25:[1, 11, 1, 0], 26:[1, 12, 1, 0], 27:[1, 13, 1, 0], 

    28:[2, 0, 0, 0], 29:[2, 1, 0, 0], 30:[2, 2, 0, 1], 31:[2, 3, 0, 2], 32:[2, 4, 0, 3], 33:[2, 5, 0, 3], 
    34:[2, 6, 1, 3], 35:[2, 7, 1, 3], 36:[2, 8, 1, 2], 37:[2, 9, 1, 1], 38:[2, 10, 1, 0], 39:[2, 11, 1, 0], 

    40:[3, 1, 0, 0], 41:[3, 2, 0, 1], 42:[3, 3, 0, 2], 43:[3, 4, 0, 3], 44:[3, 5, 0, 3], 
    45:[3, 6, 1, 3], 46:[3, 7, 1, 3], 47:[3, 8, 1, 2], 48:[3, 9, 1, 1], 49:[3, 10, 1, 0], 

    50: [4, 3, 2, 0]}

def distance(l, freq):
    distance = 0
    length = 1.8
    homerow = [[29, 30, 31, 32], [38, 37, 36, 35], [50]]
    
    for i in range(len(freq)):
        w = (1 + i)
        if freq[i] != 16 and freq[i] != 191:
            krow, kcol, kh, kf = key_lhf[l.index(toIndex[freq[i]])]
            hrow, hcol, hh, hf = key_lhf[homerow[kh][kf]]

            if hrow == krow and hcol == kcol:
                diff = 0
            elif hrow == krow:
                diff = abs(hcol - kcol)
            elif hcol == kcol:
                diff = abs(hrow - krow)
            else:
                a = abs(hrow - krow)
                b = abs(hcol - kcol)
                diff = math.sqrt((a**2) + (b**2))
 
            distance += ((length * diff)/float(w))

    return distance

def hfmCost(h, f, m, bigrams, l):
    cost = 0
    for bigram in bigrams:
        k1 = l.index(toIndex[bigram[0]])
        k2 = l.index(toIndex[bigram[1]])

        row1, col1, h1, f1 = key_lhf[k1]
        row2, col2, h2, f2 = key_lhf[k2]

        if h == 0:
            if h1 != h2:
                cost += 0.33
        else:
            if h1 == h2:
                cost += 0.33

        if f == 0:
            if f1 != f2:
                cost += 0.33
        else:
            if f1 == f2:
                cost += 0.33

        if m == 0:
            if row1 != row2:
                cost += 0.33
        elif m == 1:
            if col1 != col2:
                cost += 0.33
        else: 
            if row1 == row2 and col1 == col2:
                cost += 0.33
    return (cost/len(l))

def findDiff(b, l):
    diff = 0
    length = 1.8
    distance = 0

    for i in range(len(qwerty)):
        qrow, qcol, qh, qf = key_lhf[i]
        for h in l:
            if i == h:
                row, col, h, f = key_lhf[l.index(h)]
        if row == qrow and col == qcol:
            diff = 0
        elif row == qrow:
            diff = abs(qcol - col)
        elif col == qcol:
            diff = abs(qrow - row)
        else:
            a = abs(qrow - row)
            b = abs(qcol - col)
            diff = math.sqrt((a**2) + (b**2))
        distance += length * diff
    return distance

def fitness(l, bigrams, att, freq):
    #home row proximity
    homeDist = distance(l, freq)

    #optimize for hand/finger/motion attributes of fastest bigrams
    hfm = hfmCost(att[0][0], att[1][0], att[2][0], bigrams, l)

    #qwerty similarity
    learning = findDiff(qwerty, l)

    # cost = (homeDist * 1.5) + (learning/65) + (hfm * 0.75)
    print (homeDist), (hfm), (learning/400)
    return homeDist + hfm + (learning/400)
def score_pool(pool, existing, keys, att, freq):
    scored = []
    for p in pool:
        if existing:
            k = p[0]
        else:
            k = p
        score = fitness(k, keys, att, freq)
        scored.append((score, k))
    scored_pool = sorted(scored, reverse=True)
    sorted_scored = []
    for s in scored_pool:
        sorted_scored.append((s[1], s[0]))
    return sorted_scored

def makeCopies(l):
    copy = []
    for c in l:
        copy.append((c[0][:], c[1]))
    return copy

def mutate(pool, m):
    copies = makeCopies(pool)
    for k in copies:
        for i in range(m):
            keys = random.sample(range(51), 2)
            k1 = keys[0]
            k2 = keys[1]
            temp = k[0][k1]
            k[0][k1] = k[0][k2]
            k[0][k2] = temp
        pool.append(k)
    return pool

def find_best(pool, b, prev):
    new = pool[0]
    for p in pool:
        if p[1] < new[1]:
            new = p
    if prev == new:
        b += 1
    else:
        prev = new
        b = 0
    return prev, b

visual_value = {219:('[', '{'), 220:('\\', '|'), 221:(']', '}'), 192:('`','~'), 186:(';', ':'), 190:('.', '>'), 188:(',','<'), 189:('-','_'),
        222:("'",'"'), 187:('=','+'), 191:("/", '?'), 9:('TAB','TAB'), 13:('ENTER','ENTER'), 
        32:('SPACE','SPACE'), 20:('CAPS','CAPS'), 8:('DELETE','DELETE'),
        48:('0', ')'), 49:('1', '!'), 50:('2','@'), 51:('3','#'), 52:('4','$'), 53:('5','%'), 54:('6','^'), 55:('7','&'), 56:('8','*'), 57:('9','('),
        65:('a', 'A'), 66:('b', 'B'), 67:('c', 'C'), 68:('d', 'D'), 69:('e', 'E'), 82:('r', 'R'), 83:('s', 'S'), 80:('p', 'P'), 81:('q', 'Q'), 87:('w', 'W'), 
        84:('t', 'T'), 85:('u', 'U'), 86:('v', 'V'), 76:('l', 'L'), 75:('k', 'K'), 74:('j', 'J'), 73:('i', 'I'), 72:('h', 'H'), 71:('g', 'G'), 70:('f', 'F'), 
        79:('o', 'O'), 78:('n', 'N'), 90:('z', 'Z'), 77:('m', 'M'), 88:('x', 'X'), 89:('y', 'Y'), 90:('/', '?'), 191:('?', '?')}

divs = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 
     'C12', 'C13', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'E04']

def createKeyboard(opt):
    final = []
    for k in opt[0]:
        final.append(visual_value[toCode[k]])
    f = []
    for j in range(len(final)):
        f.append([divs[j], final[j]])
    return f, opt[1]

def getbest(p):
    m = p[0]
    for i in p:
        if i[1] < m[1]:
            m = i          
    return m

def randompool(s):
    b = []
    for i in range(len(s)/2):
        b.append(random.randint(0, len(s)-1))
    return b

def main(bigrams, att, freq):
    loop = True
    p = 300
    m = 3
    g = 0
    b = 0
    n = 3
    q = 5
    prev = [0, 0]
    o_pool = []

    pool = create_pool(p)
    scored = score_pool(pool, False, bigrams, att, freq)

    while loop:
        prev, b = find_best(scored, b, prev)
        if b > n:
            o_pool.append(prev)
            b = 0
        if len(o_pool) == q:
            best = getbest(o_pool)
            break
        pool = scored[len(scored)/2:]
        pool = mutate(pool, m)
        g += 1
        scored = score_pool(pool, True, bigrams, att, freq)
    return createKeyboard(best), g