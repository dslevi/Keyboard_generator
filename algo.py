
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

def findBigramFreq(bigrams):
    freq = {}
    for bigram in bigrams:
        freq[bigram] = freq.get(bigram, 0) + 1
    return freq

def placeKeys(strokes):
    bigram_freq = findBigramFreq(findBigrams(findStrokes(strokes)))

    keys = {96:"tilde", 126:"tilde", 33:"one", 49:"one", 50:"two", 64:"two", 35:"three", 
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

    common = ['space', "E", "T", "shift", 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'delete', 'L', 'D', 'C', 'U', 'enter', 'M', 'F', 'P', 'G', 'W', 'Y', 'B', 'comma', 'period', 'V',
            'K', 'nine', 'zero', 'dash', 'colon', 'quote', 'plus', 'tab', 'X', 'question', 'four', 'eight', 'one', 'J', 'brace_open', 'brace_close', 'Q', "two", 'Z', 'five',
            'three', 'pipe', 'six', 'seven', 'tilde', "control", "alt", 'caps']

    #Dvorak principles - home row prioritized, bigrams split to different hands
    bigrams = []
    for x in bigram_freq:
        bigrams.append((bigram_freq[x], x))
    sorted_bigrams = sorted(bigrams, reverse=True)

    dvorak_keyboard = []
    for x, y in sorted_bigrams:
        for i in y:
            if keys[i] not in dvorak_keyboard:
                dvorak_keyboard.append(keys[i])

    if len(dvorak_keyboard) < len(common):
        for h in common:
            if h not in dvorak_keyboard:
                dvorak_keyboard.append(h)
    
    #the corresponding location map, highest priority to lowest| removed D12 - shift, E8 - ctrl, E5 - alt
    dvorak_map = ['C06', 'C05', 'C07', 'C04', 'C08', 'C03', 'C09', 'C02', 'C10', 'C01', 'C11', 'C12', 'C13', 'B06', 'B05', 'B07', 'B04', 'B08', 'B03', 'B09', 'B02', 'B10', 'B01', 'B11', 
                'B12', 'B13', 'B14', 'D07', 'D06', 'D08', 'D05', 'D09', 'D04', 'D10', 'D03', 'D11', 'D02', 'D01', 'E04', 'A08', 'A07', 'A06', 'A09', 
                'A05', 'A10', 'A04', 'A11', 'A03', 'A12', 'A02', 'A13', 'A01', 'A14', 'E03', 'E01']

    keyboard = sorted(zip(dvorak_map, dvorak_keyboard))

    return keyboard












s = "103 1383963698624|104 1383963698645|105 1383963699270|106 1383963699341|97 1383963699445|102 1383963699454|115 1383963699525|107 1383963699565|100 1383963699581|102 1383963699669|107 1383963699781|106 1383963699791|104 1383963699885|102 1383963699901|98 1383963700070|110 1383963700342|108 1383963700477|107 1383963700492|120 1383963700733|99 1383963700742|122 1383963700758|118 1383963700862|104 1383963700917|107 1383963701061|106 1383963701077|98 1383963701181|97 1383963701302|106 1383963701365|102 1383963701453|104 1383963701485|97 1383963701661|115 1383963701676|100 1383963701695|104 1383963701703|102 1383963701773|107 1383963701829|100 1383963701941|115 1383963701965|102 1383963702013|106 1383963702109|115 1383963702150|100 1383963702166|108 1383963702221|102 1383963702230|104 1383963702485|101 1383963702565|108 1383963702685|108 1383963702839|111 1383963702963|32 1383963703052|116 1383963703116|104 1383963703157|101 1383963703190|114 1383963703293|101 1383963703365|32 1383963703468|109 1383963703605|121 1383963703766|32 1383963703828|110 1383963703974|97 1383963704029|109 1383963704125|101 1383963704197|32 1383963704244|105 1383963704365|100 1383963704438|32 1383963704540|8 1383963705133|8 1383963705292|115 1383963705629|32 1383963705740|100 1383963705909|97 1383963705965|110 1383963706013|105 1383963706133|101 1383963706173|108 1383963706309|108 1383963706461|101 1383963706493|32 1383963706599|119 1383963706805|104 1383963706885|97 1383963706949|116 1383963707005|32 1383963707060|105 1383963707101|115 1383963707190|32 1383963707276|121 1383963707324|111 1383963707405|117 1383963707502|114 1383963707525|32 1383963707653|110 1383963707813|97 1383963707838|109 1383963707982|101 1383963708021|63 1383963708237|"
    bigrams = []
    for i in range(len(keystrokes)):
        if (i + 1) < len(keystrokes):
            bigrams.append((keystrokes[i], keystrokes[i + 1]))
    return bigrams

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
