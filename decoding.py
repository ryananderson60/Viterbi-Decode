#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 12:45:47 2019

@author: ryananderson8215
"""
import emission, transition

def viterbi(emissionTable, transitionTable, allTags, testingText):
    
    #make viterbi table
    viterbiTable = {}
    for i in allTags:
        viterbiTable[i] = {}
        for word in testingText.split():
            viterbiTable[i][word] = 0
    
    #make set into list
    tagList = []
    for tag in allTags:
        tagList.append(tag)
    
    testWords = []
    for i in testingText.split():
        testWords.append(i)
        
    #fill viterbi table
    for i in range(len(testWords)):
        for tag in viterbiTable:          
            if i == 0:
                viterbiTable[tag][testWords[i]] = 1.0 * transitionTable["START"][tag] * emissionTable[tag][testWords[i]]  
            else:
                a = emissionTable[tag][testWords[i]]   
                b = findMax(testWords,i,tag,viterbiTable,transitionTable)
                viterbiTable[tag][testWords[i]] = a * b  
                
                
    testFinalList = []   
    
    for i in range(len(testWords)):
        maxPos = ""
        start = True
        for t in viterbiTable:
            if start == True:
                maxPos = t
                start = False
            else:
                #print(testWords[i])
                #print("comparing {0},{1} : {2} {3}".format(t,maxPos,viterbiTable[t][testWords[i]], viterbiTable[maxPos][testWords[i]]))
                if viterbiTable[t][testWords[i]] > viterbiTable[maxPos][testWords[i]]:
                    maxPos = t

        testFinalList.append((testWords[i], maxPos))

        
                
        
    
    #write viterbi table
    r = open("README.txt", "a")
    r.write("\n")
    r.write("VITERBI TABLE\n")
    r.write(" " * 10)
    for i in testingText.split():
        r.write("{0:<14}".format(i))
    r.write("\n")
    for i in viterbiTable:
        r.write("{0:>5}".format(i))
        for word in viterbiTable[i]:
            r.write("{0:>12.4}".format(viterbiTable[i][word]))
        r.write("\n") 
    
    r.write("\n")
    r.write("TAGGED OUTPUT")
    r.write("\n")
    for i in testFinalList:
        r.write("{0}/{1}".format(i[0],i[1]))
        r.write(" ")
    r.write("\n")
    r.write("\n")
    r.write("Sentence mean probably 'humans of earth' or something like that.")
    r.write("\n")
    r.write("Human is subject. Maybe other noun could be subject too in some sentences.")
    
    r.close()

#find max number in viterbi columns
def findMax(testWords, wordIndex, tag, viterbiTable, transitionTable):
    maxNum = 0
   
    probs = {}
    for t in viterbiTable:      
        a = viterbiTable[t][testWords[wordIndex - 1]]
        b = transitionTable[t][tag]
        probs[t] = a * b
    #print("next")
    
    #print(probs)
    for s in probs:
        if probs[s] > maxNum:
            maxNum = probs[s]
    
    #print(maxNum)
    return maxNum
    
       
    
if __name__ == "__main__":
    t = "Klingon_Train.txt"
    testingText = "tera`ngan legh yaS"
    f= open("Readme.txt","w")
    emissionTable = emission.createEmissionTable(t, testingText)
    transitionTable, allTags = transition.calcTransition(t)
    viterbi(emissionTable, transitionTable, allTags, testingText)
    
    
    f.close()
    