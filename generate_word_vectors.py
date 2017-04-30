import fasttext

model=fasttext.skipgram("withoutlabels_combined.txt","model")


#model = fasttext.load_model("wiki.en/wiki.en.bin")
classifier = fasttext.supervised(
    "training_data.txt", "model", label_prefix="_label_")
result = classifier.test("training_data.txt")
print(classifier.labels)
print(result.precision)
