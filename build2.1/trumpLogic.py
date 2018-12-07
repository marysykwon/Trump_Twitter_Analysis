from textblob import TextBlob
from trumpData import *
import html
import re

def cleanT(text):
    nohtml=html.unescape(text)
    noSymbol=re.sub("(.@)|(@)|(#)|(\w+:\/\/\S+)", "", nohtml)
    outer = re.compile(r'([^A-Z ])([A-Z])')
    inner = re.compile(r'(?<!^)([A-Z])([^A-Z])')
    return outer.sub(r'\1 \2', inner.sub(r'\1\2',noSymbol))

class tweetSent():
    
    def allSent(self, text):
        allList=[]
        blob=TextBlob(text)
        for sentence in blob.sentences:
            allPolarity=sentence.sentiment.polarity
            if allPolarity<0:
                allSent="Negative"
            if allPolarity==0:
                allSent="Neutral"
            if allPolarity>0:
                allSent="Positive"
            allList.append(allSent)
        return allList

    def statementOnly(self,text):
        allList=[]
        blob=TextBlob(text)
        for sentence in blob.sentences:
            strSentence=str(sentence)
            allList.append(strSentence)
        return allList
    
    def statementPositiveOnly(self,text):
        allList=[]
        blob=TextBlob(text)
        for sentence in blob.sentences:
            allPolarity=sentence.sentiment.polarity
            if allPolarity==1:
                strSentence=str(sentence)
                allList.append(strSentence)
        if not allList:
            return
        else:
            return allList

    def statementNegativeOnly(self,text):
        allList=[]
        blob=TextBlob(text)
        for sentence in blob.sentences:
            allPolarity=sentence.sentiment.polarity
            if allPolarity==-1:
                strSentence=str(sentence)
                allList.append(strSentence)
        if not allList:
            return
        else:
            return allList
        

    def subSent(self, text, subject):
        subList=[]
        blob=TextBlob(text)
        for sentence in blob.sentences:
            if subject.lower() in sentence.lower():
                subPolarity=sentence.sentiment.polarity
                if subPolarity<0:
                    subSent="Negative"
                if subPolarity==0:
                    subSent="Neutral"
                if subPolarity>0:
                    subSent="Positive"
                subList.append(subSent)
        return subList

class tweetCounter():

    def sentCount(self, listIn):
        posCount=0
        negCount=0
        neuCount=0
        for i in listIn:
            if i=="Positive":
                posCount=posCount+1
            if i=="Negative":
                negCount=negCount+1
            if i=="Neutral":
                neuCount=neuCount+1
        return posCount,negCount,neuCount

    def sentPercent(self, listIn):
        posPercent=round((listIn[0]/sum(listIn))*100,2)
        negPercent=round((listIn[1]/sum(listIn))*100,2)
        neuPercent=round((listIn[2]/sum(listIn))*100,2)
        return posPercent, negPercent, neuPercent
