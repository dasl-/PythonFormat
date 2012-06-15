#use this script to run the formatter via terminal

import python_beautifier
from sys import argv

script, input_file_name, output_file_name = argv

output_file = open(output_file_name, 'w')

input_file = open(input_file_name)

result = python_beautifier.beautify(input_file.read())

output_file.write(result)

output_file.close()