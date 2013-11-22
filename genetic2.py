import random

board = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 'A13', 'A14', 'B01', 'B02', 'B03', 'B04', 
'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12', 'B13', 'B14', 'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 
'C10', 'C11', 'C12', 'C13', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'E04']

def layout():
    return random.sample(range(52), 52)

def create_pool(size):
    pool = []
    for i in range(size):
        pool.append(layout())
    return pool

def fitness(layout):
    return random.randint(0, 100)

def score_pool(pool, existing):
    scored = []
    for p in pool:
        if existing:
            k = p[0]
        else:
            k = p
        score = fitness(k)
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

def find_optimal(pool):
    for p in pool:
        if p[1] == 100:
            return p
    return False

def main():
    loop = True
    p = 10
    m = 3
    g = 0
    pool = create_pool(p)
    scored = score_pool(pool, False)
    #think about subsituting a for loop if while takes too long, force an "optimal" --best available layout
    while loop:
        optimal = find_optimal(pool)
        if optimal:
            break
        pool = scored[:(p/2)]
        pool = mutate(pool, m)
        g += 1
        scored = score_pool(pool, True)
    return g, optimal

print main()