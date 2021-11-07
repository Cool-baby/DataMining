import numpy as np
from collections import defaultdict
from operator import itemgetter


datafile = "affinity_dataset.txt"
datas = np.loadtxt(datafile)    #加载数据集

features = ["bread","milk","butter","apple","banana"]   #定义列的属性

valid_rules = defaultdict(int)      #用来保存商品A和商品B同时存在的记录
invalid_rules = defaultdict(int)    #用来保存商品A存在时，商品B不存在的记录
#此处使用defaultdict来创建字典的原因：即使这个字典没有key的时候，也会返回默认值0，而不会报错

#A和B之间的联系，返回值为购买A的数量
def connect(indexA,indexB):
    buy_A_num = 0   #记录买A的数量
    for sample in datas:    #在数据集中一行一行遍历
        if(sample[indexA] == 0):
            continue    #当没有买A时，进入下一行数据
        buy_A_num = buy_A_num+1     #买A时计数器＋1

        if(sample[indexB] == 1):    #买了A又买B
            valid_rules[(indexA,indexB)] +=1
        else:                       #买了A没买B
            invalid_rules[(indexA,indexB)] +=1
    return buy_A_num


#计算买A又买B的置信度
def get_confidence():
    confidence = defaultdict(float)     #用来保存买A同时买B的不同组合的置信度
    for premise,feature in valid_rules.keys():      #在用来保存商品A和商品B同时存在的记录中遍历
        rule = (premise, feature)
        confidence[rule] = valid_rules[rule] / (valid_rules[rule]+invalid_rules[rule])      #计算置信度，方法：同时买A和B/买A的总量
        #print("Buy {0} and {1} at the same time,confidence:{2:0.3f}".format(features[rule[0]],features[rule[1]],confidence[rule]))
    return confidence


#计算买A后最不可能买的商品
def get_AnotB_confidence():
    AnotB_confidence = defaultdict(float)
    for premise, feature in invalid_rules.keys():
        rule = (premise,feature)
        AnotB_confidence[rule] = invalid_rules[rule] / (valid_rules[rule]+invalid_rules[rule])
    return AnotB_confidence


#计算买A又买B的支持度
def get_support():
    support = defaultdict(float)
    for premise,feature in valid_rules.keys():
        rule = (premise,feature)
        support[rule] = valid_rules[rule] / len(datas)
        #print("Buy {0} and {1} at the same time,support:{2:0.3f}".format(features[rule[0]], features[rule[1]],support[rule]))
    return support


if __name__ == "__main__":
    for i in range(len(features)):
        for j in range(len(features)):      #双重循环，遍历数据集
            if(i == j):
                continue                    #跳过A和B是同一种商品的情况
            connect(i,j)
    confidence = get_confidence()
    support = get_support()
    AnotB_confidence = get_AnotB_confidence()
    #以下几行为打印置信度前五个
    print("Top five confidence")
    #对置信度排序，字典的items()返回包含字典所有元素的列表，itemgetter(1)表示以字典各元素的值作为排序依据，reverse=TRUE表示降序
    sort_dict_confidence = sorted(confidence.items(),key=itemgetter(1),reverse=True)
    sort_dict_support = sorted(support.items(),key=itemgetter(1),reverse=True)
    sort_dict_AnotB_confidence = sorted(AnotB_confidence.items(),key=itemgetter(1),reverse=False)
    for index in range(5):
        rule_confidence = sort_dict_confidence[index][0]
        print("Top {0}:Buy {1} and {2} at the same time,confidence:{3:0.3f}".format(index+1,features[rule_confidence[0]],features[rule_confidence[1]],confidence[rule_confidence]))
    print("Top five support")
    for index in range(5):
        rule_support = sort_dict_support[index][0]
        print("Top {0}:Buy {1} and {2} at the same time,confidence:{3:0.3f}".format(index+1, features[rule_support[0]],features[rule_support[1]],confidence[rule_support]))
    print("Top five A not B support")
    for index in range(5):
        rule_AnotB_confidence = sort_dict_AnotB_confidence[index][0]
        print("Top {0}:Buy {1} and {2} at the same time,A not B confidence:{3:0.3f}".format(index+1, features[rule_AnotB_confidence[0]],features[rule_AnotB_confidence[1]],confidence[rule_AnotB_confidence]))