import fasttext

model = fasttext.load_model("wiki.en/wiki.en.bin")
classifier = fasttext.supervised(
    "traindata.txt", "model", label_prefix="_label_")
result = classifier.test("abc.txt")
print(classifier.labels)
print(result.precision)
