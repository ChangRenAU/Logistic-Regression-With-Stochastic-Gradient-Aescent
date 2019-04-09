import sys
import glob
import pickle
import math
from helper import*

def sigma(x):
	return 1.0/(1.0 + math.exp(-x))

def dot(w, x):

	product = 0.0
	for i in range(len(w)):
		product += w[i] * x[i]

	return product

def prob(w, features):

	#calculate the conditional probablity of being contact.
	result = dot(w, features)

	return sigma(result)

def predict(w, i, j, pssm):

	feature = get_fv(i, j, pssm)
	normalized_feature = normalize_feature(feature)
	feature_201 = [1] + normalized_feature

	probablity = prob(w, feature_201)

	return probablity

def classify(w, pssm):

	w = w[:]
	predictions = {}
	all_pairs = get_all_pairs(len(pssm))

	for val in all_pairs:
		i = val[0]
		j = val[1]
		prob = predict(w, i, j, pssm)
		predictions[val] = prob

	sorted_pred = sorted(predictions.items(), key=lambda x: x[1], reverse=True)

	return dict(sorted_pred)

def accuracy(pred, label, length):
	'''
	Given predicitons(dict) ,label(list of tuple) and lenght of a protein, calculate the accuracy
	'''
	l10 = length//10
	l5 = length//5
	l2 = length//2

	pairs = list(pred.keys())

	hit10 = len(set(pairs[:l10])&set(label))
	hit5 = len(set(pairs[:l5])&set(label))
	hit2 = len(set(pairs[:l2])&set(label))
	print('Hits(top L/10): %d' %hit10) 
	print('Hits(top L/5):  %d' %hit5) 
	print('Hits(top L/2):  %d' %hit2)	

	return hit10/l10, hit5/l5, hit2/l2

def main():
	if len(sys.argv) == 4:
	    pssm_filepath, rr_filepath, store = sys.argv[1:]
	else:
	    print("Error: missing RR or PSSM files")

	# pssm_filepath = 'test_pssm'
	# rr_filepath = 'test_rr'

	# pssm_filepath = 'test_pssm/1fqt.pssm'
	# rr_filepath = 'test_rr/1fqt.rr'

	# store = 'learned_weight'

	dump_file = open(store, 'rb')
	w = pickle.load(dump_file)
	dump_file.close()

	isfile = os.path.isfile(pssm_filepath)
	if isfile:
		pssm = read_pssm_file(pssm_filepath)
		rr = read_rr_file(rr_filepath)

	elif os.path.isdir(pssm_filepath):
		#todo: classify all test set and save to it's predicted RR file.
		pssm_files = sorted(glob.glob(pssm_filepath + '/*.pssm'))
		rr_files = sorted(glob.glob(rr_filepath + '/*.rr'))

	else:
		print("Error: the argument is neither a file nor a directory")

	print("loaded from " + store)
	print("Caculate accuracy...")

	if isfile:

		predictions = classify(w, pssm)
		filename = 'predicted_' + rr_filepath.split('/')[1]
		# print(predictions)

		write_rr_file(filename, rr['seq'], predictions)
		L10, L5, L2, = accuracy(predictions, rr['contact_pairs'], len(pssm))
		print('Accuracy of top L/10, L/5, L/2 for the protein sequence are: %7.4f%%, %7.4f%%, %7.4f%%' %(L10*100, L5*100, L2*100))

	else: 
		l = len(pssm_files)
		sum_L10 = sum_L5 = sum_L2 = 0.0   
		for i in range(l):
			pssm = read_pssm_file(pssm_files[i])
			rr = read_rr_file(rr_files[i])

			predictions = classify(w, pssm)
			filename = 'predicted_' + rr_files[i].split('/')[1]

			write_rr_file(filename, rr['seq'], predictions)
			print('Counting hits for %s:' %rr_files[i].split('/')[1])
			L10, L5, L2, = accuracy(predictions, rr['contact_pairs'], len(pssm))
	
			sum_L10 += L10
			sum_L5 += L5
			sum_L2 += L2

		aver_L10 = sum_L10/l * 100
		aver_L5 = sum_L5/l * 100
		aver_L2 = sum_L2/l * 100

		print('Average accuracy of top L/10, L/5, L/2 are: %10.8f%%, %10.8f%%, %10.8f%%' %(aver_L10, aver_L5, aver_L2))

if __name__ == '__main__':
	main()


