import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud, STOPWORDS
#libraries needed: numpy, pillow, wordcloud

def writeRow(sheet,row,sentList):
    column=2
    row=row
    for value in sentList:   
        sheet.cell(column=column, row=row, value=value)
        column+=1

def writeRowNumber(sheet,row,sentList):
    column=2
    row=row
    for value in sentList:
        value=int(round(value))
        sheet.cell(column=column, row=row, value=value)
        column+=1


def word_cloud(tweets):    
    pic= path.dirname(__file__) #script required to find the folder location where the picture for the word cloud is

    #function to change the default color font
    def white_color(word, font_size, position, orientation, random_state=None,
                        **kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(100, 100) #from 0 to 100, the bigger the whiter


    trump_mask= np.array(Image.open(path.join(pic, "trump_image.png"))) #getting the image for the wordcloud design
    stopwords = set(STOPWORDS) #removing stopwords from the word cloud

    #creating the word cloud, assigning number of words it will had, removing stopwords from it, margins between words in it, random number of new words that could appear everytime you run the program
    wc = WordCloud(max_words=8000, mask=trump_mask, stopwords=stopwords, margin=0,
                   random_state=10).generate(str(tweets)) #converting the cleaned tweets list to string


    plt.imshow(wc.recolor(color_func=white_color, random_state=3),
               interpolation="bilinear") #calling color function, and billinear interpolation
    wc.to_file("trump_wordcloud.png") #saving the word cloud 
    plt.axis("off")
    plt.show()
