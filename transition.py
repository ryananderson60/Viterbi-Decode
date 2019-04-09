#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 12:45:24 2019

@author: ryananderson8215
"""
import nltk as nl
import emission

def calcTransition(text):
    f = open(text, "r")
    
    sentenceList = []
    
    for line in f:
        sentenceList.append(line)
    #print(sentenceList)
    
    #split into words/tags only
    sentenceListSplit = []
    for line in sentenceList:
        sentenceListSplit.append(line.split())
    #print(sentenceListSplit)
    
    #split into word/tags only for sentences
    sentenceListWordTags = []
    for sentence in sentenceListSplit:
        sentences =[]
        for word in sentence:
            sentences.append(nl.str2tuple(word))
        sentenceListWordTags.append(sentences)
        
    tagsOnly = []
    for sentence in sentenceListWordTags:
        sentenceTags = []
        for tup in sentence:
            sentenceTags.append(tup[1])
        tagsOnly.append(sentenceTags)

    
    
    #make list with start tag for rows table
    tagsWithStart = []
    for sentence in tagsOnly:
        newSentence = ["START"]
        for tag in sentence:
            newSentence.append(tag)
        tagsWithStart.append(newSentence)
    
   
    
    #get the set of all possible tags from emission class
    allWordsPos = emission.breakWordsPosTuple(text)
    allTags = []
    for word in allWordsPos:
        allTags.append(word[1])
    allTags = set(allTags)   
    allTagsStartSet = ["START"]
    for word in allTags:
        allTagsStartSet.append(word)
    
    
    #make frequencyTable. rows = allTagsStartSet, columns = allTags
    #add smooth .1
    frequencyTable = {}
    for tag in allTagsStartSet:
        frequencyTable[tag] = {}
        for t in allTags:
            frequencyTable[tag][t] = .1
    
    #fill table with frequency values.  
    for sentence in tagsWithStart:
        for i in range(len(sentence)-1):
            i = i+1
            frequencyTable[sentence[i-1]][sentence[i]] += 1
        
        
    
    r = open("README.txt", "a")
    
    #write values to readme for frequencyTable
    r.write("\n")
    r.write("FREQUENCY TABLE\n")
    r.write(" " * 10)
    for i in allTags:
        r.write("{0:<7}".format(i))
    r.write("\n")
    for i in frequencyTable:
        r.write("{0:>5}".format(i))
        for tag in frequencyTable[i]:
            r.write("{0:>7}".format(frequencyTable[i][tag]))
        r.write("\n")
    
    
    #make individual tag frequency count
    individualTagCount = {}
    for i in allTagsStartSet:
        individualTagCount[i] = 0
    
    for sentence in tagsWithStart:
        for tag in sentence:
            individualTagCount[tag] += 1
                    
            
    #make transition table
    transitionTable = {}
    for tag in allTagsStartSet:
        transitionTable[tag] = {}
        for t in allTags:
            transitionTable[tag][t] = 0
    
    #fill transition table. Probability(tagi|tagi-1) = Count(tagi-1, tagi) +.1/ 
    #Count(tagi-1) + (.1 * len(allTagsStartSet)). already added numerator
    #smooth.
    for tag in allTagsStartSet:
        for t in allTags:
            transitionTable[tag][t] = round(frequencyTable[tag][t] / ((.1 * len(allTagsStartSet)) + individualTagCount[tag]),2)
        
        
    r.write("\n")
    r.write("TRANSMISSION TABLE (with smoothing equation)\n")
    r.write(" " * 10)
    for i in allTags:
        r.write("{0:<7}".format(i))
    r.write("\n")
    for i in transitionTable:
        r.write("{0:>5}".format(i))
        for tag in transitionTable[i]:
            r.write("{0:>7}".format(transitionTable[i][tag]))
        r.write("\n")
    
    r.close()
    f.close()
    return transitionTable, allTags
    
    
    
    
    
    