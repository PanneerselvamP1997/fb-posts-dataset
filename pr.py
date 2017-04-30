import csv
import gensim
import string
from nltk.corpus import stopwords
from stemming.porter2 import stem
import fasttext 
from stop_words import get_stop_words
import re

def load_stop_words():
    # x = stopwords.words("english")
    x = get_stop_words("en")
    tmp = [s.encode('ascii') for s in x] + list(string.printable)
    return tmp + ['http','https','com']


def clean_split(s):
    return re.split('|'.join(map(re.escape, delimiters)), s.lower().strip())


def special_split(s):
    x = clean_split(s)
    return filter(lambda a: a != "", x)


def clean_words(array):
    cleaned_words = []
    for word in array:
        if (word is '') or (word in stop_words) or (word.isdigit()):
            continue
        else:
            # word = porter.stem(word, 0, len(word) - 1)
            # word=word.decode('utf-8','ignore').encode("utf-8")
            word = word.decode('utf8').encode('ascii', errors='ignore')
            cleaned_words.append(word)
    return cleaned_words


def get_label(emt):
    n=0
    lab="None"
    #print(emt)
    if int(emt[0])+int(emt[2])>n:
        lab="joy"
        n=int(emt[0])+int(emt[2])
    if int(emt[1])>n:
        lab="surprise"
        n=int(emt[1])
    if int(emt[3])>n:
        lab="sad"
        n=int(emt[3])
    if int(emt[4])>n:
        lab="angry"
        n=int(emt[4])
    #print(lab)
    return lab

dic={"joy":0,"surprise":0,"sad":0,"angry":0}
def get_text_fromcsv(filename):
    with open(filename,"r") as file:
        f=csv.reader(file)
        data=[]
        next(file)
        for r in f:
            #print(r)
            l=get_label(r[10:])
            #print(l)
            if l!="None":
                cleaned = ' '.join(clean_words(special_split(r[1])))
                dic[l]=dic[l]+1
                data.append(cleaned + " _label_"+l)
        return data

ext="./dataset/"
files=["skynews_facebook_statuses.csv","newsxonline_facebook_statuses.csv","humansofbombay_facebook_statuses.csv","berniesanders_facebook_statuses.csv","bbcnews_facebook_statuses.csv","thewire_facebook_statuses.csv","wsj_facebook_statuses.csv","humansofnewyork_facebook_statuses.csv"]

# stop_words = []
delimiters = ['\n', ' ', ',', '.', '?', '!', ':', ';', '#', '$', '[', ']',
              '(', ')', '-', '=', '@', '%', '&', '*', '_', '>', '<',
              '{', '}', '|', '/', '\\', '\'', '"', '\t', '+', '~',
              '^','\\x']
stop_words = load_stop_words()

data=[]
for f in files:
    data=data+get_text_fromcsv(ext+f)
# print(data)
# print(dic)

fi=open("traindata.txt","w")
for line in data:
    fi.write(line+"\n")
fi.close()
