import random 
import glob
import math
import os
import shutil
import sys

def copy_files(path_list, scrPath, desPath, indices):

    #remove existed folder and its content
    if os.path.exists(desPath):
        shutil.rmtree(desPath)

    os.mkdir(desPath)

    for i in indices:
        shutil.copyfile(path_list[i], path_list[i].replace(scrPath + '/', desPath + '/'))

def main():
    """
    Split the dataset to training set(113 proteins) and test set(37 proteins)
    """
    if len(sys.argv) == 5:
        filepath1, filepath2, prefix1, prefix2  = sys.argv[1:]
    else:
        print("Error: missing input file or folder names.")
        return None

    # filepath1 = 'fasta'
    # filepath2 = 'rr'
    # prefix1 = 'train'
    # prefix2 = 'test'

    feature_paths = sorted(glob.glob(filepath1 + '/*.pssm')) 
    label_paths = sorted(glob.glob(filepath2 + '/*.rr'))
 

    length = len(feature_paths)
    num_test = math.ceil(length*0.25)
    test_indices = random.sample(range(length),num_test)
    train_indices = [i for i in range(length) if i not in test_indices]

    copy_files(feature_paths, filepath1, prefix1 + '_' + filepath1, train_indices)
    copy_files(label_paths, filepath2, prefix1 + '_' + filepath2, train_indices)

    copy_files(feature_paths, filepath1, prefix2 + '_' + filepath1, test_indices)
    copy_files(label_paths, filepath2, prefix2 + '_' + filepath2, test_indices)


    print('Dataset splitting completed.')

if __name__ == '__main__':
    main()

