# import fasttext
from gensim.models.wrappers import FastText
# import string
from collections import defaultdict
import math
# from collections import OrderedDict


def create_index(c, l):

    for w in l:
        if w not in index[c].keys():
            index[c][w] = 1
        else:
            index[c][w] = index[c][w] + 1

    l = list(set(l))
    for w in l:
        if w not in idf.keys():
            idf[w] = 1
        else:
            idf[w] = idf[w] + 1
    return

index = defaultdict(dict)
idf = {}

# model = fasttext.load_model("wiki.en/wiki.en.bin")
# print(model.model_name)
# print(model.words)
print("model about to be loaded!")
model = FastText.load_fasttext_format("wiki.en/wiki.en")
print("model loaded!")


f = open("training_data.txt", "r")
data = []
label = []
glob_count = 0
for line in f:
    l = line.strip('\n')
    l = l.split("__label__")
    data.append(l[0])
    label.append(l[1])
    glob_count = glob_count + 1

count = 1
fin = []
d = []
for l in data:
    h = l.split()
    create_index(count, h)
    d.append(h)
for l in d:
    mean = None
    den = 0
    z = None
    for w in l:
        s = math.log10(glob_count / idf[w])
        f = model[w]
        z = z + (f - sum(f) / len(f)) * s
        den = den + s
    z = z / den
    fin.append(z)

f = open("vector.txt", "w")
for y in fin:
    f.write(y)
f.close()
f = open("label.txt", "w")
for l in label:
    f.write(l)
f.close()
