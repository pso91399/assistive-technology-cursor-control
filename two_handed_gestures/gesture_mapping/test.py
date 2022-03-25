import os
import re

def list_file_paths(directory):
    return [os.path.join(directory,file) for file in os.listdir(directory)]


files = list_file_paths('input_image')
pattern = r'\/(\w+).'
output = re.findall(pattern, files[0])[0]

path = re.findall(r'\_(\w+)', output)
print(output)
print(path)