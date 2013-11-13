
visual_value = { 20: 'CAPS', 8: 'DELETE', 120: 'x', 121: 'y', 122: 'z', 123: '{', 124: '|', 125: '}', 126: '~', 118: 'v', 59: ';', 
        58: ';', 55: '7', 54: '6', 57: '9', 56: '8', 51: '3', 50: '2', 53: '5', 52: '4', 115: 's', 114: 'r', 
        117: 'u', 116: 't', 111: 'o', 110: 'n', 113: 'q', 112: 'p', 82: 'R', 83: 'S', 80: 'P', 81: 'Q', 119: 'w', 87: 'W', 
        84: 'T', 85: 'U', 108: 'l', 109: 'm', 102: 'f', 103: 'g', 100: 'd', 101: 'e', 106: 'j', 107: 'k', 104: 'h',
        105: 'i', 39: "'", 38: '&', 33: '!', 32: 'SPACE', 37: '%', 36: '$', 35: '#', 34: '"', 60: '<',61: '=', 62: '>', 
        63: '?', 64: '@', 65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 99: 'c', 98: 'b', 91: '[', 90: 'Z', 93: ']',
        92: '\\', 95: '_', 94: '^', 97: 'a', 96: '`', 13: 'ENTER', 17: 'CTRL', 16: 'SHIFT', 18:'ALT',88: 'X',89: 'Y', 
        48: '0', 49: '1', 46: '.', 86: 'V', 44: ',', 45: '-', 42: '*', 43: '+', 40: '(', 41: ')', 9:'TAB', 77:'M', 
        76: 'L', 75: 'K', 74: 'J', 73: 'I', 72: 'H', 71: 'G', 70: 'F', 79: 'O', 78: 'N', 47: '/'}

def keyMistakes(keystrokes):
    #keycode for delete is 8
    delete = 8
    count = 0
    mistakes = {}

    for i in range(len(keystrokes)):
        print i, keystrokes[i]
        if keystrokes[i] == delete:
            count += 1
            print "count increased: ", count
        elif (count > 0):
            print "decreasing begins ", count
            for h in range(count):
                index = i - (count + h + 1)
                if index >= 0:
                    mistake = visual_value[keystrokes[index]]
                    mistakes[mistake] += 1
                else:
                    mistakes[visual_value[delete]] += 1
            count = 0
        key = visual_value[keystrokes[i]]
        mistakes[key] = mistakes.get(key, 0)
    if (count > 0):
        for h in range(count):
            index = i - (count + h)
            print count
            if index >= 0:
                mistake = visual_value[keystrokes[index]]
                mistakes[mistake] += 1
            else:
                mistakes[visual_value[delete]] += 1
    return mistakes





keystrokes = [100, 8, 100, 8, 100, 8]
print keyMistakes(keystrokes)





