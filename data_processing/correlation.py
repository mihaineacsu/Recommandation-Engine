from pymongo import MongoClient
from math import sqrt

client = MongoClient()
db = client.yelp

def pearson_correlation(id_person1="Xqd0DzHaiyRqVH3WRG7hzg", id_person2="H1kH6QZV7Le4zqTRNxoZow"):
	reviews_person1 = db['review'].find({'user_id': id_person1})
	reviews_person2 = db['review'].find({'user_id': id_person2})

	businesses_person1 = {}
	for review in reviews_person1:
		businesses_person1[review['business_id']] = review

	businesses_person2 = {}
	for review in reviews_person2:
		businesses_person2[review['business_id']] = review

	common_businesses = []
	for review in businesses_person1:
		if review in businesses_person2:
			common_businesses.append(review)

	print 'common business:'
	print common_businesses

	if not common_businesses:
		return 0

	sum_person1 = sum([businesses_person1[business_id]['stars'] for business_id in common_businesses])
	sum_person2 = sum([businesses_person2[business_id]['stars'] for business_id in common_businesses])

	sum_sq_person1 = sum([pow(businesses_person1[business_id]['stars'], 2) for business_id in common_businesses])
	sum_sq_person2 = sum([pow(businesses_person2[business_id]['stars'], 2) for business_id in common_businesses])

	product_sum = sum([businesses_person1[business_id]['stars'] * businesses_person2[business_id]['stars'] for business_id in common_businesses])

	nominator = product_sum - (sum_person1 * sum_person2) / len(common_businesses)
	denominator = sqrt((sum_sq_person1 - pow(sum_person1, 2)) / len(common_businesses) * \
		(sum_sq_person2 - pow(sum_person2, 2)) / len(common_businesses))

	if denominator == 0:
		return 0

	return nominator / denominator

