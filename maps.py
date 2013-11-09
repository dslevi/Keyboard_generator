keycodes = { '20': 'CAPS', '8': 'DELETE', '120': 'x', '121': 'y', '122': 'z', '123': '{', '124': '|', '125': '}', '126': '~', '118': 'v', '59': ';', 
        '58': ';', '55': '7', '54': '6', '57': '9', '56': '8', '51': '3', '50': '2', '53': '5', '52': '4', 'x': 'META', '115': 's', '114': 'r', 
        '117': 'u', '116': 't', '111': 'o', '110': 'n', '113': 'q', '112': 'p', '82': 'R', '83': 'S', '80': 'P', '81': 'Q', '119': 'w', '87': 'W', 
        '84': 'T', '85': 'U', '108': 'l', '109': 'm', '102': 'f', '103': 'g', '100': 'd', '101': 'e', '106': 'j', '107': 'k', '104': 'h',
        '105': 'i', '39': "'", '38': '&', '33': '!', '32': 'SPACE', '37': '%', '36': '$', '35': '#', '34': '"', '60': '<', '61': '=', '62': '>', 
        '63': '?', '64': '@', '65': 'A', '66': 'B', '67': 'C', '68': 'D', '69': 'E', '99': 'c', '98': 'b', '91': '[', '90': 'Z', '93': ']',
         '92': '\\', '95': '_', '94': '^', '97': 'a', '96': '`', '13': 'ENTER', '17': 'CTRL', '16': 'SHIFT', '18': 'ALT', '88': 'X', '89': 'Y', 
         '48': '0', '49': '1', '46': '.', '86': 'V', '44': ',', '45': '-', '42': '*', '43': '+', '40': '(', '41': ')', '9': 'TAB', '77': 'M', 
         '76': 'L', '75': 'K', '74': 'J', '73': 'I', '72': 'H', '71': 'G', '70': 'F', '79': 'O', '78': 'N', '47': '/'}

keys = {96:"tilde", 126:"tilde", 33:"one", 49:"one", 50:"two", 64:"two", 35:"three", 
    51:"three", 52:"four", 53:"five", 37:"five", 54:"six", 94:"six", 55:"seven", 
    38:"seven", 42:"eight", 56:"eight", 57:"nine", 40:"nine", 48:"zero", 41:"zero", 
    36:"four", 45:"dash", 95:"dash", 43:"plus", 61:"plus", 8:"delete", 9:"tab", 
    13:"enter", 16:"shift_left", 17:"control_left", 18:"alt_left", 20:"caps",
    32:"space", 97:"A", 65:"A", 113:"Q", 81:"Q", 119:"W", 87:"W", 101:"E", 69:"E", 114:"R",
    82:"R", 116:"T", 84:"T", 89:"Y", 121:"Y", 85:"U", 117:"U", 73:"I", 105:"I", 80:"P", 
    112:"P", 123:"brace_open", 91:"brace_open", 93:"brace_close", 125:"brace_close", 
    124:"pipe", 92:"pipe", 111:"O", 79:"O", 98:"B", 66:"B", 115:"S", 83:"S", 100:"D", 
    68:"D", 102:"F", 70:"F", 103:"G", 71:"G", 104:"H", 72:'H', 74:'J', 106:'J', 107:'K', 
    75:'K', 76:'L', 108:'L', 77:'M', 109:'M', 59:"colon", 58:'colon', 39:'quote', 
    34:'quote', 122:"Z", 90:"Z", 120:"X", 88:"X", 99:"C", 67:"C", 118:"V", 86:"V", 110:"N",
    78:"N", 60:"comma", 44:"comma", 62:"period", 46:"period", 63:"question", 47:"question"}

#removed D12 - shift, E8 - ctrl, E5 - alt
qwerty_map = { 126:'A1', 96:'A1', 33:'A2', 49:'A2', 64:'A3', 50:'A3', 35:'A4', 51:'A4', 36:'A5', 52:'A5', 37:'A6', 53:'A6', 94:'A7', 54:'A7', 38:'A8', 
                55:'A8', 42:'A9', 56:'A9', 40:'A10', 57:'A10', 41:'A11', 48:'A11', 95:'A12', 45:'A12', 43:'A13', 61:'A13', 8:'A14', 
                9:'B1', 81:'B2', 113:'B2', 87:'B3', 119:'B3', 69:'B4', 101:'B4', 82:'B5', 114:'B5', 84:'B6', 116:'B6', 89:'B7', 121:'B7', 85:'B8', 117:'B8', 
                73:'B9', 105:'B9', 79:'B10', 111:'B10', 80:'B11', 112:'B11', 123:'B12', 91:'B12', 125:'B13', 93:'B13', 124:'B14', 92:'B14', 
                20:'C1', 65:'C2', 97:'C2', 83:'C3', 115:'C3', 68:'C4', 100:'C4', 70:'C5', 102:'C5', 71:'C6', 103:'C6', 72:'C7', 104:'C7', 74:'C8', 106:'C8', 
                75:'C9', 107:'C9', 76:'C10', 108:'C10', 58:'C11', 59:'C11', 34:'C12', 39:'C12', 13:'C13', 16:'D1', 90:'D2', 122:'D2', 88:'D3', 120:'D3', 
                67:'D4', 99:'D4', 86:'D5', 118:'D5', 66:'D6', 98:'D6', 78:'D7', 110:'D7', 77:'D8', 109:'D8', 60:'D9', 44:'D9', 62:'D10', 46:'D10', 63:'D11', 
                47:'D11', 17:'E1', 18:'E3', 32:'E4'}


#the placements left to right with highest priority, key values are placed here
dvorak_priorites = []
#the corresponding location value for the qwerty map, removed D12 - shift, E8 - ctrl, E5 - alt
dvorak_map = ['C6', 'C5', 'C7', 'C4', 'C8', 'C3', 'C9', 'C2', 'C10', 'C1', 'C11', 'C12', 'C13', 'B6', 'B5', 'B7', 'B4', 'B8', 'B3', 'B9', 'B2', 'B10', 'B1', 'B11', 
                'B12', 'B13', 'B14', 'D7', 'D6', 'D8', 'D5', 'D9', 'D4', 'D10', 'D3', 'D11', 'D2', 'D1', 'E4', 'A8', 'A7', 'A6', 'A9', 
                'A5', 'A10', 'A4', 'A11', 'A3', 'A12', 'A2', 'A13', 'A4', 'A14', 'E3', 'E1']

common = ["space", "E", "T", "shift", 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'delete', 'L', 'D', 'C', 'U', 'enter', 'M', 'F', 'P', 'G', 'W', 'Y', 'B', 'comma', 'period', 'V',
            'K', 'nine', 'zero', 'dash', 'colon', 'quote', 'plus', 'tab', 'X', 'question', 'four', 'eight', 'one', 'J', 'brace_open', 'brace_close', 'Q', "two", 'Z', 'five',
            'three', 'pipe', 'six', 'seven', 'tilde', "control", "alt", 'caps']
