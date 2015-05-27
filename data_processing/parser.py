__author__ = 'alexei'

import re
import nltk
from nltk import data, corpus
from nltk.stem import WordNetLemmatizer as wnl

class Parser():

    def __init__(self):

        self.tokenizer = data.load('tokenizers/punkt/english.pickle')
        self.wnl       = wnl()
        self.delims = {".", ',', "!", ":", ";"}
        self.stopwords = {"the"}

    def remove_delims(self, text):
        text = re.sub(r",|\(|\)", "  ", text)
        text = re.sub(r"\.|\?|!|:|;", " . ", text)
        return text

    def remove_insanity(self, text):
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub(r"\"|\\|\*|&|-|_|/|~|`|#|@", " ", text)
        text = text.lower()
        return text

    def lemmatize(self, word, pos):

        pos = pos.lower()[0]

        if pos == "j" or pos == "r":
            return self.wnl.lemmatize(word, "a")

        if pos == "n":
            return self.wnl.lemmatize(word, "n")

        if pos == "v":
            return self.wnl.lemmatize(word, "v")

        return word

    def parse(self, text):
        text = self.remove_insanity(text)
        text = self.remove_delims(text)
        sentences = text.split(".")

        result = []
        for sent in sentences:
            sent = [token for token in sent.strip().split() if token not in self.stopwords]

            if len(sent) <= 1:
                continue

            tokens = nltk.pos_tag(sent)
            result.append([self.lemmatize(word[0], word[1]) for word in tokens])

        return result

def _test():

    p = Parser()

    from mongo import MongoORM
    db = MongoORM()

    for item in db.get_collection("test_corpus"):
        print p.parse(item["text"])
        exit(0)

if __name__ == "__main__":
    _test()
