from trumpData import *
from trumpLogic import *
from statistics import *
from trumpWrite import* 

#Define objects/classes
twitter=readExcel()
twittersent=tweetSent()
tcount=tweetCounter()

#Create new workbook
trumpBook=Workbook()
    #Three different sheets
trumpSheet=trumpBook.get_sheet_by_name('Sheet') #Store sentiment analysis and stats
positiveSheet=trumpBook.create_sheet('Positive')#Stores most positive sentences
negativeSheet=trumpBook.create_sheet('Negative')#Stores most negative sentences

#containers for sentiment values
all_statements_sent=[]
subject_sent = {"Hillary":[], "CNN":[], "NYTimes":[], "Fox News":[], "Keyword":[]}
timepolarities = {'Morning':[], 'Afternoon':[], 'Evening':[], "Night": []}
tweetpd=[]
nightSent=[]
morningSent=[]
afternoonSent=[]
eveningSent=[]

#Containers for retweet and favs
retweetList=[]
favList=[]
highRetweet=0
highFav=0

#container to get list of tweetsperday and time of day counts
datecount=0
nightCount=0
morningCount=0
afternoonCount=0
eveningCount=0

#container for storing sentences / most positive and negative sentences
posStatements=[]
negStatements=[]
sentences=[]

#Container for Wordcloud
wordC = []

#Ask for keyword
print("This program analyzes 1 year of Trump's Twitter")
print("-------------------------------------------------------------------")
keyword=input("Enter keyword to search in tweets: ")
print("-------------------------------------------------------------------")
print("Please wait 1-2 minutes for analysis")
print("Analysis will be complete when wordcloud image pops up.")

lastDate=twitter.readDate(2) #to read the first date in the file to compare to other dates

#loop to all rows except header
for i in range(2, sheet.max_row+1):
    statement=twitter.readTweet(i) #read text column and clean tweet
    tweetOnly=twitter.readTweetOnly(i)
    all_statements=twittersent.allSent(statement) #return list of sentiment for given tweet
    all_statements_sent.extend(all_statements) #add list of sent of tweets to list of all sentiment

    hillary=twittersent.subSent(statement, "hillary") #examine sentiment of statements relating to hilary
    subject_sent['Hillary'].extend(hillary) #add to list of sent of statements
    cnn=twittersent.subSent(statement, "cnn") #examine sentiment of statements relating to cnn
    subject_sent['CNN'].extend(cnn) #add to list of sent of statements
    nytimes=twittersent.subSent(statement, "nytimes") #examine sentiment of statements relating to nytimes
    subject_sent['NYTimes'].extend(nytimes) #add to list of sent of statements
    foxnews=twittersent.subSent(statement, "fox news") #examine sentiment of statements relating to fox news
    subject_sent['Fox News'].extend(foxnews) #add to list of sent of statements
    keywordSubject=twittersent.subSent(statement, keyword) #examine sentiment of statements related to keyword
    subject_sent['Keyword'].extend(keywordSubject) #add to list of sent of statements

    #Grabs values for retweet and Fav amts
    retweetVal=twitter.readRetweetAmt(i)
    retweetList.append(int(retweetVal))
    
    favVal=twitter.readFavAmt(i)
    favList.append(int(favVal))

    #checks for tweets with largest amts of fav/retweet
    if retweetVal>highRetweet:
        highRetweet_tweet=tweetOnly
        highRetweet=retweetVal
    if favVal>highFav:
        highFav_tweet=tweetOnly
        highFav=favVal
    
    
    #Defines stats for tweets per day and time of day ranges
    specDate=twitter.readDate(i)
    if specDate!=lastDate:
        tweetpd.append(datecount)
        lastDate=specDate
        datecount=1
    elif specDate==lastDate:
            datecount=datecount+1
    specTime=twitter.readTime(i)
    if specTime>=0 and specTime<=55959:
        nightCount=nightCount+1
        nightSent.extend(all_statements)
    if specTime>=60000 and specTime<=115959:
        morningCount=morningCount+1
        morningSent.extend(all_statements)
    if specTime>=120000 and specTime<=175959:
        afternoonCount=afternoonCount+1
        afternoonSent.extend(all_statements)
    if specTime>=180000 and specTime<=235959:
        eveningCount=eveningCount+1
        eveningSent.extend(all_statements)

    #Takes statement and checks if polarity is 1 or -1
        #if statement is then returns list of sentences
        #if none, then returns nothing
    posSentences=twittersent.statementPositiveOnly(statement)
    negSentences=twittersent.statementNegativeOnly(statement)
    #fills containers for most positive and negative sentences
    if posSentences != None:
        posStatements.extend(posSentences)
    if negSentences != None:
        negStatements.extend(negSentences)

    #Fills sentences container will all sentences
    sentence=twittersent.statementOnly(statement)
    sentences.extend(sentence)
    

#############################################
#Counters
#Stores sentiment grades/ratios of all sentences
allsentcount=tcount.sentCount(all_statements_sent)
allpercent=tcount.sentPercent(allsentcount)
#Stores sentiment grades/ratios of keyword:Hillary
hillarycount=tcount.sentCount(subject_sent.get("Hillary"))
hillarypercent=tcount.sentPercent(hillarycount)
#Stores sentiment grades/ratios of keyword:CNN
cnncount=tcount.sentCount(subject_sent.get("CNN"))
cnnpercent=tcount.sentPercent(cnncount)
#Stores sentiment grades/ratios of keyword:NYTimes
nytimescount=tcount.sentCount(subject_sent.get("NYTimes"))
nytimespercent=tcount.sentPercent(nytimescount)
#Stores sentiment grades/ratios of keyword:Fox News
foxnewscount=tcount.sentCount(subject_sent.get("Fox News"))
foxnewspercent=tcount.sentPercent(foxnewscount)
#Stores sentiment grades/ratios time of day variables
nightsentcount=tcount.sentCount(nightSent)
nightpercent=tcount.sentPercent(nightsentcount)
morningsentcount=tcount.sentCount(morningSent)
morningpercent=tcount.sentPercent(morningsentcount)
afternoonsentcount=tcount.sentCount(afternoonSent)
afternoonpercent=tcount.sentPercent(afternoonsentcount)
eveningsentcount=tcount.sentCount(eveningSent)
eveningpercent=tcount.sentPercent(eveningsentcount)

####################################################
#Compiles above block in easy lists for writing horizontally on xlsx
#Horizontal sentiment rows for excel write
#Sequentialy: [PositiveCount][Positive%][NegativeCount][Negative%][NeutralCount][Neutral%]
allSent=wordSent(allsentcount,allpercent)

hilSent = wordSent(hillarycount,hillarypercent)
CNNSent= wordSent(cnncount,nytimespercent)
NYSent= wordSent(nytimescount,nytimespercent)
FoxSent= wordSent(foxnewscount,foxnewspercent)

nightSent=wordSent(nightsentcount,morningpercent)
morningSent=wordSent(morningsentcount,morningpercent)
afternoonSent=wordSent(afternoonsentcount,afternoonpercent)
eveningSent=wordSent(eveningsentcount,eveningpercent)

#Check is keyword even exists in any tweets
try:
    key_count=tcount.sentCount(subject_sent.get("Keyword")) #count the polarity results
    key_percent=tcount.sentPercent(key_count) #calculate percentages
    #print(key_count) #print number of positive, negative, and neutral statements
    #print(key_percent) #print percentages of positive, negative, and neutral statements
    keywordSent=wordSent(key_count,key_percent)#Horizontal container for excel write
except ZeroDivisionError:
    print("-------------------------------------------------------------------")
    print("No results relating to",keyword,"found.") #print if no results found
    keywordSent=None

###########################################################
#Excel prints
#Write to new analysis workbook
trumpSheet.cell(column=1, row = 2).value= "All"

##########################################################
#Overall Sentiment Ratios

writeRow(trumpSheet,2,allSent)

trumpSheet.cell(column=2, row = 1).value= "Positive"
trumpSheet.cell(column=3, row = 1).value= "%"

trumpSheet.cell(column=4, row = 1).value= "Negative"
trumpSheet.cell(column=5, row = 1).value= "%"

trumpSheet.cell(column=6, row = 1).value= "Neutral"
trumpSheet.cell(column=7, row = 1).value= "%"

###############################################################
#Time of Day Analysis

trumpSheet.cell(column=1, row = 4).value= "Time of Day"
#Morning
trumpSheet.cell(column=1, row = 5).value= "Morning"
#Afternoon
trumpSheet.cell(column=1, row = 6).value= "Afternoon"
#Evening
trumpSheet.cell(column=1, row = 7).value= "Evening"
#Night
trumpSheet.cell(column=1, row = 8).value= "Night"

writeRow(trumpSheet,5,morningSent)
writeRow(trumpSheet,6,afternoonSent)
writeRow(trumpSheet,7,eveningSent)
writeRow(trumpSheet,8,nightSent)

###########################################
#Subject analysis
#Rows 10,11,12,13,
hilSent = wordSent(hillarycount,hillarypercent)
CNNSent= wordSent(cnncount,nytimespercent)
NYSent= wordSent(nytimescount,nytimespercent)
FoxSent= wordSent(foxnewscount,foxnewspercent)

#Subjects
keywordList= ['Hilary','CNN','NY Times','Fox',keyword]
row = 9
for value in keywordList:
    trumpSheet.cell(column=1, row=row+1, value=value)
    row+=1

#Hillary
writeRow(trumpSheet,10,hilSent)
#CNN
writeRow(trumpSheet,11,CNNSent)
#NY Times
writeRow(trumpSheet,12,NYSent)
#Fox News
writeRow(trumpSheet,13,FoxSent)
#Input
if keywordSent != None:
    writeRow(trumpSheet,14,keywordSent)

##########################################################
#Most Positive Sentences
#Stored in 2nd Sheet in TrumpAnalysis
column = 1
for i, value in enumerate(posStatements):
    positiveSheet.cell(column=column, row=i+1, value=value)

#Most Negative Sentences
#Stored in 3rd Sheet in TrumpAnalysis
column = 1
for i, value in enumerate(negStatements):
    negativeSheet.cell(column=column, row=i+1, value=value)

#############################################################
#Tweet Per Day Stats
#Some sweet calculations
maxtweet=max(tweetpd)
mintweet=min(tweetpd)
avgtweet=round(mean(tweetpd), 2)
stdtweet=round(stdev(tweetpd), 2)
tweetStats=[maxtweet,mintweet,avgtweet,stdtweet]
#Writes the states horizontall on xlsx
writeRow(trumpSheet,17,tweetStats)

trumpSheet.cell(column=1, row = 16).value= "Statistics"
trumpSheet.cell(column=1, row = 17).value= "Tweets Per Day"
trumpSheet.cell(column=2, row = 16).value= "Max"
trumpSheet.cell(column=3, row = 16).value= "Min"
trumpSheet.cell(column=4, row = 16).value= "Avg"
trumpSheet.cell(column=5, row = 16).value= "Std Dev"

##################################################3
#Retweet and Fav Stats

retweetAvg=round(mean(retweetList), 2)
retweetMax=max(retweetList)
retweetMin=min(retweetList)
retweetStd=round(stdev(retweetList), 2)

favAvg=round(mean(favList), 2)
favMax=max(favList)
favMin=min(favList)
favStd=round(stdev(favList),2)

retweetWrite=[retweetMax,retweetMin,retweetAvg,retweetStd]
favWrite=[favMax,favMin,favAvg,favStd]



trumpSheet.cell(column=1, row = 19).value="Fav/Retweets"
trumpSheet.cell(column=2, row = 19).value= "Max"
trumpSheet.cell(column=3, row = 19).value= "Min"
trumpSheet.cell(column=4, row = 19).value= "Avg"
trumpSheet.cell(column=5, row = 19).value= "Std Dev"

trumpSheet.cell(column=1, row = 20).value= "Retweet"
writeRow(trumpSheet,20,retweetWrite)

trumpSheet.cell(column=1, row = 21).value= "Favorite"
writeRow(trumpSheet,21,favWrite)

trumpSheet.cell(column=1, row = 23).value= "Most Retweets"
trumpSheet.cell(column=1, row = 24).value= highRetweet_tweet

trumpSheet.cell(column=1, row = 26).value= "Most Likes"
trumpSheet.cell(column=1, row = 27).value= highFav_tweet









##################################################################
#Saves new workbook to xlsx
trumpBook.save('TrumpAnalysis.xlsx')

#Wordcloud Picture
wc= word_cloud(sentences)


#─────────▄──────────────▄────
#────────▌▒█───────────▄▀▒▌───
#────────▌▒▒▀▄───────▄▀▒▒▒▐───
#───────▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐───
#─────▄▄▀▒▒▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐───
#───▄▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀██▀▒▌───
#──▐▒▒▒▄▄▄▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄▒▒▌──
#──▌▒▒▐▄█▀▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐──
#─▐▒▒▒▒▒▒▒▒▒▒▒▌██▀▒▒▒▒▒▒▒▒▀▄▌─
#─▌▒▀▄██▄▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌─
#─▌▀▐▄█▄█▌▄▒▀▒▒▒▒▒▒░░░░░░▒▒▒▐─
#▐▒▀▐▀▐▀▒▒▄▄▒▄▒▒▒▒▒░░░░░░▒▒▒▒▌
#▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒░░░░░░▒▒▒▐─
#─▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒▒▒░░░░▒▒▒▒▌─
#─▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐──
#──▀▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▌──
#────▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀───
#───▐▀▒▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀─────
#──▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▀────────

#wow such code
#many variables
#very clean
#so practical




