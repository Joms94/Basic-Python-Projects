# Remove each member with a "no" in their active column.
# Append removed members to the exMemb file.
# Preserve format of original files.

def cleanFiles(currentMem,exMem):
    '''
    currentMem: File containing list of current members
    exMem: File containing list of old members
    Removes all rows from currentMem containing 'no' and appends them to exMem
    '''
    with open(currentMem,"r+") as writeFile:
        with open(exMem,"a+") as appendFile:
            # Get the data
            writeFile.seek(0)
            members = writeFile.readlines()
            # Remove header
            header = members[0]
            inactive = [member for member in members if ('no' in member)]
            '''
           The above is the same as 

           for member in inactive:
                if 'no' in member:
                    inactive.append(member)
            '''
            # Go to the beginning of the write file
            writeFile.seek(0)
            for member in members:
                if (member in inactive):
                    appendFile.write(member)
                else:
                    writeFile.write(member)
            writeFile.truncate()




memReg = 'D:\Personal\Education\Programming\Test files\members.txt'
exReg = 'D:\Personal\Education\Programming\Test files\inactive.txt'
cleanFiles(memReg, exReg)

headers = "Membership No  Date Joined  Active  \n"


with open(memReg, 'r') as readFile:
    print("Active Members: \n\n")
    print(readFile.read())

with open(exReg, 'r') as readFile:
    print("Inactive Members: \n\n")
    print(readFile.read())