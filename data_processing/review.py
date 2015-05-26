__author__ = 'alexei'

from mongo import *
from parser import Parser
from util.proc import *

from gensim.models import Word2Vec

def get_corpus(coll="test_corpus", keys=None, max_items=50000):

    db = MongoORM()

    if not keys:
        count = 0
        corpus = []
        for item in db.get_collection(coll):
            corpus.append((item["text"], item["stars"]))
            count += 1
            if count == max_items:
                break
        # corpus = [(item["text"], item["stars"]) for item in db.get_collection(coll)]
    else:
        corpus = []
        for review in db.get_collection(coll):
            item = {}
            for key in keys:
                item[key] = review[key]
            corpus.append(item)

    print "Num items ", len(corpus)
    return corpus


def get_sentences(corpus, max_items=40000):
    p = Parser()
    result = []

    count = 0
    for item in corpus:
        result += p.parse(item[0])

        count += 1
        if count % 5000 == 0:
            print "Sentences: ", count
        if count >= max_items:
            break

    # result = [p.parse(item[0]) for item in corpus]
    return result


def train_w2vec(sentences, path="./w2v_restaurants.model"):

    t = Timer()
    model = Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save(path)
    t.measure("W2V model trained!")


from gensim import corpora, models

def preprocess_lda(sentences):

    t = Timer()
    dictionary = corpora.Dictionary(sentences)
    dictionary.save("./dict_restaurants.dict")
    t.measure("dictionary saved!")

    t = Timer()
    corpus = [dictionary.doc2bow(sent) for sent in sentences]
    corpora.MmCorpus.serialize("./corpus_restaurants.mm", corpus)
    t.measure("corpus saved!")

def lda_train():

    t = Timer()
    id2word = corpora.Dictionary.load("./dict_restaurants.dict")
    mm = corpora.MmCorpus("./corpus_restaurants.mm")
    t.measure("lda: corpus loaded")

    t = Timer()
    lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=10, update_every=0, passes=20)
    t.measure("lda: model trained")

    print lda.print_topics(10)

    lda.save("./lda_restaurants.mm")


def main():

    reviews = get_corpus()

    # Process sentences from reviews
    t = Timer()
    sentences = get_sentences(reviews, max_items=50000)
    t.measure("Sentences extracted.")

    # Word2Vector
    train_w2vec(reviews)

    # LDA model
    preprocess_lda(reviews)
    lda_train()

if __name__ == "__main__":

    main()