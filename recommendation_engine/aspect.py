__author__ = 'alexei'

from data_processing.mongo import MongoORM
import gensim
import nltk

from pprint import pprint as pp

def w2v_augument_seeds(model, word_list, target):

    sim_words = model.most_similar_cosmul(positive=word_list, topn=20)

    for word in sim_words:
        pos = nltk.pos_tag([word[0]])

        if word[1] < 0.75:
            break

        if pos[0][1][0].lower() == "n":
            target.add(word[0])

def aspect_seeds_restaurant(model):

    aspects = {"value": {"value", "charge", "cash"},
               "food": {"food", "taste", "flavor", "flavour", "dish", "meal", "drink"},
               "atmosphere": {"atmosphere"},
               "service": {"service"},
               "location": {"location", "neighbourhood"}}

    for aspect in aspects:

        items = aspects[aspect]
        result = set(aspects[aspect])
        for item in items:
            w2v_augument_seeds(model, [item], result)
        aspects[aspect] |= result

        for other in aspects:
            if other != aspect:
                aspects[aspect] -= aspects[other]

    return aspects

def context_seeds(model):

    context = {"time": {"sunday", "monday", "afternoon", "early", "late", "breakfast", "lunch", "dinner", "time", "day", "month", "morning", "night", "minute", "hour"},
               "companion": {"family", "friend", "colleague", "couple", "solo", "brother", "sister"}}

    for c in context:
        items = context[c]
        result = set(context[c])
        for item in items:
            w2v_augument_seeds(model, [item], result)
        context[c] |= result

    pp(context)

    return context

def aspect_segmentation_bootstrap():

    db = MongoORM()

    pass

class bcolors:
    COL2   = '\033[36m'
    COL1   = '\033[33m'
    COL0   = '\033[96m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def aspect_segmentation(review, aspects, contexts):

    result = []

    for sentence in review["sentences"]:

        res_aspects  = set()
        res_contexts = set()

        for word in sentence:

            for aspect in aspects:
                if word in aspects[aspect]:
                    res_aspects.add(aspect)

            for context in contexts:
                if word in contexts[context]:
                    res_contexts.add(context)

        result.append((tuple(res_aspects), tuple(res_contexts), sentence))

    return result

def print_segmentation(review, aspects, contexts):

    segmentation = aspect_segmentation(review, aspects, contexts)
    colours = {"value": bcolors.WARNING,
              "food": bcolors.OKGREEN,
              "atmosphere": bcolors.HEADER,
              "service": bcolors.COL0,
              "location": bcolors.COL1,
              "companion": bcolors.OKBLUE,
              "time": bcolors.COL2}

    for aspect, context, sentence in segmentation:

        # print aspect, context, sentence

        backcolour = None

        if len(aspect) == 1:
            backcolour = colours[aspect[0]]
        else:
            backcolour = bcolors.ENDC

        for word in sentence:

            printed = False

            for c in context:
                if word in contexts[c]:
                    # print "ftw", (c), word,
                    print colours[c], word, backcolour,
                    printed = True
                    break

            if printed:
                continue

            if len(aspect) == 1:
                print backcolour, word,
                printed = True
            else:
                for a in aspect:
                    if word in aspects[a]:
                        print colours[a], word, bcolors.ENDC,
                        printed = True
                        break

            if not printed:
                print backcolour, word,

        print bcolors.ENDC


def aspect_identification(category="restaurants"):

    model_name = "../data_processing/w2v_" + category + ".model"
    model = gensim.models.Word2Vec.load(model_name)

    aspects = aspect_seeds_restaurant(model)
    contexts = context_seeds(model)

    # pp(aspects)
    # pp(contexts)

    return aspects, contexts

def _test_aspect_segmentation():

    aspects, contexts = aspect_identification()
    db = MongoORM()

    for item in db.get_collection("test_optimized"):
        print_segmentation(item, aspects, contexts)
        break

    exit(0)


def main():

    # aspect_identification()
    _test_aspect_segmentation()



if __name__ == "__main__":
    main()