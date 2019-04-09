#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 12:41:34 2019

@author: ryananderson8215
"""

import nltk as nl

def breakWordsPosTupleHelper(text):
    f = open(text, "r")
    l = []
    for sentence in f:
        for t in sentence.split():
            l.append(t)
    f.close()
    return l
    #print(l)

def breakWordsPosTuple(text):
    l = breakWordsPosTupleHelper(text)
    listOfTuples = []
    for word in l:
        listOfTuples.append(nl.str2tuple(word))
    return listOfTuples

def createEmissionTable(text, testingText):
    listOfTuples = breakWordsPosTuple(text)
    
    f = open("Readme.txt",  "a")
    
    
    
    #make tags into set
    setOfTags = []
    for word in listOfTuples:
        setOfTags.append(word[1])
    setOfTags = set(setOfTags)
    
    #make frequency dict of tag counts
    frequencyDict = {}
    for i in setOfTags:
        frequencyDict[i] = 0
    #print(frequencyDict)
    
    #go through original list and count words
    for word in listOfTuples:
        if word[1] in frequencyDict:
            frequencyDict[word[1]] += 1
    
    #make set of words
    setOfWords = []
    for word in listOfTuples:
        setOfWords.append(word[0])
    

    #add test words too
    for i in testingText.split():
        setOfWords.append(i)

    setOfWords = set(setOfWords)    
    
    
    #now make emission dictionary to represent as table
    emissionDict = {}
    for word in setOfWords:
        emissionDict[word] = {}
        for tag in frequencyDict:
            emissionDict[word][tag] = 0
    
    #fill in values of emission table
    for word in emissionDict:
        for tag in emissionDict[word]:
            wordTagCount = 0
            for i in listOfTuples:
                if i[0] == word:
                    if i[1] == tag:                      
                        wordTagCount += 1
            #prob = count(word|tag)/count(tag)
            emissionDict[word][tag] = wordTagCount 
    #smooth
    for word in emissionDict:
        for tag in emissionDict[word]:
            emissionDict[word][tag] += .1
    

    f.write("FREQUENCY TABLE\n")
    f.write(" " * 11)
    for i in frequencyDict:
        f.write("{0:>11}".format(i))
    f.write("\n")
    for i in emissionDict:
        f.write("{0:<10}".format(i))
        for t in emissionDict[i]:
            f.write("{0:>11}".format(emissionDict[i][t]))
        f.write("\n")
            
    #get set of tags
    setOfTags = []
    for tag in listOfTuples:
        setOfTags.append(tag[1])
    setOfTags = set(setOfTags)
   
    
    
    #create emission table
    emissionTable = {}
    for i in setOfTags:
        emissionTable[i] = {}
        for word in testingText.split():
            emissionTable[i][word] = 0
    
    #fill table with probs.  Use frequencyDict of tags and emissionDict
    #for counts. Remember to smooth. Dont need smooth factor in numerator 
    #because it was already applied in frequency table
    for tag in emissionTable:
        for word in emissionTable[tag]:
            emissionTable[tag][word] = emissionDict[word][tag] / ((frequencyDict[tag] + (len(emissionDict) * .1)))

                                       
            
    
    #write values to readme
    f.write("\n")
    f.write("EMISSION TABLE (with smoothing equation)\n")
    f.write(" " * 6)
    for i in testingText:
        f.write("{0}".format(i))
    f.write("\n")
    for i in emissionTable:
        f.write("{0:<5}".format(i))
        for word in emissionTable[i]:
            f.write("{0:>7.3}".format(emissionTable[i][word]))
        f.write("\n")
    
 
    f.close()
    
    return emissionTable
            
    
    
    
    
        