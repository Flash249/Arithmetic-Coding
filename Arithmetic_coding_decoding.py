import numpy as np
import pprint
import decimal

def getInputString():
    print("Enter the input string: ")
    inputString = input()
    # inputString += " "
    return inputString

def getUniqueElements(inputString):
    uniqueElements = set(inputString)
    uniqueElements = sorted(uniqueElements)
    return uniqueElements

def getFrequencyOfCharacters(inputString):
    uniqueElements = getUniqueElements(inputString)
    inputString = list(inputString)
    
    frequencyCount = []
    for character in uniqueElements:
        frequencyCount.append(decimal.Decimal(inputString.count(character)))
    return frequencyCount

def getProbabilityCount(frequencyCount, lengthOfInputString):
    probabilityCount = []
    for count in frequencyCount:
        count = decimal.Decimal(((count/lengthOfInputString)))
        probabilityCount.append(count)
    return probabilityCount

def getCummulativeResult(probabilityCount):
    cummulativeSum = []
    newCummulative = [0]
    cummulative = 0 
    for probability in probabilityCount:
        cummulative += probability
        # if (cummulative>=1 or cummulative >=0.98):
        #     cummulative =1
        cummulativeSum.append(decimal.Decimal(cummulative))
        newCummulative.append(decimal.Decimal(cummulative))
    return cummulativeSum, newCummulative

def getLookupTable(cummulativeSum, newCummulative):
    lookup = {}
    for iterator in range(len(cummulativeSum)):
        lookup[iterator] = newCummulative[iterator], cummulativeSum[iterator]
    return lookup

def encodedString(inputString, uniqueCharacters, lookupTable):
    uniqueCharacters = list(uniqueCharacters)
    low = 0
    high = 1
    tagRange = 0

    for i in range(len(inputString)):
        for j in range(len(uniqueCharacters)):
            if inputString[i] == uniqueCharacters[j]:
                position = j
                j += 1

                # print(position)

                tagRange = decimal.Decimal(high - low) 
                high = decimal.Decimal(low + (tagRange * lookupTable[position][1]))
                low = decimal.Decimal(low + (tagRange * lookupTable[position][0]))
                # high = np.round((low + (tagRange * lookupTable[position][1])),4)
                # low = np.round((low + (tagRange * lookupTable[position][0])),4)
                # print(high,low)
                # print(tagRange, high, low,lookupTable[position][1],lookupTable[position][0])
                i += 1
                break

    tag = (low)

    return tag

def getDecodedString(inputString, uniqueCharacters, probabilityCount, lookupTable, tagValue):
    decoded = ''
    uniqueCharacters = list(uniqueCharacters)

    for i in range(len(inputString)):
        for j in range(len(uniqueCharacters)):
            # tagValue = decimal.Decimal(tagValue)
            if (tagValue >= lookupTable[j][0] and tagValue <= lookupTable[j][1]):
                position = j
                tagValue = decimal.Decimal(((tagValue - lookupTable[position][0]) / probabilityCount[j]))
                # print(tagValue)

                decodedCharacter = uniqueCharacters[position]

                decoded += decodedCharacter
                break
    return decoded

def drive_subpart(inputString):
    uniqueCharacters = getUniqueElements(inputString)
    # print(uniqueCharacters)
    # print("The length of unique characters are "+str(len(uniqueCharacters))) 
    
    frequencyOfCharacters = getFrequencyOfCharacters(inputString)
    # print(frequencyOfCharacters)
    probabilityCount = getProbabilityCount(frequencyOfCharacters, len(inputString))
    # print(probabilityCount)
    cummulativeSum, newCummulative = getCummulativeResult(probabilityCount)
    # print(cummulativeSum, newCummulative)
    
    lookupTable = getLookupTable(cummulativeSum, newCummulative)
    # pprint.pprint(lookupTable)
    # print(lookupTable[1][0])
    tagValue = encodedString(inputString, uniqueCharacters, lookupTable)
    print("Tagvalue is : %.5f " %tagValue)
    
    decodedString = getDecodedString(inputString, uniqueCharacters, probabilityCount, lookupTable, tagValue)
    return decodedString

def assert_strings(inputString, decodedString):
    i = 1
    cnt = 0
    while(inputString!=decodedString or i >10):
        
        for i in range(i):
            inputString += " "
        i = i + 1
        decodedString = drive_subpart(inputString)
        cnt += 1
        if inputString==decodedString:
            break
            # return decodedString[:-i]
        elif cnt > 10:
            print("Program unable to encode and decode")
            exit()
        decodedString=decodedString[:-cnt]
    return decodedString

if __name__ == "__main__":

    inputString = getInputString()
    print("\nThe length of input string is "+str(len(inputString)))
    # print(inputString)

    decodedString = drive_subpart(inputString)
    decodedString = assert_strings(inputString, decodedString)
    print("\nDecoded string is: "+decodedString)