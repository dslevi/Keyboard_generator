import random

#MAPS
visual_value = {219:('[', '{'), 220:('\\', '|'), 221:(']', '}'), 192:('`','~'), 186:(';', ':'), 190:('.', '>'), 188:(',','>'), 189:('-','_'),
        222:("'",'"'), 187:('=','+'), 190:("/", '?'), 9:('TAB','TAB'), 13:('ENTER','ENTER'), 17:('CTRL','CTRL'), 16:('SHIFT','SHIFT'), 
        18:('ALT','ALT'), 32:('SPACE','SPACE'), 20:('CAPS','CAPS'), 8:('DELETE','DELETE'),
        48:('0', ')'), 49:('1', '!'), 50:('2','@'), 51:('3','#'), 52:('4','$'), 53:('5','%'), 54:('6','^'), 55:('7','&'), 56:('8','*'), 57:('9','('),
        65:('a', 'A'), 66:('b', 'B'), 67:('c', 'C'), 68:('d', 'D'), 69:('e', 'E'), 82:('r', 'R'), 83:('s', 'S'), 80:('p', 'P'), 81:('q', 'Q'), 87:('w', 'W'), 
        84:('t', 'T'), 85:('u', 'U'), 86:('v', 'V'), 76:('l', 'L'), 75:('k', 'K'), 74:('j', 'J'), 73:('i', 'I'), 72:('h', 'H'), 71:('g', 'G'), 70:('f', 'F'), 
        79:('o', 'O'), 78:('n', 'N'), 90:('z', 'Z'), 77:('m', 'M'), 88:('x', 'X'), 89:('y', 'Y')}

#KEYBOARD PROFILE

def parseKeystrokes(strokes):
    keystrokes = []
    tokens = strokes.split()
    shift_on = False
    for i in range(len(tokens)):
        if i % 3 == 0:
            if int(tokens[i + 1]) == 16:
                shift_on = not shift_on
            keystrokes.append((tokens[i].encode('ascii', 'ignore'), int(tokens[i + 1]), int(tokens[i + 2]), shift_on))
    return keystrokes

def keyFreq(keystrokes):
    freq = {}
    for stroke in keystrokes:
        if stroke[0] == "D":
            if stroke[3] and stroke[1] > 90 and stroke[1] < 65:
                key = visual_value[stroke[1]][1]
            else:
                key = visual_value[stroke[1]][0]
            freq[key] = freq.get(key, 0) + 1
    return freq

#fix mistakes later!
def keyMistakes(keystrokes):
    delete = 8
    count = 0
    mistakes = {}

    for i in range(len(keystrokes)):
        if keystrokes[i][0] == "D":
            if keystrokes[i][1] == delete:
                count += 1
            elif (count > 0):
                for h in range(count):
                    index = i - (count + h + 1)
                    if index >= 0:
                        mistake = visual_value[keystrokes[index][1]]
                        mistakes[mistake] += 1
                    else:
                        mistakes[visual_value[delete]] += 1
                count = 0
            key = visual_value[keystrokes[i][1]]
            mistakes[key] = mistakes.get(key, 0)
    if (count > 0):
        for h in range(count):
            index = i - (count + h)
            if index >= 0:
                mistake = visual_value[keystrokes[index][1]]
                mistakes[mistake] += 1
            else:
                mistakes[visual_value[delete]] += 1
    return mistakes

def findKeytimes(keystrokes):
    keytimes = []
    for i in range(len(keystrokes)):
        if (i + 1) < len(keystrokes) and keystrokes[i][0] == "D":
            down = keystrokes[i]
            for h in range(i + 1, len(keystrokes)):
                if keystrokes[h][0] == "U" and keystrokes[h][1] == keystrokes[i][1]:
                    up = keystrokes[h]
                    keytimes.append((down, up))
                    break
    return keytimes

def findngrams(n, keytimes):
    ngrams = []
    for i in range(len(keytimes)):
        ngram = []
        if (i + (n - 1)) < len(keytimes):
            for h in range(n):
                ngram.append(keytimes[i + h])
        if len(ngram) > 0:
            ngrams.append(ngram)
    return ngrams

#key press and release
def dwellTime(keytimes):
    times = {}
    dwellTimes = {}
    for key in keytimes:        
        downtime = key[0][2]
        uptime = key[1][2]
        if key[1][3] and key[1][1] > 90 and key[1][1] < 65:
            key_time = visual_value[key[1][1]][1]
        else:
            key_time = visual_value[key[1][1]][0]
        if times.has_key(key_time):
            times[key_time].append((uptime - downtime))
        else:
            times[key_time] = [(uptime - downtime)]
    for k in times:
        total = 0
        for t in times[k]:
            total += t
        dwellTimes[k] = (total/len(times[k]))
    return dwellTimes

#Key up to key down
def flightTime(ngraphs):
    times = {}
    flightTimes = {}
    for ngraph in ngraphs:
        key_up = ngraph[0][1][2]
        key_down = ngraph[1][0][2]
        diff = key_down - key_up
        if ngraph[0][0][3] and ngraph[0][0][1] > 90 and ngraph[0][0][1] < 65:
            key1 = visual_value[ngraph[0][0][1]][1]
        else:
            key1 = visual_value[ngraph[0][0][1]][0]
        if ngraph[1][0][3] and ngraph[1][0][1] > 90 and ngraph[1][0][1] < 65:
            key2 = visual_value[ngraph[1][0][1]][1]
        else:
            key2 = visual_value[ngraph[1][0][1]][0]
        key = key1 + ":" + key2
        if times.has_key(key):
            times[key].append(diff)
        else:
            times[key] = [diff]
    for k in times:
        total = 0
        for t in times[k]:
            total += t
        flightTimes[k] = (total/len(times[k]))
    return flightTimes

def definingTimes(n, times, fast):
    keytimes = []
    defining = []
    for time in times:
        keytimes.append((times[time], time))
    keytimes.sort()
    if n > len(times):
        n = len(times) 
    for i in range(n):
        if fast:
            defining.append(keytimes[i])
        else:
            defining.append(keytimes[-(1 + i)])
    return defining

def ngramTimes(ngrams):
    times = {}
    for n in ngrams:
        start = n[0][0][2]
        end = n[-1][0][2]
        key = ""
        for i in range(len(n)):
            if n[i][0][3]:
                ch = visual_value[n[i][0][1]][1]
            else:
                ch = visual_value[n[i][0][1]][0]
            key += ch + ":"
        if times.get(key[:-1]):
            times[key[:-1]].append((end - start))
        else:
            times[key[:-1]] = [(end - start)]
    final = {}
    for time in times:
        total = 0
        for t in times[time]:
            total += t
        avg = (total/len(times[time]))
        final[time] = avg 
    return final

def bestBigrams(bigramTimes):
    pass

def trigramTimes(keystrokes):
    pass

def bestTrigrams(trigramTimes):
    pass







#KEYBOARD GENERATION

def bigramFreq(keystrokes):
    bigrams = {}
    for stroke in keystrokes:
        if stroke[0] == "D":
            bigrams[stroke[1]] = bigrams.get(stroke[1], 0) + 1
    return bigrams

def createKeyboard(strokes):
    #key values ordered from most frequently typed to least
    common_keys = [('SPACE'), ('E'), ('T'), ('A'), ('O'), ('I'), ('N'), ('S'), ('R'), ('H'), ('DELETE'), 
        ('L'), ('D'), ('C'), ('U'), ('ENTER'), ('M'), ('F'), ('P'), ('G'), ('W'), ('Y'), ('B'), (',', '<'), ('.', '>'), 
        ('V'), ('K'), ('9', '('), ('0', '1'), ('-', '_'), (';',':'), ("'", '"'), ('=', '+'), ('TAB'), ('X'), ('/','?'), ('4','$'), ('8', '*'), 
        ('1', '!'), ('J'), ('[', '{'), (']', '}'), ('Q'), ("2", '@'), ('Z'), ('5', '%'), ('3', '#'), ('\\', '|'), ('6','^'), ('7','&'), ('`', '~')]

    common_keys2 = [('SPACE', 'SPACE'), ('e', 'E'), ('t', 'T'), ('a', 'A'), ('o', 'O'), ('i', 'I'), ('n', 'N'), ('s', 'S'), ('r', 'R'), ('h', 'H'), ('DELETE', 'DELETE'), 
        ('l', 'L'), ('d', 'D'), ('c', 'C'), ('u', 'U'), ('ENTER', 'ENTER'), ('m', 'M'), ('f', 'F'), ('p', 'P'), ('g', 'G'), ('w', 'W'), ('y', 'Y'), ('b', 'B'), 
        (',', '<'), ('.', '>'), ('v', 'V'), ('k', 'K'), ('9', '('), ('0', ')'), ('-', '_'), (';',':'), ("'", '"'), ('=', '+'), ('TAB', 'TAB'), ('x', 'X'), ('/','?'), 
        ('4','$'), ('8', '*'), ('1', '!'), ('j', 'J'), ('[', '{'), (']', '}'), ('q', 'Q'), ("2", '@'), ('z', 'Z'), ('5', '%'), ('3', '#'), ('\\', '|'), ('6','^'), 
        ('7','&'), ('`', '~')]

    bigram_freq = bigramFreq(strokes)
    reversed_bigrams = []
    for x in bigram_freq:
        reversed_bigrams.append((bigram_freq[x], x))
    sorted_bigrams = sorted(reversed_bigrams, reverse=True)

    dvorak_keyboard = []
    dvorak_keyboard2 = []
    for x, y in sorted_bigrams:
        if visual_value[y][0] != "SHIFT" and visual_value[y][0] != "CONTROL" and visual_value[y][0] != "ALT" and visual_value[y][0] != "CAPS": 
            if visual_value[y] not in dvorak_keyboard:
                if y <= 90 and y >= 65:
                    dvorak_keyboard.append(visual_value[y][1])
                elif y <= 32:
                    dvorak_keyboard.append(visual_value[y][0])
                else:
                    dvorak_keyboard.append((visual_value[y][1], visual_value[y][0]))
            if visual_value[y] not in dvorak_keyboard2:
                dvorak_keyboard2.append(visual_value[y])
    if len(dvorak_keyboard) < len(common_keys):
        for h in common_keys:
            if h not in dvorak_keyboard:
                if len(h) > 1 and h != "ENTER" and h != "SPACE" and h != "TAB" and h!="DELETE":
                    dvorak_keyboard.append((h[1], h[0]))
                else:
                    dvorak_keyboard.append(h)
        for h in common_keys2:
            if h not in dvorak_keyboard2:
                dvorak_keyboard2.append(h)

    #the corresponding location map, highest priority to lowest| removed D12 - shift, E8 - ctrl, E5 - alt
    dvorak_map = ['C06', 'C05', 'C07', 'C04', 'C08', 'C03', 'C09', 'C02', 'C10', 'C11', 'C12', 'C13', 'B06', 'B05', 'B07', 'B04', 'B08', 'B03', 'B09', 'B02', 'B10', 'B01', 'B11', 
                'B12', 'B13', 'B14', 'D07', 'D06', 'D08', 'D05', 'D09', 'D04', 'D10', 'D03', 'D11', 'D02', 'E04', 'A08', 'A07', 'A06', 'A09', 
                'A05', 'A10', 'A04', 'A11', 'A03', 'A12', 'A02', 'A13', 'A01', 'A14']

    visual_map = sorted(zip(dvorak_map, dvorak_keyboard))
    value_map = sorted(zip(dvorak_map, dvorak_keyboard2))

    return visual_map, value_map

dvorak_map = ['C06', 'C05', 'C07', 'C04', 'C08', 'C03', 'C09', 'C02', 'C10', 'C11', 'C12', 'C13', 'B06', 'B05', 'B07', 'B04', 'B08', 'B03', 'B09', 'B02', 'B10', 'B01', 'B11', 
                'B12', 'B13', 'B14', 'D07', 'D06', 'D08', 'D05', 'D09', 'D04', 'D10', 'D03', 'D11', 'D02', 'E04', 'A08', 'A07', 'A06', 'A09', 
                'A05', 'A10', 'A04', 'A11', 'A03', 'A12', 'A02', 'A13', 'A01', 'A14']

def makePattern():
    pattern = []
    for i in range(10):
        pattern.append(dvorak_map[random.randint(0, len(dvorak_map) -1)])
    return pattern