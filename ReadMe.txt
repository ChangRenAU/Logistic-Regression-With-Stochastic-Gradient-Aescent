Implementing Logistic Regression for Protein Contact Map prediction
Stochastic Gradient Ascent Based Optimization Algorithm applied to maximum the log likelihood. 

------------------
Usage Instructions
------------------

Operating System: Mac OS

This program runs on python 3, make sure the python version is correct:

    which python

To split the dataset:

    python train_test_split.py pssm rr train test

To run Logistic regression learning on training set（the last parameter is the number of iterations）:

    python LR_learning.py train_pssm train_rr learned_weight 100

To run Logistic regression classification on test set:

    python LR_classify.py test_pssm test_rr learned_weight

To run classification on a specific input protein sequence:

    python LR_classify.py pssm/1gzc.pssm rr/1gzc.rr learned_weight
