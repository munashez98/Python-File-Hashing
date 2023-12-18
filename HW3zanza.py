# import modules that will be used in the script
try:
    import os
    import datetime as dt
    from hashlib import sha256
    import base64
    import binascii
    import base64
except ImportError:
    print("Module not found. Exiting program...")
BloCKSIZE = 655356  # global variable that defines max block size that may be read for hashing


def sha256func(file2hash):
    """
    This function will take content that needs to be hashed and return the relevant SHA256 hash value
    """
    HashingFile = file2hash

    # try to hash the file passed to this function from the main function
    try:
        file_hash = sha256()
        with open(HashingFile, 'rb') as HF:
            FileBlock = HF.read(BloCKSIZE)
            while len(FileBlock) > 0:
                file_hash.update(FileBlock)
                FileBlock = HF.read(BloCKSIZE)

        return file_hash.hexdigest()

    # if an object is not hashable return this error
    except AttributeError:
        print("Error! Function cannot operate on this object type")


def hw64decode(workingfile):
    """
        This function will take base64 encoded content and return the string representation of the content.
        This function also finds files with appended data and computes a hash without the appended data
        Finally, the function will decode the encoded data
    """
    appendedfile = workingfile

    # With the file passed from the main function open and read as bytes via variable AF
    with open(appendedfile, 'rb') as AF:

        hexdata = binascii.hexlify(AF.read())
        hexstring = hexdata.decode()

        i = len(hexstring)  # i is defined by the length of the file assigned to AF

        while i >= 4:  # while loop to check if there is appended data after the trailer bytes

            ByteSeq2 = hexstring[(i - 4):i]

            if ByteSeq2 == "ffd9":

                aff = len(hexstring) - i
                if aff > 0:  # if there is appended data then decode it, assuming it is base64 data
                    b64string = hexstring[i:]
                    b64decoding = base64.b64decode(b64string)
                    decodedstring = binascii.hexlify(b64decoding)
                    decodedData = decodedstring.decode('utf-8')

                # calculate the hash of the file without any appended data and assign it to variable NonAppendedHash
                try:
                    sha256()
                    String4Hash = hexstring[:i]
                    digest = sha256(String4Hash.encode())

                    NonAppendedHash = digest.hexdigest()

                    return [decodedData, NonAppendedHash]  # return the decoded data and file hash without appended data

                except AttributeError:
                    print("Error! Function cannot operate on this object type")

                break

            i -= 4


if __name__ == '__main__':
    """ 
    The main function of the script. Here the program will prompt the user for a folder to traverse.
    The provided folder and subfolders are traversed for jpg files and if found computes the 
    Sha256 hash, MAC times, and stores them in the Zanzaoutput.txt file
    """

    user_prompt = input(
        "Please provide the path of the directory to investigate) #prompt user for directory path: ")  # prompt user
    # for directory
    presence_of_file = os.path.exists(user_prompt)  # navigate to the user-defined directory

    # if a directory cannot be found raise a FileNotFoundError
    if not presence_of_file:
        raise FileNotFoundError("Input directory does not exist")

    byte_dict = dict()  # create an empty dictionary for our values

    # obtain the file path of the files in the directory
    for rootdir, subdirs, files in os.walk(user_prompt):
        for file in files:
            filepath = os.path.join(rootdir, file)

            x = open(filepath, "rb")  # open a file in read bytes mode as variable x
            a = str(x.read(4))  # read the first 4 bytes of a file
            jpg_byte = 'xff\\xd8'  # byte representation of a jpg file header

            # if function that dictates what to do with a file that contains the jpg header
            if jpg_byte in a:
                hashval = sha256func(
                    filepath)  # if the header matches, then pass the file to sha256func and assign the hash to hashval
                filename = str(file)  # obtain the file's name

                Decoded64s = hw64decode(
                    filepath)  # if the header matches, then pass the file to the hw64decode function

                DecodedBase64 = Decoded64s[0]  # assign the decoded string to DecodedBase64
                StrippedFileHash = Decoded64s[1]  # assign the hash of the non-appended file to StrippedFileHash

                FileAttr = []  # create an empty list

                # obtain the access, modified, and created times of a file
                Access = int(os.path.getatime(filepath))
                Modified = int(os.path.getmtime(filepath))
                Created = int(os.path.getctime(filepath))

                # obtain the access, modified, and create times from the file in the format 'MM-DD-YYYY HH:MM:SS AM/PM'
                AccTime = dt.datetime.fromtimestamp(Access).strftime(" %m %d %Y, %I:%M:%S %p")
                modTime = dt.datetime.fromtimestamp(Modified).strftime(" %m %d %Y, %I:%M:%S %p")
                CreaTime = dt.datetime.fromtimestamp(Created).strftime(" %m %d %Y, %I:%M:%S %p")

                FileAttr.append(
                    "SHA256 Value: " + str(hashval))  # append the sha256 value with the appended string to the list
                FileAttr.append("File Accessed: " + str(AccTime))  # append the access time to FileAttr list
                FileAttr.append("File Modified: " + str(modTime))  # append the modified time to FileAttr list
                FileAttr.append("File Created: " + str(CreaTime))  # append the create time to FileAttr list
                FileAttr.append(
                    "Decoded Base64 String: " + str(DecodedBase64))  # append the decoded base64 string to the list
                FileAttr.append("Hash without appended data: " + str(
                    StrippedFileHash))  # append the file hash without appended data to the list

                byte_dict[
                    filename] = FileAttr  # write data to the dictionary using filename as the key and list as values

            x.close()  # close x

    # create an output file named fileoutput.txt that contains all the information in byte_dict()
    OutputFile = open("fileoutput.txt", "w")
    for item in byte_dict.items():
        OutputFile.writelines("%s \n" % str(item))
    OutputFile.close()  # close the output file

    TimeOfConclusion = dt.datetime.now().strftime(" %m %d %Y, %I:%M:%S %p")  # get time script completed running

    print("Operation concluded at: ", TimeOfConclusion)  # print time script concluded running
    print("Output file can be found at: ", os.path.abspath("Zanzaoutput.txt"))  # print location of output file
