from math import sqrt
from operator import itemgetter
from sklearn.metrics import mean_squared_error

from pymongo import MongoClient

from sys import argv
upper_limit = 1000
if len(argv) is 2:
	upper_limit = int(argv[1])

client = MongoClient()
db = client.yelp
similarity_threshold = 0

def k_recommandations(user_id, k=10):
	recommandations = compute_recommandations(user_id)
	sorted_business_ids = [pair for pair in sorted(recommandations.items(), key=itemgetter(1))]
	sorted_business_ids.reverse()

	print "----> Mean squared err: %s\n" % compute_mean_sq_err(sorted_business_ids)

	return [] if not sorted_business_ids else sorted_business_ids[:k]

def compute_mean_sq_err(sorted_business_ids):
	initial_scores = []
	for i in sorted_business_ids:
		found = db['business'].find_one({'business_id': i[0]})
		if not found:
			raise Exception('Not found!')
		initial_scores.append(found['stars'])

	if len(initial_scores) is 0:
		print "not enough data"
		return None

	return mean_squared_error(initial_scores, [i[1] for i in sorted_business_ids])

def compute_recommandations(user_id):
	""" Returns a dictionary with a mapping of business_id : score.
	"""

	weighted_scores = {}
	normal_scores = {}

	current_user_businesses = reviewed_businesses(user_id)

	for u in db['users'].find().limit(upper_limit):
		other_user_id = u['user_id']
		# we won't run pearson_correlation against our current user
		if other_user_id == user_id:
			continue

		other_user_businesses = reviewed_businesses(other_user_id)
		
		similarity_score = pearson_correlation(current_user_businesses, other_user_businesses)
		if similarity_score <= similarity_threshold:
			continue

		recommandations = list_recommandations(current_user_businesses, other_user_businesses)
		for recommended_business in recommandations:
			weighted_scores.setdefault(recommended_business, 0)
			normal_scores.setdefault(recommended_business, 0)

			stars = other_user_businesses[recommended_business]['stars']
			weighted_scores[recommended_business] += similarity_score * stars
			normal_scores[recommended_business] += similarity_score


	return dict((business_id, float(weighted_scores[business_id] / normal_scores[business_id])) for business_id in weighted_scores)


def reviewed_businesses(id):
	""" Returns a dictionary of businesses reviewed by the user with user_id==id.
	
	The dict contains a mapping with reviewed_business_id as a key
	and the review obj as a value.
	"""

	businesses = {}

	for review in db['review'].find({'user_id': id}):
		businesses[review['business_id']] = review

	return businesses

def list_recommandations(user_reviews, other_reviews):
	""" Returns a list of recommandations for the user.
	Find other reviews that are not common between the two users.
	"""

	return substract(other_reviews, user_reviews)

def substract(a, b):
	""" Returns a list of all the items from a that are not common with b """

	return [item for item in a if item not in b]

def intersect(a, b):
	""" Returns a list of all the common items in the two parameters """

	return [item for item in a if item in b]

def pearson_correlation(businesses_person1, businesses_person2):
	common_businesses = intersect(businesses_person1, businesses_person2) 

	# if len(common_businesses) >= 1:
	# 	print 'common business:'
	# 	print common_businesses
	if not common_businesses:
		return 0

	# return cosineDistance(businesses_person1, businesses_person2, common_businesses)
	return classic(businesses_person1, businesses_person2, common_businesses)

def classic(businesses_person1, businesses_person2, common_businesses):
	sum_person1 = sum([businesses_person1[business_id]['stars'] for business_id in common_businesses])
	sum_person2 = sum([businesses_person2[business_id]['stars'] for business_id in common_businesses])

	sum_sq_person1 = sum([pow(businesses_person1[business_id]['stars'], 2) for business_id in common_businesses])
	sum_sq_person2 = sum([pow(businesses_person2[business_id]['stars'], 2) for business_id in common_businesses])

	product_sum = sum([businesses_person1[business_id]['stars'] * businesses_person2[business_id]['stars'] for business_id in common_businesses])

	nominator = product_sum*len(common_businesses) - (sum_person1 * sum_person2)
	denominator = sqrt((sum_sq_person1*len(common_businesses) - pow(sum_person1, 2)) * \
		(sum_sq_person2* len(common_businesses) - pow(sum_person2, 2)))

	if denominator == 0:
		return 0

	return float(nominator / denominator)

def cosineDistance(businesses_person1, businesses_person2, common_businesses):
	sum_sq_person1 = sum([pow(businesses_person1[business_id]['stars'], 2) for business_id in common_businesses])
	sum_sq_person2 = sum([pow(businesses_person2[business_id]['stars'], 2) for business_id in common_businesses])

	product_sum = sum([businesses_person1[business_id]['stars'] * businesses_person2[business_id]['stars'] for business_id in common_businesses])

	denominator = sum_sq_person1 * sum_sq_person2

	if denominator == 0:
		return 0

	return product_sum/float(denominator)



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


print k_recommandations("ZWOj6LmzwGvMDh-A85EOtA")