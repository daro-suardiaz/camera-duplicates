import roman
import re
from pprint import pprint

class CamerasSanitizer():
    
    def __init__(self, input_file):
        self.cameras = input_file
        self.word_freq = dict()
        self.cameras_mapping_dict = dict()
        self.sanitized_values = dict()
        


    def weight_variations(self):
        """
        Builds a dictionary of normalized camera names with all its different variations
        and weights them.
        
        :return: a dictionary of unique normalized camera names and the most used variation
        """

        for camera in self.cameras:

            # first we normalize the string
            normalized_camera = self.normalize_string(camera)
            
            # check if the normalized string is already a key in the dictionary of unique values
            if normalized_camera not in self.word_freq.keys():
                
                # check if the normalized string is a substring of an existing key
                is_substring = False
                for key in self.word_freq.keys():
                    if re.search(normalized_camera, key):
                        normalized_camera = key
                        # check if the variation of the camera is registered
                        self._check_camera_variation(camera, normalized_camera)
                        is_substring = True

                # if it's not a substring, then it's a new value
                if is_substring == False:
                    new_camera = None
                    new_camera = {normalized_camera: {camera: 1}}
                    self.word_freq.update(new_camera)
            
            else:
                self._check_camera_variation(camera, normalized_camera)
        
        return self.get_most_used_variations()



    def normalize_string(self, input_string):
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
                    if model_nbr.isdigit():
                        pass
                    else:
                        model_nbr = roman.fromRoman(model_nbr.upper())
                        token = token+' '+str(model_nbr)
            
            # check if the token is a roman numeral and covert it to INT
            is_roman = roman_nums.search(token)
            if is_roman:
                token = str(roman.fromRoman(token))

            normalized_tokens.append(token)
        
        # convert the list of normalized tokens into a single string and normalize it
        output_string = ' '.join(normalized_tokens)
        output_string = output_string.strip()
        output_string = output_string.lower()
        output_string = output_string.replace(" ","")
        return output_string



    def _check_camera_variation(self, camera, normalized_camera):
        """
        Checks if a given camera name is registered as a variaton of a normalized name
        
        :param: camera model
        :param: normalized string representing that camera model
        """
        if camera not in self.word_freq[normalized_camera].keys():
                new_value = None
                new_value = {camera: 1}
                self.word_freq[normalized_camera].update(new_value)
        else:
            self.word_freq[normalized_camera][camera] += 1





    def get_most_used_variations(self):
        """
        Calculates the key with the highest value in the inner dict of variations for a camera
        and creates a mapping dictionary with normalized names (k) and most used variation (v)

        :param: a dictionary of normalized camera names with weighted variations
        """
        for key, value in self.word_freq.items():
            value_dict = value
            most_used_name = max(value_dict, key=lambda key: value_dict[key])
            self.cameras_mapping_dict[key] = most_used_name
    


    def sanitize_cameras(self):
        """
        Sanitizes the list of cameras with the most used value from the mappings dict
        and populates a dictionary with all the replacements occurred
        """
        for camera in self.cameras:
            normalized_string = self.normalize_string(camera)
        
            for key in self.cameras_mapping_dict.keys():
                if re.search(normalized_string, key):
                    normalized_string = key
            
            if camera != self.cameras_mapping_dict[normalized_string]:
                
                if camera not in self.sanitized_values.keys():
                    new_mapping = {camera: self.cameras_mapping_dict[normalized_string]}
                    self.sanitized_values.update(new_mapping)