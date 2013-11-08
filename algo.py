keycode = { '20': 'CAPS', '8': 'DELETE', '120': 'x', '121': 'y', '122': 'z', '123': '{', '124': '|', '125': '}', '126': '~', '118': 'v', '59': ';', 
            '58': ';', '55': '7', '54': '6', '57': '9', '56': '8', '51': '3', '50': '2', '53': '5', '52': '4', 'x': 'META', '115': 's', '114': 'r', 
            '117': 'u', '116': 't', '111': 'o', '110': 'n', '113': 'q', '112': 'p', '82': 'R', '83': 'S', '80': 'P', '81': 'Q', '119': 'w', '87': 'W', 
            '84': 'T', '85': 'U', '108': 'l', '109': 'm', '102': 'f', '103': 'g', '100': 'd', '101': 'e', '106': 'j', '107': 'k', '104': 'h',
            '105': 'i', '39': "'", '38': '&', '33': '!', '32': 'SPACE', '37': '%', '36': '$', '35': '#', '34': '"', '60': '<', '61': '=', '62': '>', 
            '63': '?', '64': '@', '65': 'A', '66': 'B', '67': 'C', '68': 'D', '69': 'E', '99': 'c', '98': 'b', '91': '[', '90': 'Z', '93': ']',
             '92': '\\', '95': '_', '94': '^', '97': 'a', '96': '`', '13': 'ENTER', '17': 'CTRL', '16': 'SHIFT', '18': 'ALT', '88': 'X', '89': 'Y', 
             '48': '0', '49': '1', '46': '.', '86': 'V', '44': ',', '45': '-', '42': '*', '43': '+', '40': '(', '41': ')', '9': 'TAB', '77': 'M', 
             '76': 'L', '75': 'K', '74': 'J', '73': 'I', '72': 'H', '71': 'G', '70': 'F', '79': 'O', '78': 'N', '47': '/'}

qwerty_map = { 126:'A1', 96:'A1', 33:'A2', 49:'A2', 64:'A3', 50:'A3', 35:'A4', 51:'A4', 36:'A5', 52:'A5', 37:'A6', 53:'A6', 94:'A7', 54:'A7', 38:'A8', 
                55:'A8', 42:'A9', 56:'A9', 40:'A10', 57:'A10', 41:'A11', 48:'A11', 95:'A12', 45:'A12', 43:'A13', 61:'A13', 8:'A14', 
                9:'B1', 81:'B2', 113:'B2', 87:'B3', 119:'B3', 69:'B4', 101:'B4', 82:'B5', 114:'B5', 84:'B6', 116:'B6', 89:'B7', 121:'B7', 85:'B8', 117:'B8', 
                73:'B9', 105:'B9', 79:'B10', 111:'B10', 80:'B11', 112:'B11', 123:'B12', 91:'B12', 125:'B13', 93:'B13', 124:'B14', 92:'B14', 
                20:'C1', 65:'C2', 97:'C2', 83:'C3', 115:'C3', 68:'C4', 100:'C4', 70:'C5', 102:'C5', 71:'C6', 103:'C6', 72:'C7', 104:'C7', 74:'C8', 106:'C8', 
                75:'C9', 107:'C9', 76:'C10', 108:'C10', 58:'C11', 59:'C11', 34:'C12', 39:'C12', 13:'C13', 16:'D1', 90:'D2', 122:'D2', 88:'D3', 120:'D3', 
                67:'D4', 99:'D4', 86:'D5', 118:'D5', 66:'D6', 98:'D6', 78:'D7', 110:'D7', 77:'D8', 109:'D8', 60:'D9', 44:'D9', 62:'D10', 46:'D10', 63:'D11', 
                47:'D11', 16:'D12', 17:'E1', 18:'E3', 32:'E4', 18:'E5', 17:'E8'}

#timestamps stripped out, metadata can be recycled later or removed later if necessary
def findStrokes(strokes):
    keystrokes = []
    #results in an empty token at the end of tokens list, must be removed
    tokens = strokes[:-1].split("|")
    for token in tokens:
        key_data = token.split()
        #changed the tuple keycode values into ints instead of strings
        keystrokes.append(int(key_data[0]))
    return keystrokes

#increases weight for correct press, decrease key weights for mistakes (based upon deletes)
#weight for delete? decreases for unnecessary deletes
def findKeyWeights(strokes, layout):
    weights = {}
    delete = 8
    count = 0
    for i in range(len(strokes)):
        if strokes[i] == delete:
            count +=1
        elif (count > 0):
            for h in range(count):
                index = i - (count + h + 1)
                if index >= 0:
                    devalued = layout[strokes[index]]
                    weights[devalued] -= 1
                else:
                    weights[layout[delete]] -= 1
            count = 0
        key = layout[strokes[i]]
        weights[key] = weights.get(key, 0) + 1
    return weights

#by key value instead of location, different values for upper/lowercase letters
#figure out what to do with shifts later
def findBigrams(keystrokes):
    bigrams = []
    for i in range(len(keystrokes)):
        if (i + 1) < len(keystrokes):
            bigrams.append((keystrokes[i], keystrokes[i + 1]))
    return bigrams

def findBigramFreq(bigrams):
    freq = {}
    for bigram in bigrams:
        freq[bigram] = freq.get(bigram, 0) + 1
    return freq

def placeKeys(bigram_freq):
    keyboard = []

    return keyboard

# #optimal is defined by vector placement, costs v benefits ...right now just homerow placement of most freq bigrams
# def find_opt_keyboard(keyboards):
#     best = []
#     return best

# def dvorak_priority(keystrokes):
#     frequencies = findBigramFreq(findBigrams(findStrokes(keystrokes)))
#     all_keyboards = []
#     #find all possible unique keyboard layout variations, need to replace .... use genetic algo?
#     for i in range(100):
#         keyboard = placeKeys(frequencies)
#         all_keyboards.append(keyboard)
#     return find_opt_keyboard(all_keyboards)

#MISC analytics

def ms_to_s(time):
    return float(time)/float(1000)

def calc_avg_times(strokes):
    keycodes = { '20': 'CAPS', '8': 'DELETE', '120': 'x', '121': 'y', '122': 'z', '123': '{', '124': '|', '125': '}', '126': '~', '118': 'v', '59': ';', 
            '58': ';', '55': '7', '54': '6', '57': '9', '56': '8', '51': '3', '50': '2', '53': '5', '52': '4', 'x': 'META', '115': 's', '114': 'r', 
            '117': 'u', '116': 't', '111': 'o', '110': 'n', '113': 'q', '112': 'p', '82': 'R', '83': 'S', '80': 'P', '81': 'Q', '119': 'w', '87': 'W', 
            '84': 'T', '85': 'U', '108': 'l', '109': 'm', '102': 'f', '103': 'g', '100': 'd', '101': 'e', '106': 'j', '107': 'k', '104': 'h',
            '105': 'i', '39': "'", '38': '&', '33': '!', '32': 'SPACE', '37': '%', '36': '$', '35': '#', '34': '"', '60': '<', '61': '=', '62': '>', 
            '63': '?', '64': '@', '65': 'A', '66': 'B', '67': 'C', '68': 'D', '69': 'E', '99': 'c', '98': 'b', '91': '[', '90': 'Z', '93': ']',
             '92': '\\', '95': '_', '94': '^', '97': 'a', '96': '`', '13': 'ENTER', '17': 'CTRL', '16': 'SHIFT', '18': 'ALT', '88': 'X', '89': 'Y', 
             '48': '0', '49': '1', '46': '.', '86': 'V', '44': ',', '45': '-', '42': '*', '43': '+', '40': '(', '41': ')', '9': 'TAB', '77': 'M', 
             '76': 'L', '75': 'K', '74': 'J', '73': 'I', '72': 'H', '71': 'G', '70': 'F', '79': 'O', '78': 'N', '47': '/'}
    key_times = {}
    
    sessions = strokes[:-1].split("*")
    for session in sessions:
        print session
        tokens = session[:-1].split("|")
        prev_time = 0

        for i in range(len(tokens)):
            key = tokens[i].split()
            key_code = int(key[0])
            if i == 0:
                #should I change the zero to another time...?
                timestamp = 0
            else:
                timestamp = abs(prev_time - ms_to_s(int(key[1])))
            if key_times.has_key(key_code):
                key_times[key_code].append(timestamp)
            else:
               key_times[key_code] = [timestamp]
            prev_time = ms_to_s(int(key[1]))
        
    avg_times = {}
    for key in key_times:
        total = 0
        for time in key_times[key]:
            total += time
        keycode = keycodes[str(key)]
        avg_times[keycode] = '%.2f' % (total/len(key_times[key]))
    return avg_times