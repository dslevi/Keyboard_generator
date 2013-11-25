import random, math

#MAPS
visual_value = {219:('[', '{'), 220:('\\', '|'), 221:(']', '}'), 192:('`','~'), 186:(';', ':'), 190:('.', '>'), 188:(',','>'), 189:('-','_'),
        222:("'",'"'), 187:('=','+'), 190:("/", '?'), 9:('TAB','TAB'), 13:('ENTER','ENTER'), 17:('CTRL','CTRL'), 16:('SHIFT','SHIFT'), 
        18:('ALT','ALT'), 32:('SPACE','SPACE'), 20:('CAPS','CAPS'), 8:('DELETE','DELETE'),
        48:('0', ')'), 49:('1', '!'), 50:('2','@'), 51:('3','#'), 52:('4','$'), 53:('5','%'), 54:('6','^'), 55:('7','&'), 56:('8','*'), 57:('9','('),
        65:('a', 'A'), 66:('b', 'B'), 67:('c', 'C'), 68:('d', 'D'), 69:('e', 'E'), 82:('r', 'R'), 83:('s', 'S'), 80:('p', 'P'), 81:('q', 'Q'), 87:('w', 'W'), 
        84:('t', 'T'), 85:('u', 'U'), 86:('v', 'V'), 76:('l', 'L'), 75:('k', 'K'), 74:('j', 'J'), 73:('i', 'I'), 72:('h', 'H'), 71:('g', 'G'), 70:('f', 'F'), 
        79:('o', 'O'), 78:('n', 'N'), 90:('z', 'Z'), 77:('m', 'M'), 88:('x', 'X'), 89:('y', 'Y'), 90:('?', '?'), 191:('?', '?')}

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
    if len(text) <= 0:
        accuracy = 0
    else:
        accuracy = ((len(text) - len(chars))/float(len(text)) * 100)
        if accuracy < 0:
            accuracy = 0
        accuracy = "%.2f" % accuracy
        accuracy = str(accuracy + "%")
    if time <= 0:
        wpm = 0
    else:
        wpm = ("%.1f" % (len(text.split())/(float(time)/60)))
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
        #replace with intoPercent(hands, total)
        for i in range(len(hands)):
            percentage = ((hands[i]/float(total)) * 100)
            hands[i] = (str("%.1f" % percentage) + "%")
        for i in range(len(fingers)):
            for h in range(len(fingers[i])):
                percentage = ((fingers[i][h]/float(total)) * 100)
                fingers[i][h] = (str("%.1f" % percentage) + "%")
    return hands, fingers

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
            l[i] = (str("%.1f" % percentage) + "%")
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

def triAttributes(trigrams):
    total = 0
    times = []

    #same, alternated, mix
    hand = [0, 0, 0]
    fing = [0, 0, 0]

    #horizontal, vertical, mix, (diagonal/hand alt)
    motion = [0, 0, 0, 0]

    for n in trigrams:
        key1 = n[0][0][1]
        key2 = n[1][0][1]
        key3 = n[2][0][1]
        if key1 != 191 and key2 != 191 and key3 != 191:
            total += 1
            diff = n[1][0][2] - n[0][0][2]
            r1, c1, h1, f1 = key_lhf[key1]
            r2, c2, h2, f2 = key_lhf[key2]
            r3, c3, h3, f3 = key_lhf[key3]
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

b = [[(('D', 81, 1385352916045, False), ('U', 81, 1385352916219, False)), (('D', 65, 1385352916612, False), ('U', 65, 1385352916778, False))], [(('D', 65, 1385352916612, False), ('U', 65, 1385352916778, False)), (('D', 87, 1385352917268, False), ('U', 87, 1385352917450, False))], [(('D', 87, 1385352917268, False), ('U', 87, 1385352917450, False)), (('D', 83, 1385352917732, False), ('U', 83, 1385352917898, False))], [(('D', 83, 1385352917732, False), ('U', 83, 1385352917898, False)), (('D', 69, 1385352918388, False), ('U', 69, 1385352918570, False))], [(('D', 69, 1385352918388, False), ('U', 69, 1385352918570, False)), (('D', 68, 1385352918812, False), ('U', 68, 1385352918978, False))], [(('D', 68, 1385352918812, False), ('U', 68, 1385352918978, False)), (('D', 81, 1385352920740, False), ('U', 81, 1385352920890, False))], [(('D', 81, 1385352920740, False), ('U', 81, 1385352920890, False)), (('D', 90, 1385352922156, False), ('U', 90, 1385352922330, False))], [(('D', 90, 1385352922156, False), ('U', 90, 1385352922330, False)), (('D', 85, 1385352923092, False), ('U', 85, 1385352923266, False))], [(('D', 85, 1385352923092, False), ('U', 85, 1385352923266, False)), (('D', 74, 1385352923524, False), ('U', 74, 1385352923666, False))], [(('D', 74, 1385352923524, False), ('U', 74, 1385352923666, False)), (('D', 73, 1385352924148, False), ('U', 73, 1385352924258, False))], [(('D', 73, 1385352924148, False), ('U', 73, 1385352924258, False)), (('D', 75, 1385352924796, False), ('U', 75, 1385352925018, False))], [(('D', 75, 1385352924796, False), ('U', 75, 1385352925018, False)), (('D', 79, 1385352925556, False), ('U', 79, 1385352925690, False))], [(('D', 79, 1385352925556, False), ('U', 79, 1385352925690, False)), (('D', 76, 1385352925964, False), ('U', 76, 1385352926122, False))]]
print triAttributes(b)

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