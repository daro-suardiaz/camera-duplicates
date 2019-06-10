from fuzzywuzzy import fuzz
import roman
import re

""" 
1) get a list of unique values
2) fix those values 
"""


def normalize_marks(input_string):
    """
    As we have several variations of the Canon Mark models, let's try to clean ip up
    
    1) break down the input string into tokens
    2) check if one of those tokens is a variation of "Mark" (i.e. mark, mk, MarkIII, etc)
    3) check if the mark model number is in roman and covert it to INT
    """
    
    tokens = [t for t in input_string.split()]
    normalized_tokens = []
    lookup_pattern = re.compile("(m(?:ar)?k\s*)([ivx\d]*)", flags=re.IGNORECASE)
    roman_nums = roman.romanNumeralPattern

    for i, token in enumerate(tokens, 0):
        
        # check if the token is a variation of mark
        lookup = lookup_pattern.search(token)
        if lookup:
            token =  'Mark'
            model_nbr = lookup.group(2)
            
            # check if the model number is part of the same token and covert it to INT
            if model_nbr != '':
                model_nbr = roman.fromRoman(model_nbr)
                token = token+' '+str(model_nbr)
        
        # check if the token is a roman numeral and covert it to INT
        is_roman = roman_nums.search(token)
        if is_roman:
            token = roman.fromRoman(token)

        normalized_tokens.append(token)
    
    # convert the list of normalized tokens into a single string
    output_string = ' '.join(normalized_tokens)
    return output_string


def normalize_text(input_string):
    """
    Simple text normalization by eliminating spaces and lowering case
    """
    output_string = input_string.strip()
    output_string = input_string.lower()
    output_string = input_string.replace(" ","")
    return output_string

    
    
    
    




cameras = [ 'Canon 5D mkIII',
            'Canon 5D mark II',
            'Canon 5d MKII',
            'Canon 5dMKII',
            'Canon 5D Mk III']

for camera in cameras:
    normalized_camera = normalize_marks(camera)
    normalized_camera = normalize_text(camera)
    
    



test = None

word_freq = dict()

if camera not in word_freq.keys():
    word_freq[camera] = 1
else:
    word_freq[camera] += 1
print(word_freq)











print('Reference: %s' % camera)
print('Test: %s' % test)

ratio = fuzz.token_sort_ratio(camera, test)
print(ratio)





