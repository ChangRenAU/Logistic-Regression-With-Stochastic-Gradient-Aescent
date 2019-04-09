import os
import glob
import itertools as it 
import random

def read_rr_file(filename):
    """
    Given file name, read rr format data return a dictionary
    """
    with open(filename) as f:

        res = {}
        rr = f.readlines()
        res['seq'] = rr[0].strip()
        line = []

        for i in range(1, len(rr)):
            pair = rr[i].split(' ')[:2]
            line.append(tuple(map(int, pair)))
        res['contact_pairs'] = sorted(line)

    f.close
    return res

def write_rr_file(filename, seq, pred):
    
    path = 'predicted_test_rr'
    if not os.path.isdir(path):
        os.mkdir(path)
    
    filepath = path +'/' + filename

    if os.path.isfile(filepath):
        os.remove(filepath)

    data = seq + '\n'
    for k, v in pred.items():
        data += str(k[0]) + ' ' + str(k[1]) + ' 0 8 ' + str(v) + '\n'

    with open(filepath,'w+') as f:
        f.write(data)
    f.close

def read_pssm_file(filename):
    res = []
    with open(filename) as f:
        start_reading = False
        for line in f:
            line = line.strip()
            # ipdb.set_trace()
            if line[:4]=='A  R':
                start_reading = True
                continue
            elif len(line)==0 or line[0] == 'K':
                start_reading = False

            if start_reading:
                res.append([int(x) for x in line.split()[2:22]])
    return res

def get_fv(i, j, matrix):
    """
    Get the feature vectors for a pair.
    """
    fv = get_window_feature(i, matrix) + get_window_feature(j, matrix)

    return fv

def get_feature(matrix, i):

    if i < 0 or i > len(matrix)-1:
        return [-1]*20
    else:
        return matrix[i]

def get_window_feature(i, matrix):
    w1 = get_feature(matrix, i-2)
    w2 = get_feature(matrix, i-1)
    w3 = get_feature(matrix, i)
    w4 = get_feature(matrix, i+1)
    w5 = get_feature(matrix, i+2)

    return w1 + w2 + w3 + w4 + w5

def get_all_pairs(k):

    com = list(it.permutations(range(1,k+1), 2))
    combinations = []

    for pair in com:
        if abs(pair[1] - pair[0]) > 5:
            combinations.append(pair)

    return combinations

def balance_data(k, contact_pairs, num):
    '''
    given length of a input data point, return balanced data
    '''
    all_pairs = get_all_pairs(k)
    noncontact_pairs = sorted(list(set(all_pairs) - set(contact_pairs)))

    l = len(contact_pairs)
    half = num//2

    if l > half:
        balanced_pairs = random.choices(contact_pairs, k = half) + random.choices(noncontact_pairs, k = half) 
    else:
        balanced_pairs = contact_pairs + random.choices(noncontact_pairs, k = num - l)

    random.shuffle(balanced_pairs)

    return balanced_pairs

def normalize_feature(vector):
    vmin, vmax = min(vector), max(vector)
    for i, val in enumerate(vector):
        vector[i] = (val-vmin) / (vmax-vmin)
    return vector


if __name__ == '__main__':
    # pssm = read_pssm_file('pssm/1a3a.pssm')
    # print(len(pssm))

    # a = get_fv(1, 5, pssm)
    # print(a)

    # a = get_all_pairs(20)
    # print(a)
    # print(len(a))

    # b = random.choices(a, k = 200)
    # print(b)

    # c = normalize_feature(a)
    # print(c)

    # seq = 'ABCDEFG'
    # data = {(24, 153): 0.31, (167, 36): 0.3, (192, 53): 0.318, (166, 177): 0.32, (190, 143): 0.5, (193, 148): 0.7, (120, 32): 0.8, (98, 7): 0.17, (176, 113): 0.568, (45, 198): 0.675, (37, 7): 0.3, (118, 3): 0.75, (88, 140): 0.01, (111, 118): 0.248, (148, 122): 0.3878, (103, 70): 0.3}
    # out = seq + '\n'

    # for k, v in data.items():
    #     out += str(k[0]) + ' ' + str(k[1]) + ' 0 8 ' + str(v) + '\n'

    # print(out)

    pass


