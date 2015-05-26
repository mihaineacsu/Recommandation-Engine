__author__ = 'alexei'

from mongo import *

def create_corpus(name="test_corpus", categories={"Restaurants"}, city=None):

    db = MongoORM()
    businesses = set()

    for business in db.get_collection("business"):
        for item in business["categories"]:
            if item in categories:
                businesses.add(business["business_id"])

    print "Count ", categories, " bussiness ", len(businesses), "."

    for review in db.get_collection("review"):

        if review["business_id"] in businesses:
            review["_id"] = review["review_id"]

            del review["review_id"]
            del review["type"]

            db.insert_item(name, review)

    print "Count items ", db.get_collection_count(name), "."


if __name__ == "__main__":
    create_corpus()