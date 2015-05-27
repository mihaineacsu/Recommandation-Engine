__author__ = 'alexei'

from mongo import *



def create_corpus(name, categories={"Restaurants"}, city=None, only_stars=False):

    """
        Select a subdomain of reviews/ratings for ease of development.

        Cities:
        U.K.: Edinburgh
        Germany: Karlsruhe
        Canada: Montreal and Waterloo
        U.S.: Pittsburgh, Charlotte, Urbana-Champaign, Phoenix, Las Vegas, Madison

        :param name:
        :param categories:
        :param city:
        :return:
    """

    db = MongoORM()
    businesses = set()

    for business in db.get_collection("business"):

        if city and business["city"] != city:
            continue

        for item in business["categories"]:
            if item in categories:
                businesses.add(business["business_id"])
                break

    print "Count ", categories, " bussiness ", len(businesses), "."

    for review in db.get_collection("review"):

        if review["business_id"] in businesses:

            if only_stars:
                item = {"_id":         review["review_id"],
                        "stars":       review["stars"],
                        "user_id":     review["user_id"],
                        "business_id": review["business_id"]}
            else:
                item = review
                item["_id"] = item["review_id"]
                del item["review_id"]
                del item["type"]

            db.insert_item(name, item)

    print "Count items ", db.get_collection_count(name), "."


if __name__ == "__main__":
    create_corpus(name="review_small", city="Pittsburgh")