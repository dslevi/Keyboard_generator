import random, math

qwerty = [192, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 189, 187, 8,
            9, 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 219, 221, 220,
            65, 83, 68, 70, 71, 72, 74, 75, 76, 186, 222, 13,
            90, 88, 67, 86, 66, 78, 77, 190, 188, 190, 32]

def layout():
    return random.sample(range(52), 52)

def create_pool(size):
    pool = []
    #check to make sure each layout is unique!!
    for i in range(size):
        pool.append(layout())
    return pool

key_lhf = {192:[0, 0, 0, 0], 49:[0, 1, 0, 0], 50:[0, 2, 0, 1], 51:[0, 3, 0, 2], 52:[0, 4, 0, 3], 53:[0, 5, 0, 3], 54:[0, 6, 1, 3], 55:[0, 7, 1, 3], 56:[0, 8, 1, 2], 57:[0, 9, 1, 1], 48:[0, 10, 1, 0], 189:[0, 11, 1, 0], 187:[0, 12, 1, 0], 8:[0, 13, 1, 0], 
        9:[1, 0, 0, 0], 81:[1, 1, 0, 0], 87:[1, 2, 0, 1], 69:[1, 3, 0, 2], 82:[1, 4, 0, 3], 84:[1, 5, 0, 3], 89:[1, 6, 1, 3], 85:[1, 7, 1, 3], 73:[1, 8, 1, 2], 79:[1, 9, 1, 1], 80:[1, 10, 1, 0], 219:[1, 11, 1, 0], 221:[1, 12, 1, 0], 220:[1, 13, 1, 0], 
        20:[2, 0, 0, 0], 65:[2, 1, 0, 0], 83:[2, 2, 0, 1], 68:[2, 3, 0, 2], 70:[2, 4, 0, 3], 71:[2, 5, 0, 3], 72:[2, 6, 1, 3], 74:[2, 7, 1, 3], 75:[2, 8, 1, 2], 76:[2, 9, 1, 1],  186:[2, 10, 1, 0], 222:[2, 11, 1, 0], 13:[2, 12, 1, 0], 
        16:[3, 0, 0, 0], 90:[3, 1, 0, 0], 88:[3, 2, 0, 1], 67:[3, 3, 0, 2], 86:[3, 4, 0, 3], 66:[3, 5, 0, 3], 78:[3, 6, 1, 3], 77:[3, 7, 1, 3], 188:[3, 8, 1, 2], 190:[3, 9, 1, 1], 191:[3, 10, 1, 0], 
        17:[4, 0, 0, 0], 18:[4, 2, 2, 0], 32:[4, 3, 2, 0]}

def distance(l):
    key_lhf = {192:[0, 0, 0, 0], 49:[0, 1, 0, 0], 50:[0, 2, 0, 1], 51:[0, 3, 0, 2], 52:[0, 4, 0, 3], 53:[0, 5, 0, 3], 54:[0, 6, 1, 3], 55:[0, 7, 1, 3], 56:[0, 8, 1, 2], 57:[0, 9, 1, 1], 48:[0, 10, 1, 0], 189:[0, 11, 1, 0], 187:[0, 12, 1, 0], 8:[0, 13, 1, 0], 
        9:[1, 0, 0, 0], 81:[1, 1, 0, 0], 87:[1, 2, 0, 1], 69:[1, 3, 0, 2], 82:[1, 4, 0, 3], 84:[1, 5, 0, 3], 89:[1, 6, 1, 3], 85:[1, 7, 1, 3], 73:[1, 8, 1, 2], 79:[1, 9, 1, 1], 80:[1, 10, 1, 0], 219:[1, 11, 1, 0], 221:[1, 12, 1, 0], 220:[1, 13, 1, 0], 
        20:[2, 0, 0, 0], 65:[2, 1, 0, 0], 83:[2, 2, 0, 1], 68:[2, 3, 0, 2], 70:[2, 4, 0, 3], 71:[2, 5, 0, 3], 72:[2, 6, 1, 3], 74:[2, 7, 1, 3], 75:[2, 8, 1, 2], 76:[2, 9, 1, 1],  186:[2, 10, 1, 0], 222:[2, 11, 1, 0], 13:[2, 12, 1, 0], 
        16:[3, 0, 0, 0], 90:[3, 1, 0, 0], 88:[3, 2, 0, 1], 67:[3, 3, 0, 2], 86:[3, 4, 0, 3], 66:[3, 5, 0, 3], 78:[3, 6, 1, 3], 77:[3, 7, 1, 3], 188:[3, 8, 1, 2], 190:[3, 9, 1, 1], 191:[3, 10, 1, 0], 
        17:[4, 0, 0, 0], 18:[4, 2, 2, 0], 32:[4, 3, 2, 0]}

    keyList = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13], 
        [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [1, 10], [1, 11], [1, 12], [1, 13], 
        [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9],  [2, 10], [2, 11], [2, 12], 
        [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [3, 9], [3, 10], [4, 0], [4, 2], [4, 3]]

    length = 1.8
    distance = 0

    homerow = [[65, 83, 68, 70], [186, 76, 75, 74], [32]]
    for k in l:
        row, col, hand, finger = key_lhf[k]
        # homerow[] keyList[pos_k]
        hrow, hcol, hhand, hfinger = key_lhf[0]
        if finger == 0 or finger == 3:
            if hrow == row:
                #find diff between cols
                distance += (length * abs(hcol - col))
            elif hcol == col:
                #find diff between rows
                distance += (length * abs(hrow - row))
            else:
                #pythagorean theorem
                a = (length * abs(hcol - col))
                b = (length * abs(hrow - row))
                c = math.sqrt((a**2) + (b**2))
                distance += c
        else:
            distance += (length * abs(hrow - row))
    return distance

def hfmCost(h, f, m, keys, layout):
    cost = 0
    return cost

#calculate by proximity instead of differences
def findDiff(b, l):
    diff = 0
    for i in range(len(b)):
        if b[i] != l[i]:
            diff += 1
    return diff

def fitness(layout, keys, att):
    #home row proximity
    homeDist = distance(layout)

    #optimize for hand/finger/motion attributes of fastest bigrams
    hand, finger, motion = att
    hfm = hfmCost(hand[0][:2], finger[1][:2], motion[2][:2], keys, layout)

    #qwerty similarity
    key_cost = 100/len(qwerty)
    learning = key_cost * findDiff(qwerty, layout)

    cost = "%.1f" % (float(1/3) * homeDist) + (float(1/3) * hfm) + (float(1/3) * learning)
    return cost

def score_pool(pool, existing, keys, att):
    scored = []
    for p in pool:
        if existing:
            k = p[0]
        else:
            k = p
        score = fitness(k, keys, att)
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
            keys = random.sample(range(52), 2)
            k1 = keys[0]
            k2 = keys[1]
            temp = k[0][k1]
            k[0][k1] = k[0][k2]
            k[0][k2] = temp
        pool.append(k)
    return pool

def find_optimal(pool, b, prev):
    new = pool[0]
    for p in pool:
        if p[1] == 10:
            return p, prev, b
        if p[1] > [new][1]:
            new = p
    if prev == new:
        b += 1
    else:
        prev = new
        b = 0
    return False, prev, b

def rand_selection(s):
    p = []
    weighted = [0, 1, 2, 3, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9]
    for i in range(len(s)/2):
        x = weighted[random.randint(0, len(weighted) - 1)]
        p.append(s[x])
        for n in weighted:
            if n == x:
                del n
    return p

def createKeyboard(opt):
    final = []
    board = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'B01', 'B02', 'B03', 'B04', 
    'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 
    'C10', 'C11', 'C12', 'C13', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'E04']

    for k in opt:
        final.append(board[k])
    return final

def main(keys, att):
    loop = True
    p = 10
    m = 3
    g = 0
    b = 0
    n = 3
    q = 4
    prev = [0, 0]
    o_pool = []

    pool = create_pool(p)
    scored = score_pool(pool, False, keys, att)
    #think about subsituting a for loop if while takes too long, force an "optimal" --best available layout
    while loop:
        optimal, prev, b = find_optimal(scored, b, prev)
        if optimal:
            break
        if b > n:
            o_pool.append(prev)
            b = 0
        if len(prev) > q:
            break
        pool = rand_selection(scored)
        pool = mutate(pool, m)
        g += 1
        scored = score_pool(pool, True, keys, att)
    if optimal:
        keyboard = createKeyboard(optimal[0])
        return keyboard
    else:
        #run through process again and return best from optimal keyboard
        return keyboard

keys = [71, 75, 74, 72, 70, 68, 83, 32, 69, 84, 65, 79, 73, 78, 82, 8, 76, 67, 85, 13, 77, 80, 87, 89, 66, 188, 190, 86, 57, 48, 189, 186, 222, 187, 9, 88, 191, 52, 56, 49, 219, 221, 81, 50, 90, 53, 51, 220, 54, 55, 192]
att = [[1, '68.75', 1, '81.25', 0, '62.50'], [1, '81.25', 1, '93.75', 0, '56.25'], [0, '18.75', 1, '12.50', 1, '25.00']]
print main(keys, att)