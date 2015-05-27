from pymongo import MongoClient
from math import sqrt

client = MongoClient()
db = client.yelp

def reviewed_businesses(id):
	reviewed_businesses = {}

	for review in db['review'].find({'user_id': id}):
		user_reviewed_businesses[review['business_id']] = review

	return reviewed_businesses

def k_recommandations(user_id):
	similarity_threshold = 0

	weighted_scores = {}
	normal_scores = {}

	current_user_businesses = reviewed_businesses(user_id)

	for u in db['users'].find():
		other_user_id = u['user_id']

		# we won't run pearson_correlation against our current user
		if other_user_id is user_id:
			continue

		other_user_businesses = reviewed_businesses(other_user_id)
		similarity_score = pearson_correlation(user_businesses, other_user_businesses)
		if similarity_score > similarity_threshold:
			# find other reviews that are not common between the two users
			substract(from=other_user_businesses, user_businesses)

def substract(from, businesses_person2):
	for review in from:
		if review in businesses_person2:
			del businesses_person1[review]

def intersect(businesses_person1, businesses_person2):
	return [review for review in businesses_person1 if review in businesses_person2]

def pearson_correlation(businesses_person1, businesses_person2):
	common_businesses = intersect(businesses_person1, businesses_person2) 

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

	return nominator / float(denominator)


def pearson_correlation_old(id_person1="Xqd0DzHaiyRqVH3WRG7hzg", id_person2="H1kH6QZV7Le4zqTRNxoZow"):
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
