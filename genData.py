import random, math

#MAPS
visual_value = {219:('[', '{'), 220:('\\', '|'), 221:(']', '}'), 192:('`','~'), 186:(';', ':'), 190:('.', '>'), 188:(',','<'), 189:('-','_'),
        222:("'",'"'), 187:('=','+'), 191:("/", '?'), 9:('TAB','TAB'), 13:('ENTER','ENTER'), 17:('CTRL','CTRL'), 16:('SHIFT','SHIFT'), 
        18:('ALT','ALT'), 32:('SPACE','SPACE'), 20:('CAPS','CAPS'), 8:('DELETE','DELETE'),
        48:('0', ')'), 49:('1', '!'), 50:('2','@'), 51:('3','#'), 52:('4','$'), 53:('5','%'), 54:('6','^'), 55:('7','&'), 56:('8','*'), 57:('9','('),
        65:('a', 'A'), 66:('b', 'B'), 67:('c', 'C'), 68:('d', 'D'), 69:('e', 'E'), 82:('r', 'R'), 83:('s', 'S'), 80:('p', 'P'), 81:('q', 'Q'), 87:('w', 'W'), 
        84:('t', 'T'), 85:('u', 'U'), 86:('v', 'V'), 76:('l', 'L'), 75:('k', 'K'), 74:('j', 'J'), 73:('i', 'I'), 72:('h', 'H'), 71:('g', 'G'), 70:('f', 'F'), 
        79:('o', 'O'), 78:('n', 'N'), 90:('z', 'Z'), 77:('m', 'M'), 88:('x', 'X'), 89:('y', 'Y'), 90:('?', '?'), 191:('?', '?')}

value = {'CTRL': 17, '$': 52, '(': 57, ',': 188, '0': 48, '4': 52, 'TAB': 9, '8': 56, '<': 188, '@': 50, 'D': 68, 'H': 72, 'L': 76, 'P': 80, 'T': 84, 'ENTER': 13, 'X': 88, '\\': 220, '`': 192, 'd': 68, 'h': 72, 'l': 76, 'p': 80, 't': 84, 'x': 88, '|': 220, 'DELETE': 8, '#': 51, "'": 222, '+': 187, '3': 51, '7': 55, ';': 186, '?': 191, 'C': 67, 'G': 71, 'K': 75, 'O': 79, 'CAPS': 20, 'S': 83, 'W': 87, '[': 219, '_': 189, 'c': 67, 'g': 71, 'k': 75, 'o': 79, 's': 83, 'w': 87, '{': 219, '"': 222, '&': 55, '*': 56, '.': 190, '2': 50, '6': 54, ':': 186, '>': 190, 'B': 66, 'F': 70, 'J': 74, 'N': 78, 'R': 82, 'V': 86, '^': 54, 'b': 66, 'f': 70, 'j': 74, 'n': 78, 'r': 82, 'v': 86, 'ALT': 18, '~': 192, 'SHIFT': 16, '!': 49, '%': 53, ')': 48, '-': 189, '1': 49, '5': 53, '9': 57, '=': 187, 'A': 65, 'E': 69, 'SPACE': 32, 'I': 73, 'M': 77, 'Q': 81, 'U': 85, 'Y': 89, ']': 221, 'a': 65, 'e': 69, 'i': 73, 'm': 77, 'q': 81, 'u': 85, 'y': 89, '}': 221}

#KEYBOARD PROFILE

def parseKeystrokes(input):
    keystrokes = []
    tokens = input.split()
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

def keyMistakes(mistakes):
    freq = {}
    chars = mistakes[:-1].split()
    for ch in chars:
        freq[ch.encode('ascii', 'ignore')] = freq.get(ch.encode('ascii', 'ignore'), 0) + 1
    return freq

def keyAccuracy(mistakes, text, time):
    chars = mistakes[:-1].split()
    if len(text) > 0:
        accuracy = ((len(text) - len(chars))/float(len(text)) * 100)
        if accuracy < 0:
            accuracy = 0
        accuracy = "%.2f" % accuracy
        accuracy = str(accuracy + "%")
    else:
        accuracy = 0
    time = float(time)
    if time > 0:
        wpm = ("%.1f" % (len(text.split())/(time/60)))
    else:
        wpm = 0
    return accuracy, wpm

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

def ngramFreq(n, input1, input2):
    freq = []

    return freq

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

def fastestTimes(n, times):
    keytimes = []
    defining = []
    for time in times:
        keytimes.append((times[time], time))
    keytimes.sort()

    for i in range(n):
        val1 = value[keytimes[i][1][0]]
        val2 = value[keytimes[i][1][1]]
        defining.append([val1, val2])
    return defining

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

#row, col, hand, finger
key_lhf = {192:[0, 0, 0, 0], 49:[0, 1, 0, 0], 50:[0, 2, 0, 1], 51:[0, 3, 0, 2], 52:[0, 4, 0, 3], 53:[0, 5, 0, 3], 54:[0, 6, 1, 3], 55:[0, 7, 1, 3], 56:[0, 8, 1, 2], 57:[0, 9, 1, 1], 48:[0, 10, 1, 0], 189:[0, 11, 1, 0], 187:[0, 12, 1, 0], 8:[0, 13, 1, 0], 
        9:[1, 0, 0, 0], 81:[1, 1, 0, 0], 87:[1, 2, 0, 1], 69:[1, 3, 0, 2], 82:[1, 4, 0, 3], 84:[1, 5, 0, 3], 89:[1, 6, 1, 3], 85:[1, 7, 1, 3], 73:[1, 8, 1, 2], 79:[1, 9, 1, 1], 80:[1, 10, 1, 0], 219:[1, 11, 1, 0], 221:[1, 12, 1, 0], 220:[1, 13, 1, 0], 
        20:[2, 0, 0, 0], 65:[2, 1, 0, 0], 83:[2, 2, 0, 1], 68:[2, 3, 0, 2], 70:[2, 4, 0, 3], 71:[2, 5, 0, 3], 72:[2, 6, 1, 3], 74:[2, 7, 1, 3], 75:[2, 8, 1, 2], 76:[2, 9, 1, 1],  186:[2, 10, 1, 0], 222:[2, 11, 1, 0], 13:[2, 12, 1, 0], 
        16:[3, 0, 0, 0], 90:[3, 1, 0, 0], 88:[3, 2, 0, 1], 67:[3, 3, 0, 2], 86:[3, 4, 0, 3], 66:[3, 5, 0, 3], 78:[3, 6, 1, 3], 77:[3, 7, 1, 3], 188:[3, 8, 1, 2], 190:[3, 9, 1, 1], 191:[3, 10, 1, 0], 
        17:[4, 0, 0, 0], 18:[4, 2, 2, 0], 32:[4, 3, 2, 0]}

def handFingerFreq(keytimes):
    total = 0
    hands = [0, 0, 0]
    fingers = [[0, 0, 0, 0], [0, 0, 0, 0], [0]]

    for key in keytimes:
        for k in key:
            if k[0] == "D":
                hands[key_lhf[k[1]][2]] += 1
                fingers[key_lhf[k[1]][2]][key_lhf[k[1]][3]] += 1
                total += 1
    if total > 0:
        for i in range(len(hands)):
            percentage = ((hands[i]/float(total)) * 100)
            hands[i] = percentage
        for i in range(len(fingers)):
            for h in range(len(fingers[i])):
                percentage = ((fingers[i][h]/float(total)) * 100)
                fingers[i][h] = percentage
    f = [fingers[0][0], fingers[0][1], fingers[0][2], fingers[0][3], fingers[2][0], fingers[1][3], fingers[1][2], fingers[1][1], fingers[1][0]]
    return hands, f

def distance(keytimes):
    #measured in mm, includes gap between keys
    length = 1.8
    distance = 0
    homerow = [[65, 83, 68, 70], [186, 76, 75, 74], [32]]
    for key in keytimes:
        for k in key:
            if k[0] == "D":
                row, col, hand, finger = key_lhf[k[1]]
                hrow, hcol, hhand, hfinger = key_lhf[homerow[hand][finger]]
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
    return (str("%.1f" % distance) + " mm")

#TYPING ATTRIBUTES
def intoPercent(l, total):
    for i in range(len(l)):
            percentage = ((l[i]/float(total)) * 100)
            l[i] = percentage
    return l

def biAttributes(bigrams):
    total = 0
    times = []

    #same, alternated
    hand = [0, 0]
    fing = [0, 0]

    #horizontal, vertical, (diagonal/hand alt)
    motion = [0, 0, 0]

    for n in bigrams:
        key1 = n[0][0][1]
        key2 = n[1][0][1]
        if key1 != 191 and key2 != 191:
            total += 1
            diff = n[1][0][2] - n[0][0][2]
            r1, c1, h1, f1 = key_lhf[key1]
            r2, c2, h2, f2 = key_lhf[key2]

            if h1 == h2:
                hand[0] += 1
                h = 0

                if r1 == r2 and c1 == c2:
                    motion[2] += 1
                    m = 2
                elif r1 == r2:
                    motion[0] += 1
                    m = 0
                else:
                    motion[1] += 1
                    m = 1
            else:
                hand[1] += 1
                h = 1
                m = 2
                motion[2] += 1

            if f1 == f2:
                fing[0] += 1
                f = 0
            else:
                fing[1] += 1
                f = 1

            times.append([diff, key1, key2, h, f, m])
    if total > 0:
        hand = intoPercent(hand, total)
        fing = intoPercent(fing, total)
        motion = intoPercent(motion, total)
    return hand, fing, motion, times

def definingAtt(times):
    times.sort()
    fastest = times[:(len(times)/3)]
    middle = times[len(times)/3:((2*len(times))/3)]
    slowest = times[(2*len(times))/3:]
    fastest = findAtt(fastest)
    middle = findAtt(middle)
    slowest = findAtt(slowest)
    vatt, att = wordAtt([fastest, middle, slowest])
    return fastest, middle, slowest, vatt, att 

def findAtt(l):
    total = len(l)
    att = [[0, 0], [0, 0], [0, 0, 0]]
    for e in l:
        att[0][e[3]] += 1
        att[1][e[4]] += 1
        att[2][e[5]] += 1
    if total > 0:
        for i in range(len(att[0])):
            att[0][i] =  ((att[0][i]/float(total)) * 100)
        for i in range(len(att[1])):
            att[1][i] = ((att[1][i]/float(total)) * 100)
        for i in range(len(att[2])):
            att[2][i] = ((att[2][i]/float(total)) * 100)
    return att

def wordAtt(l):
    d = [[], [], []]
    a = [[], [], []]
    for i in range(len(l)):
        if l[i][0][0] > l[i][0][1]:
            d[i].append("Same hand")
            a[0].append(0)
            a[0].append(l[i][0][0])
        elif l[i][0][0] < l[i][0][1]:
            d[i].append("Hand alternation")
            a[0].append(1)
            a[0].append(l[i][0][1])
        else:
            d[i].append("Equal alternation and same hand usage")
            a[0].append(2)
            a[0].append(l[i][0][1])

        if l[i][1][0] > l[i][1][1]:
            d[i].append("Same finger")
            a[1].append(0)
            a[1].append(l[i][1][0])
        elif l[i][1][0] < l[i][1][1]:
            d[i].append("Finger alteration")
            a[1].append(1)
            a[1].append(l[i][1][1])
        else:
            d[i].append("Equal alternation and same finger usage")
            a[1].append(2)
            a[1].append(l[i][1][1])

        if l[i][2][0] > l[i][2][1]:
            d[i].append("Horizontal movement")
            a[2].append(0)
            a[2].append(l[i][2][0])
        elif l[i][2][0] < l[i][2][1]:
            d[i].append("Vertical movement")
            a[2].append(1)
            a[2].append(l[i][2][1])
        else:
            d[i].append("Horizontal, vertical, diagonal movement")
            a[2].append(2)
            a[2].append(l[i][2][2])
    return d, a 

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
        ('V'), ('K'), ('9', '('), ('0', ')'), ('-', '_'), (';',':'), ("'", '"'), ('=', '+'), ('TAB'), ('X'), ('/','?'), ('4','$'), ('8', '*'), 
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

def makeKeys(strokes):
    common_val = [32, 69, 84, 65, 79, 73, 78, 83, 82, 72, 8, 
        76, 68, 67, 85, 13, 77, 70, 80, 71, 87, 89, 66, 188, 190, 
        86, 75, 57, 48, 189, 186, 222, 187, 9, 88, 52, 56, 
        49, 74, 219, 221, 81, 50, 90, 53, 51, 220, 54, 55, 192]
    keys = []
    bigram_freq = bigramFreq(strokes)
    reversed_bigrams = []
    for x in bigram_freq:
        reversed_bigrams.append((bigram_freq[x], x))
    sorted_bigrams = sorted(reversed_bigrams, reverse=True)
    for key in sorted_bigrams:
        if key != 16:
            keys.append(key[1])
    for key in common_val:
        if key not in keys:
            keys.append(key)
    return keys

