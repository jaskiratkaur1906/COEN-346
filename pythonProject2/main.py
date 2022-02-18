import threading
import subprocess
import time
import os

arrowFound = False
doubleArrowFound = False
ampersandFound = False
slashFound = False

inputFile = open('input.txt', 'r')
lines = inputFile.readlines()
lines = [line.rstrip('\n') for line in lines]

userName = lines[0]
hostName = lines[1]
path = lines[2]

def main():


    os.chdir(path)

    shellThread = threading.Thread(target = commandLineInterpreter)
    shellThread.start()
    shellThread.join()


def execute_commands(command):

    words = command.split()
    arrowFound = checkArrow(words)
    doubleArrowFound = checkDoubleArrow(words)
    ampersandFound = checkAmpersand(words)


    if (words[0] == 'echo' and arrowFound == False and doubleArrowFound == False and ampersandFound == False):

        subprocess.run(command.split())

    elif(words[0] == 'echo' and arrowFound == True and doubleArrowFound == False and ampersandFound == False):

        writeToTextFile(words,command,-1)

    elif (words[0] == 'echo' and arrowFound == False and doubleArrowFound == True and ampersandFound == False):

        appendToTextFile(words,command,-1)

    elif(words[0] == 'echo' and arrowFound == True and doubleArrowFound == False and ampersandFound == True):
        print("Running command in background, Enter next command")

        T2shellThread = threading.Thread(target=commandLineInterpreter)

        print("T2 shellThread started")
        T2shellThread.start()

        print("Sleeping for 10 seconds")
        time.sleep(10)
        print("Done sleeping")

        writeToTextFile(words, command, -2)

        T2shellThread.join()
        print("T2 shellThread joined")


    elif (words[0] == 'echo' and arrowFound == False and doubleArrowFound == True and ampersandFound == True):
        print("Run write to file in background, NO WAITING")

        T2shellThread = threading.Thread(target=commandLineInterpreter)

        print("T2 shellThread started")
        T2shellThread.start()

        print("Sleeping for 10 seconds")
        time.sleep(10)
        print("Done sleeping")

        appendToTextFile(words, command, -2)

        T2shellThread.join()
        print("T2 shellThread joined")


    elif(words[0] == 'path'):

        print("Entered check slash")
        words = command.split('/')
        words.remove('path ')

        newWords = [word + '/' for word in words]
        print(newWords)

        #openExecFromPath(words,command)


    else:
        subprocess.run(command.split())


def checkArrow(words):
    for word in words:
        if (word == '->'):
            arrowFound = True
            break
        else:
            arrowFound = False

    return arrowFound

def checkDoubleArrow(words):
        for word in words:
            if (word == '->>'):
                doubleArrowFound = True
                break
            else:
                doubleArrowFound = False

        return doubleArrowFound

def checkAmpersand(words):
        for word in words:
            if(word == '&'):
                ampersandFound = True
                break
            else:
                ampersandFound = False

        return ampersandFound


def checkSlash(words):
    for word in words:
        if (word == '/'):
            slashFound = True
            break
        else:
            slashFound = False

    return slashFound



def commandLineInterpreter():

    while True:

        command = input(f"{userName}{hostName}$")

        if command == "exit":
            break

        else:

            t1 = threading.Thread(target=execute_commands, args=(command,))

            t1.start()
            print("T1 started")

            t1.join()
            print("T1 joined")

def writeToTextFile(words,command,n):
    print("Written into new text file")
    fileName = words[n]

    words.remove(fileName)
    words.remove('echo')
    words.remove('->')

    if(n == -2):
        words.remove('&')

    p1 = subprocess.run(command.split(), capture_output=True, text=True)
    with open(f'{fileName}', 'w') as f:
        f.write(' '.join(words))

def appendToTextFile(words,command,n):

    print("Append to existing text file")
    fileName = words[n]

    words.remove(fileName)
    words.remove('echo')
    words.remove('->>')

    if (n == -2):
        words.remove('&')

    p1 = subprocess.run(command.split(), capture_output=True, text=True)
    with open(f'{fileName}', 'a') as f:
        f.write(' '.join(words))

def openExecFromPath(words,command):

    print("Opened from given path")
    fileName = words[-1]
    path = command

    print(path)


if '__main__' == __name__:
    main()











