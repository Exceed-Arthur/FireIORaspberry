import os


def replaceVariableInPYFileString(fileName, var=None, val=None): # variable and val to use
    fileBuffer = "" # Add everything back into this along w replaced val line
    with open(fileName, 'r') as f:
        for line in f.readlines():
            if str(var) in line: # Replace var in this line with val
                if val == None:
                    fileBuffer += f"{var} = {val}\n"
                    print(f"Line of {fileName} modified to: {fileBuffer}")
                else:
                    fileBuffer += f"{var} = '{val}'\n"
                    print(f"Line of {fileName} modified to: '{fileBuffer}'")
            else:
                fileBuffer += line  # Add back since nothing to replace
    return fileBuffer


def replaceFileFromString(filename, fileString):
    with open(filename, 'w+') as f:
        f.write(fileString)
    if filename in os.listdir(os.getcwd()):
        print(f"Wrote file string of length {len(fileString)} to {filename}")


"""
EXAMPLE SERVER FUNCTION CALL TO REPLACE WIFI CREDENTIALS

1. ACCESS POINT GETS DATA FOR BOTH VARIABLES
2. ITERATE THROUGH BOTH
3. REPLACE THE VARIABLE TO A TEMP STRING OF THE FILE TO BE RE-WRITTEN
4. REPLACE FILE FROM STRING

"""
# print(replaceVariableInPYFile('config.py', "WIFI_SSID", "lMartinez"))

