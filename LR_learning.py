import sys
import glob
import math
import random
import pickle
from helper import*

def sigma(x):

	return 1.0/(1.0 + math.exp(-x))

def dot(w, x):

	w = w[:]
	product = 0.0
	for i in range(len(w)):
		product += w[i] * x[i]

	return product

def prob(w, features):

	w = w[:]
	result = dot(w, features)

	return sigma(result)

def gradient_ascent(w, features, label, lr):

	w = w[:]

	diff = label - prob(w, features)

	for i in range(len(w)):
		w[i] += lr * (diff * features[i])

	return w[:]

def initialize_weights(k):
	#k is the number of features + 1
	return [random.gauss(0, 1) for x in range(k)]

def log_likelihood(label, data, w):

	'''
	Given a data points, caculate the log likelihood of it.
			n
	LL(θ) = ∑y(i) logσ(θT x(i))+(1−y(i))log[1−σ(θT x(i))]

	'''
	w = w[:]
	product = dot(data, w)

	ll = label * product - math.log(1.0 + math.exp(product))

	return ll

def distance(v1, v2):

	return math.sqrt(sum([math.pow((a - b), 2.0) for a, b in zip(v1, v2)]))

def train_SGA(data, labels, w, learning_rate = 1e-5):

	w = w[:]
	diff = float('inf')
	ll = 0.0

	#randomly select k numbers of training points from training set with replacement
	idx = random.choices(range(len(data)), k = 20)

	for i in idx: 
		pssm = read_pssm_file(data[i])
		rr = read_rr_file(labels[i])
		contact_pairs = rr['contact_pairs']
		#balance data
		balanced_pairs = balance_data(len(pssm), contact_pairs, 200)

		for (i,j) in balanced_pairs:
			label = 1 if (i,j) in contact_pairs else 0

			feature_200 = get_fv(i, j, pssm)
	
			norm_feature = normalize_feature(feature_200)
			feature_201 = [1] + norm_feature

			w = gradient_ascent(w, feature_201, label, learning_rate)
			ll += log_likelihood(label, feature_201, w)

	return w, ll

def main():
	if len(sys.argv) == 5:
		pssm_filepath, rr_filepath, store, epochs = sys.argv[1:]
	else:
		print("Error: missing files or other required arguments")

	# pssm_filepath = 'train_pssm'
	# rr_filepath = 'train_rr'
	# store = 'learned_weight'

	pssm_files = sorted(glob.glob(pssm_filepath + '/*.pssm'))
	rr_files = sorted(glob.glob(rr_filepath + '/*.rr'))

	#Xi: 20x5x2
	w = initialize_weights(201)
	log_ll = []
	epochs = int(epochs)

	print('starting training the model...')

	for i in range(epochs): 

		learning_rate = 1e-5
		epsilon = 1e-8

		old_w = w[:]
		updated_w, ll = train_SGA(pssm_files, rr_files, w, learning_rate)
		log_ll.append(ll)
		
		print('iteration: %d, learning rate: %8.5f, log likelihood = %10.4f' %(i, learning_rate, ll))
		
		diff = distance(old_w, updated_w)
		# print(diff)
		w = updated_w[:]

		count = 0
		if diff < epsilon:
			count += 1
			if count > 5:
				break

	dump_file = open(store, 'wb')
	pickle.dump(w, dump_file)
	print("learning finished, store in " + store)
	dump_file.close()

	log_file = open('log_likelihood', 'wb')
	pickle.dump(log_ll, log_file)
	log_file.close()

if __name__ == '__main__':
	main()



