import matplotlib.pyplot as plt
import pickle

x = range(20000)
load_file = open('log_likelihood', 'rb')
y = pickle.load(load_file)

plt.figure()
plt.plot(x,y)
plt.xlabel('epochs')
plt.ylabel('log likelihood')
plt.show()