from CamerasSanitizer import FileSanitizer
from pprint import pprint


cameras = open('duplicates.txt', 'r')

Sanitizer = FileSanitizer(cameras)

Sanitizer.weight_variations()
pprint(Sanitizer.word_freq)
pprint(Sanitizer.cameras_mapping_dict)


Sanitizer.sanitize_cameras()
pprint(Sanitizer.sanitized_values)