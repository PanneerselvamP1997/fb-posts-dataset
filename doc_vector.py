import fasttext
import string
from collections import defaultdict
import math
from collections import OrderedDict


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

model = fasttext.load_model("wiki.en/wiki.en.bin")
# print(model.model_name)
# print(model.words)

f = open("training_data.txt", "r")
data = []
label = []
for line in f:
    l = line.strip('\n')
    l = l.split("__label__")
    data.append(l[0])
    label.append(l[1])

count = 1

for l in data:
    h = l.split()
    create_index(count, h)
    z = None
    den = 0
    for w in h:
        c = math.log10(1 + index[count][w]) * \
            math.log10(len(index.keys()) / idf[w])
        # z=z+c*model[w]
        den = den + c
        # print(model[w])
    # z=z/den
    # print(z)
