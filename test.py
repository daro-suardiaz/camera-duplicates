from fuzzywuzzy import fuzz
from pprint import pprint
import roman
import re

""" 
1) get a list of unique values
2) fix those values 
"""


def normalize_string(input_string):
    """
    
    As we have several variations of the Canon Mark models we have to clean it up
    
    1) break down the input string into tokens
    2) check if one of those tokens is a variation of "Mark" (i.e. mark, mk, MarkIII, 5dmark, etc)
    3) check if the mark model number is in roman and covert it to INT
    4) eliminating spaces and lowering case
    """
    
    tokens = [t for t in input_string.split()]
    normalized_tokens = []
    lookup_pattern = re.compile("(m(?:ar)?k\s*)([ivx\d]*)", flags=re.IGNORECASE)
    roman_nums = roman.romanNumeralPattern

    for i, token in enumerate(tokens, 0):
        
        # check if the token is a variation of mark
        lookup = lookup_pattern.search(token)
        if lookup:
            # some strings have the 5d concatenated to the model, let's separate it
            if re.search('5d', token, re.IGNORECASE):
                token = '5D Mark'
            else:
                token = 'Mark'
            model_nbr = lookup.group(2)
            
            # check if the model number is part of the same token and covert it to ,INT
            if model_nbr != '':
                model_nbr = roman.fromRoman(model_nbr)
                token = token+' '+str(model_nbr)
        
        # check if the token is a roman numeral and covert it to INT
        is_roman = roman_nums.search(token)
        if is_roman:
            token = str(roman.fromRoman(token))

        normalized_tokens.append(token)
    
    # convert the list of normalized tokens into a single string
    output_string = ' '.join(normalized_tokens)
    output_string = output_string.strip()
    output_string = output_string.lower()
    output_string = output_string.replace(" ","")
    return output_string



cameras = [ 'Canon 5dMKII',
            'Canon 5D mark II',
            'Canon 5d MKII',
            'Canon 5d MKII',
            'Canon 5D mkIII',
            'Canon 5D mk III']

word_freq = dict()

for camera in cameras:
    normalized_camera = normalize_string(camera)
    

    if normalized_camera not in word_freq.keys():
        new_camera = None
        new_camera = {normalized_camera: {camera: 1}}
        word_freq.update(new_camera)
    else:
        if camera not in word_freq[normalized_camera].keys():
            new_value = None
            new_value = {camera: 1}
            word_freq[normalized_camera].update(new_value)
        else:
            word_freq[normalized_camera][camera] += 1
    
pprint(word_freq)






