#KEY MAPS
visual_value = { 20: 'CAPS', 8: 'DELETE', 120: 'x', 121: 'y', 122: 'z', 123: '{', 124: '|', 125: '}', 126: '~', 118: 'v', 59: ';', 
        58: ';', 55: '7', 54: '6', 57: '9', 56: '8', 51: '3', 50: '2', 53: '5', 52: '4', 115: 's', 114: 'r', 
        117: 'u', 116: 't', 111: 'o', 110: 'n', 113: 'q', 112: 'p', 82: 'R', 83: 'S', 80: 'P', 81: 'Q', 119: 'w', 87: 'W', 
        84: 'T', 85: 'U', 108: 'l', 109: 'm', 102: 'f', 103: 'g', 100: 'd', 101: 'e', 106: 'j', 107: 'k', 104: 'h',
        105: 'i', 39: "'", 38: '&', 33: '!', 32: 'SPACE', 37: '%', 36: '$', 35: '#', 34: '"', 60: '<',61: '=', 62: '>', 
        63: '?', 64: '@', 65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 99: 'c', 98: 'b', 91: '[', 90: 'Z', 93: ']',
        92: '\\', 95: '_', 94: '^', 97: 'a', 96: '`', 13: 'ENTER', 17: 'CTRL', 16: 'SHIFT', 18:'ALT',88: 'X',89: 'Y', 
        48: '0', 49: '1', 46: '.', 86: 'V', 44: ',', 45: '-', 42: '*', 43: '+', 40: '(', 41: ')', 9:'TAB', 77:'M', 
        76: 'L', 75: 'K', 74: 'J', 73: 'I', 72: 'H', 71: 'G', 70: 'F', 79: 'O', 78: 'N', 47: '/'}

key_divs = {96:"tilde", 126:"tilde", 33:"one", 49:"one", 50:"two", 64:"two", 35:"three", 
        51:"three", 52:"four", 53:"five", 37:"five", 54:"six", 94:"six", 55:"seven", 
        38:"seven", 42:"eight", 56:"eight", 57:"nine", 40:"nine", 48:"zero", 41:"zero", 
        36:"four", 45:"dash", 95:"dash", 43:"plus", 61:"plus", 8:"delete", 9:"tab", 
        13:"enter", 16:"shift", 17:"control", 18:"alt", 20:"caps",
        32:"space", 97:"A", 65:"A", 113:"Q", 81:"Q", 119:"W", 87:"W", 101:"E", 69:"E", 114:"R",
        82:"R", 116:"T", 84:"T", 89:"Y", 121:"Y", 85:"U", 117:"U", 73:"I", 105:"I", 80:"P", 
        112:"P", 123:"brace_open", 91:"brace_open", 93:"brace_close", 125:"brace_close", 
        124:"pipe", 92:"pipe", 111:"O", 79:"O", 98:"B", 66:"B", 115:"S", 83:"S", 100:"D", 
        68:"D", 102:"F", 70:"F", 103:"G", 71:"G", 104:"H", 72:'H', 74:'J', 106:'J', 107:'K', 
        75:'K', 76:'L', 108:'L', 77:'M', 109:'M', 59:"colon", 58:'colon', 39:'quote', 
        34:'quote', 122:"Z", 90:"Z", 120:"X", 88:"X", 99:"C", 67:"C", 118:"V", 86:"V", 110:"N",
        78:"N", 60:"comma", 44:"comma", 62:"period", 46:"period", 63:"question", 47:"question"}
div_to_value = {"tilde":["~", '`'], "one":['!', '1'], 'two':['@', '2'], 'three':['#', '3'], 'four':['$', '4'], 
            'five':['%', '5'], 'six':['^', '6'], 'seven':['&', '7'], 'eight':['*', '8'], 'nine':['(', '9'], 
            'zero':[')', '0'], 'dash':['_', '-'], 
            'plus':['+', '='], 'delete':['DELETE'],'tab':['TAB'], 'Q':['Q'], 'W':['W'], 'E':['E'], 'R':['R'], 'T':['T'], 'Y':['Y'], 
            'U':['U'], 'I':['I'], 'O':['O'], 'P':['P'], 'brace_open':['{', '['], 'brace_close':['}', ']'],
            'pipe':['|', '\\'], 'caps':['CAPS'], 'A':['A'], 'S':['S'], 'D':['D'], 'F':['F'], 'G':['G'], 'H':['H'], 'J':['J'], 
            'K':['K'], 'L':['L'], 'colon':[':', ';'], 'quote':['"', "'"], 'enter':['ENTER'], 'shift':['SHIFT'], 'Z':['Z'], 'X':['X'], 
            'C':['C'], 'V':['V'], 'B':['B'], 'N':['N'], 'M':['M'], 'comma':['<', ','], 'period':['>', '.'], 'question':['?', '/'], 
            'control':['CONTROL'], 'alt':['ALT'], 'space':['SPACE']}

def CSSkeyboard(keyboard):
    css = []
    for key in keyboard:
        css.append((key[0], div_to_value[key[1]]))
    return css


#ANALYTICS GENERATION

def parseKeystrokes(strokes):
    keystrokes = []
    #parses out input for each individual prompt response
    responses = strokes[:-1].split("*")    
    for response in responses:
        tokens = response[:-1].split("|")
        for token in tokens:
            key_data = token.split()
            keystrokes.append(int(key_data[0]))
    return keystrokes

def keyFreq(keystrokes):
    freq = {}
    for key in keystrokes:
        freq[visual_value[key]] = freq.get(visual_value[key], 0) + 1
    return freq

def keyMistakes(keystrokes):
    #keycode for delete is 8
    delete = 8
    count = 0
    mistakes = {}
    for i in range(len(keystrokes)):
        if ((count > 0) and (keystrokes[i] != delete)) or (i == len(keystrokes) + 1):
            for h in range(count):
                index = i - (count + h + 1)
                if index >= 0:
                    mistake = visual_value[keystrokes[index]]
                    mistakes[mistake] += 1
                else:
                    mistakes[visual_value[delete]] += 1
        if keystrokes[i] == delete:
            count += 1
        key = visual_value[keystrokes[i]]
        mistakes[key] = mistakes.get(key, 0)
    return mistakes

def ms_to_s(time):
    return float(time)/float(1000)

def avgTimes(strokes):
    key_times = {}
    
    responses = strokes[:-1].split("*")
    for response in responses:
        tokens = response[:-1].split("|")
        prev_time = 0

        for i in range(len(tokens)):
            key = tokens[i].split()
            key_code = int(key[0])
            timestamp = key[1]
            if i == 0:
                time = 0
            else:
                time = abs(prev_time - ms_to_s(timestamp))
            if key_times.has_key(key_code):
                key_times[key_code].append(time)
            else:
               key_times[key_code] = [time]
            prev_time = ms_to_s(timestamp)
        
    avg_times = {}
    for key in key_times:
        total = 0
        for time in key_times[key]:
            total += time
        keyvalue = visual_value[key]
        avg_times[keyvalue] = '%.2f' % (total/len(key_times[key]))
    return avg_times

def createAnalytics(strokes):
    keystrokes = parseKeystrokes(strokes)
    frequencies = keyFreq(keystrokes)
    mistakes = keyMistakes(keystrokes)
    average_times = avgTimes(strokes)
    return frequencies, mistakes, average_times

#KEYBOARD GENERATION

def bigramFreq(keystrokes):
    freq = {}
    for i in range(len(keystrokes)):
        if (i + 1) < len(keystrokes):
            bigram = (keystrokes[i], keystrokes[i+1])
            freq[bigram] = freq.get(bigram, 0) + 1
    return freq    

def createKeyboard(strokes):
    #key values ordered from most frequently typed to least
    common_keys = ['space', "E", "T", "shift", 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'delete', 'L', 'D', 'C', 'U', 'enter', 'M', 'F', 'P', 'G', 'W', 'Y', 'B', 'comma', 'period', 'V',
            'K', 'nine', 'zero', 'dash', 'colon', 'quote', 'plus', 'tab', 'X', 'question', 'four', 'eight', 'one', 'J', 'brace_open', 'brace_close', 'Q', "two", 'Z', 'five',
            'three', 'pipe', 'six', 'seven', 'tilde', "control", "alt", 'caps']

    bigram_freq = bigramFreq(parseKeystrokes(strokes))
    reversed_bigrams = []
    for x in bigram_freq:
        reversed_bigrams.append((bigram_freq[x], x))
    sorted_bigrams = sorted(reversed_bigrams, reverse=True)

    dvorak_keyboard = []
    for x, y in sorted_bigrams:
        for i in y:
            if key_divs[i] not in dvorak_keyboard:
                dvorak_keyboard.append(key_divs[i])
    if len(dvorak_keyboard) < len(common_keys):
        for h in common_keys:
            if h not in dvorak_keyboard:
                dvorak_keyboard.append(h)

    #the corresponding location map, highest priority to lowest| removed D12 - shift, E8 - ctrl, E5 - alt
    dvorak_map = ['C06', 'C05', 'C07', 'C04', 'C08', 'C03', 'C09', 'C02', 'C10', 'C01', 'C11', 'C12', 'C13', 'B06', 'B05', 'B07', 'B04', 'B08', 'B03', 'B09', 'B02', 'B10', 'B01', 'B11', 
                'B12', 'B13', 'B14', 'D07', 'D06', 'D08', 'D05', 'D09', 'D04', 'D10', 'D03', 'D11', 'D02', 'D01', 'E04', 'A08', 'A07', 'A06', 'A09', 
                'A05', 'A10', 'A04', 'A11', 'A03', 'A12', 'A02', 'A13', 'A01', 'A14', 'E03', 'E01']

    return sorted(zip(dvorak_map, dvorak_keyboard))