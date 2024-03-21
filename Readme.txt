## Readme
## A script that prompts the user for a script path to traverse for jpg files (File header FF D8) before returning its SHA256 hash, and file attributes
## Author: Munashe Zanza

##~Running file~##
- To execute the file run the command 'python3 JPGHash.py'. Note: This will run the script using python3, if you're using another version then replace the '3' with the version you're using.
-When prompted, enter the path to the directory that you want to traverse for .jpg files
-The path must point to a directory that contains the files and not to the files themselves

##~Output~##
- After running the script, the location of the output file will be printed in the command line. This location is usually in the same folder as the script itself
- This script is capable of detecting appended data in case of steganography and generating a hash with and without the appended data

##~Modules Used in Script~##
- os
- datetime
- hashlib
- base64
- binascii
- base64
