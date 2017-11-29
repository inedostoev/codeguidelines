#!/usr/bin/python
# codeguidelines.py - githook script
# @author Kirill Nedostoev <nedostoev.ka@phystech.edu>

import sys
import os
from os.path import isdir
import subprocess

tmpFileName = "4b825dc642cb6eb9a060e54bf8d69288fbee4904i.c"

class tColors:
    OKGREEN =   '\033[92m'
    FAIL =      '\033[91m'
    WARNING =   '\033[93m'
    ENDC =      '\033[0m'
    BLUE =      '\033[94m'

def runGitDiff():
    output = subprocess.check_output(['git', 'diff',
                                      '--cached',
                                      '--name-only',
                                      '--diff-filter=ACM'], stderr=subprocess.STDOUT)
    return output

def runGCC(fileName):
    output = subprocess.check_output(['g++', '-E', fileName],
                                     stderr=subprocess.STDOUT)
    return output


def fileAnalysis(fileName):
    strlen = len(fileName)
    if ((fileName.rfind('.cpp') != (strlen- 4)) and (fileName.rfind('.c') != (strlen - 2)) and ((fileName.rfind('.hpp') != (strlen - 4)) and (fileName.rfind('.h') != (strlen - 2)))):
            return 0 

    print("Testing code style of file: " + tColors.OKGREEN + fileName + tColors.ENDC)

    fd = open(fileName, 'r')
    buffer = fd.read()
    fd.close()

    exitCode = 0
    result = checkTrailingSpaces(buffer)
    if result == 1:
        exitCode = 1

    fd = open(tmpFileName, 'w+')
    buffer = buffer.replace("#include", " ")
    fd.write(buffer)
    fd.close()

    buffer = runGCC(tmpFileName)
    output = subprocess.call(['rm', tmpFileName])
    blameList = [ "try", "catch", "typedef", "dynamic_cast" ]
    splitBuffer = buffer.split();
    if checkUsingNamespace(splitBuffer) == 1:
        exitCode = 1
    for word in splitBuffer:
        if word in blameList:
            print("'" + tColors.WARNING + word + tColors.ENDC + "' is prohibited")
            exitCode = 1
    return exitCode

def checkTrailingSpaces(buffer):
    splitBuffer = buffer.split('\n')
    counter = 0
    exitCode = 0
    while counter < len(splitBuffer):
        line = splitBuffer[counter]
        if len(line) == 0:
            counter += 1
            continue
        if line[len(line) - 1] == ' ':
            print(tColors.WARNING + "Trailing space " + tColors.ENDC  + "in line: " +tColors.BLUE + ("%i" % (counter + 1)) + tColors.ENDC)
            exitCode = 1
        counter += 1
    return exitCode

def checkUsingNamespace(buffer):
    counter = 0
    while counter < len(buffer):
        if buffer[counter] == "using" and buffer[counter + 1] == "namespace":
            print("'" + tColors.WARNING + "using namespace" + tColors.ENDC + "' is prohibited")
            return 1
        counter += 1
    return 0

def checkFile(fileName):
    exitCode = 0
    result = fileAnalysis(fileName)
    if result == 1:
        print(tColors.FAIL + "Test failed" + tColors.ENDC)
        exitCode = 1
    return exitCode

def changeExitCode(exitCode, returnCode):
    if exitCode == 1:
        return 1;
    elif exitCode == 0 and returnCode == 1:
        return 1;
    else:
        return 0;

def checkDirOrFile(fileName):
    exitCode = 0;
    if fileName == ".git":
        return 0
    if isdir(fileName):
        listOfDir = os.listdir(fileName);
        for newitem in listOfDir:
            exitCode = changeExitCode(exitCode, checkDirOrFile(fileName + "/" + newitem))
    else:
        exitCode = checkFile(fileName)
    return exitCode;


if __name__ == "__main__":
    mode = sys.argv[1]
    exitCode = 0

    if mode == "commit":
        output = runGitDiff()
        output = output.split()
        for fileName in output:
            exitCode = checkFile(fileName)

    elif mode == "push":
        listOfDir = os.listdir(sys.argv[2]);
        for fileName in listOfDir:
            exitCode = changeExitCode(exitCode, checkDirOrFile(fileName))

    else:
        print(tColors.FAIL + "Error, unknown format of comand str")
        sys.exit(1)
 
    sys.exit(exitCode)
