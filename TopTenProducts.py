#In any e-commerce site we may need to know the top ten products sold in last one hour this code fetches the last one hour most purchased products at any given point of time

import random

dic = {}

class Product:
    def __init__(self, id, hr, name):
        self.id = id
        self.hr = hr
        self.name = name
        self.count = 1
        
def sorttopten(ls):
    for i in range(0,10):
        for j in range(i+1,len(ls)):
            if(ls[i].count < ls[j].count):
                temp = ls[i]
                ls[i] = ls[j]
                ls[j] = temp
    #remove elements after sorting to free the space required
    del ls[10:]
        

def PutProductInfo(id, hr, p):
       str1 = str(hr)+"_"+str(id)
       if(dic.get(str1) == None):
           dic[str1] = Product(id, hr, p)
       else:
           p = dic[str1]
           p.count = p.count +1

def GetTopTen(hr):
    ls = []
    for key, value in dic.items():
        if key.split('_')[0] == str(hr):
            ls.append(dic[key])
    #ls.sort(key=lambda p: p.count, reverse=True)
    sorttopten(ls)
    for i in ls:
        print(i.id, i.hr, i.count, i.name)

if __name__ == "__main__":
    lstProductName = []
    for i in range(1,100+1):
        lstProductName.append(f"Product {i}")
    for i in range(1000):
        p = random.randint(1,100)
        PutProductInfo(p, random.randint(1,24), lstProductName[p-1])
    GetTopTen(10)
