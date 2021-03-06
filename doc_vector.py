# import fasttext
#from gensim.models.wrappers import FastText
# import string
from collections import defaultdict
import math
# from collections import OrderedDict
from operator import add

import gensim

#from gensim.models.keyedvectors import KeyedVectors


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
# model = FastText.load_fasttext_format("wiki.en/wiki.en")
# print(model.model_name)
# print(model.words)
print("model about to be loaded!")
model = gensim.models.KeyedVectors.load_word2vec_format(
    'glove_twitter.txt', binary=False)
print("model loaded!")


f = open("preprocess_combined.txt", "r")
# f=open("training_data.txt","r")
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
    count = count + 1
for l in d:
    mean = None
    den = 0.0
    new_word_vector = []
    for w in l:
        idf_ = math.log10(glob_count / idf[w])
        # idf_=1
        f = [0] * 200
        try:
            f = model[w]
        except Exception:
            pass
#        f = [x for x in xrange(10)]
        mean = sum(f) / float(len(f))
        new_doc = []
        for x in f:
            new_score = (x - mean) * idf_
            new_doc.append(new_score)
        new_word_vector.append(new_doc)
        den += idf_
    ans = [0] * 200
    for wv in new_word_vector:
        ans = map(add, ans, wv)
    # print(ans)
    # print(den)
    if den == 0:
        den = 1
    for i in range(len(ans)):
        ans[i] = ans[i] / float(den)
    # print(ans)
    # for v in new_word_vector:
    #     new_v = map(add, )
    fin.append(ans)

f = open("vector_twitter.txt", "w")
for y in fin:
    # f.write(str(' '.join(y)) + "\n")
    f.write(str(y) + "\n")
f.close()

f = open("label_twitter.txt", "w")
for l in label:
    f.write(str(l))
f.close()
