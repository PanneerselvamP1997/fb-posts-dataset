import csv
import re
import string
from stop_words import get_stop_words
from porter_stemmer import PorterStemmer


def load_stop_words():
    # x = stopwords.words("english")
    x = get_stop_words("en")
    tmp = [s.encode('ascii') for s in x] + list(string.printable)
    return tmp + ['http', 'https', 'com']


def clean_split(s):
    return re.split('|'.join(map(re.escape, delimiters)), s.strip().strip("\n").lower())


def special_split(s):
    x = clean_split(s)
    return filter(lambda a: a != "", x)


def clean_words(array):
    cleaned_words = []
    for word in array:
        if (word is '') or (word.isdigit()):
            continue
        else:
            word = word.decode('utf8').encode('ascii', errors='ignore')
            word = porter.stem(word, 0, len(word) - 1)
            cleaned_words.append(word)
    return cleaned_words


def get_label(emt):
    n = 0
    lab = "None"

    if int(emt[0]) + int(emt[2]) > n:
        lab = "joy"
        n = int(emt[0]) + int(emt[2])
    if int(emt[1]) > n:
        lab = "surprise"
        n = int(emt[1])
    if int(emt[3]) > n:
        lab = "sad"
        n = int(emt[3])
    if int(emt[4]) > n:
        lab = "angry"
        # n = int(emt[4])
    # print(lab)
    return lab

# dic = {"joy": 0, "surprise": 0, "sad": 0, "angry": 0}


def get_text_fromcsv(filename):
    with open(filename, "r") as file:
        f = csv.reader(file)
        d = []
        next(file)
        for r in f:
            l = get_label(r[10:])
            if l != "None":
                cleaned = ' '.join(clean_words(special_split(r[1])))
                # dic[l] = dic[l] + 1
                #d.append(cleaned + " __label__" + l)
                d.append(cleaned)
        return d

delimiters = ['\n', ' ', ',', '.', '?', '!', ':', ';', '#', '$', '[', ']',
              '(', ')', '-', '=', '@', '%', '&', '*', '_', '>', '<',
              '{', '}', '|', '/', '\\', '\'', '"', '\t', '+', '~',
              '^']
stop_words = load_stop_words()
porter = PorterStemmer()
data = get_text_fromcsv("combined.csv")

fi = open("withoutlabels_combined.txt", "w")
for line in data:
    fi.write(line + "\n")
fi.close()
