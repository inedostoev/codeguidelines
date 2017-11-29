#!/usr/bin/python
# codeguidelines.py - githook script
# @author Kirill Nedostoev <nedostoev.ka@phystech.edu>

import sys
import os
from os.path import isdir
import subprocess

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
    if fileName.find(".cpp") == -1 or fileName.find(".c"):
        return 0
    if fileName.find(".h") == -1 or fileName.find(".hpp"):
        return 0   

    fd = open(fileName, 'r')
    buffer = fd.read()
    fd.close()
    fd = open("4b825dc642cb6eb9a060e54bf8d69288fbee4904i.c", 'w+')
    buffer = buffer.replace("include", " ")
    fd.write(buffer)
    fd.close()
    
    buffer = runGCC("4b825dc642cb6eb9a060e54bf8d69288fbee4904i.c")
    output = subprocess.call(['rm', '4b825dc642cb6eb9a060e54bf8d69288fbee4904i.c'])
    if checkTab(buffer) != -1:
        print("Tab is prohibited")
        return 1
    buffer = deleteComments(buffer)
    blameList = [ "try", "catch", "typedef", "dynamic_cast" ]
    splitBuffer = buffer.split();
    if checkUsingNamespace(splitBuffer) == 1:
        return 1
    for word in splitBuffer:
        if word in blameList:
            print("'" + word + "' is prohibited")
            return 1
    return 0

def deleteComments(buffer):
    return buffer

def checkTrailingSpaces(fileName):
    fd = open(fileName, 'r')
    buffer = fd.read()
    fd.close()
    splitBuffer = buffer.split('\n')
    counter = 0
    exitCode = 0
    while counter < len(splitBuffer):
        line = splitBuffer[counter]
        if len(line) == 0:
            counter += 1
            continue
        if line[len(line) - 1] == ' ':
            print("Trailing space in line: %i" % (counter + 1))
            exitCode = 1
        counter += 1
    return exitCode

def checkUsingNamespace(buffer):
    counter = 0
    while counter < len(buffer):
        if buffer[counter] == "using" and buffer[counter + 1] == "namespace":
            print("'using namespace' is prohibited")
            return 1
        counter += 1
    return 0


def checkTab(buffer):
    return buffer.find('\t');

def changeExitCode(exitCode, returnCode):
    if exitCode == 1:
        return 1;
    elif exitCode == 0 and returnCode == 1:
        return 1;
    else:
        return 0;

def checkDirOrFile(item):
    exitCode = 0;
    if item == ".git":
        return 0
    if isdir(item):
        listOfDir = os.listdir(item);
        for newitem in listOfDir:
            exitCode = changeExitCode(exitCode, checkDirOrFile(item + "/" + newitem))
    else:
        print("Testing code style of file: " + item)
        result = checkTrailingSpaces(item)
        if result == 1:
            print("Test failed")
            exitCode = 1
        result = fileAnalysis(item)
        if result == 1:
            print("Test failed")
            exitCode = 1
    return exitCode;


if __name__ == "__main__":
    mode = sys.argv[1]
    exitCode = 0
    if mode == "commit":
        output = runGitDiff()
        output = output.split()
        for fileName in output:
            print("Testing code style of file: " + fileName)
            result = checkTrailingSpaces(fileName)
            if result == 1:
                print("Test failed")
                exitCode = 1
            result = fileAnalysis(fileName)
            if result == 1:
                print("Test failed")
                exitCode = 1
    elif mode == "push":
        listOfDir = os.listdir(sys.argv[2]);
        for item in listOfDir:
            exitCode = changeExitCode(exitCode, checkDirOrFile(item))
    else:
        print("Error, unknown format of comand str")
        sys.exit(1)
    sys.exit(exitCode)
