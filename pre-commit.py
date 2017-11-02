#!/usr/bin/python
# pre-commit.py - githook script
# @author Kirill Nedostoev <nedostoev.ka@phystech.edu>

import sys
import subprocess

def runGitDiff():
    output = subprocess.check_output(['git', 'diff',
                                      '--cached',
                                      '--name-only',
                                      '--diff-filter=ACM'], stderr=subprocess.STDOUT)
    return output

def runGCC(fileName):
    output = subprocess.check_output(['gcc', '-E', fileName],
                                     stderr=subprocess.STDOUT)
    return output


def fileAnalysis(fileName):
    buffer = runGCC(fileName)
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
            print(word + " is prohibited")
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
    while counter < len(splitBuffer):
        line = splitBuffer[counter]
        if len(line) == 0:
            counter += 1
            continue
        if line[len(line) - 1] == ' ':
            print("Trailing space in line: %i" % (counter + 1))
            return 1
        counter += 1
    return 0

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


if __name__ == "__main__":
    output = runGitDiff()
    output = output.split()
    exitCode = 0
    for fileName in output:
        print("Testing code style of file: " + fileName)
        result = checkTrailingSpaces(fileName)
        if result == 1:
            print("Test failed")
            sys.exit(1)
        result = fileAnalysis(fileName)
        if result == 1:
            print("Test failed")
            exitCode = 1
    sys.exit(exitCode)

