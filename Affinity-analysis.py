import numpy as np
from collections import defaultdict
from operator import itemgetter


datafile = "DataFile/affinity_dataset.txt"
datas = np.loadtxt(datafile)

features = ["bread","milk","butter","apple","banana"]

valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)


def connect(indexA,indexB):
    buy_A_num = 0
    for sample in datas:
        if(sample[indexA] == 0):
            continue
        buy_A_num = buy_A_num+1

        if(sample[indexB] == 1):
            valid_rules[(indexA,indexB)] +=1
        else:
            invalid_rules[(indexA,indexB)] +=1
    return buy_A_num


def get_confidence():
    confidence = defaultdict(float)
    for premise,feature in valid_rules.keys():
        rule = (premise, feature)
        confidence[rule] = valid_rules[rule] / (valid_rules[rule]+invalid_rules[rule])
        print("Buy {0} and {1} at the same time,confidence:{2:0.3f}".format(features[rule[0]],features[rule[1]],confidence[rule]))
    return confidence


if __name__ == "__main__":
    for i in range(len(features)):
        for j in range(len(features)):
            if(i == j):
                continue
            connect(i,j)
    confidence = get_confidence()

    print("Top five confidence")
    sort_dict = sorted(confidence.items(),key=itemgetter(1),reverse=True)
    for index in range(5):
        rule = sort_dict[index][0]
        print("Top {0}:Buy {1} and {2} at the same time,confidence:{3:0.3f}".format(index,features[rule[0]],features[rule[1]],confidence[rule]))