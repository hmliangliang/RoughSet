import numpy as np
class Roughset:
    def __init__(self, data):
        self.data = data.copy()
        
    def discretize(self, num):#对数据进行离散化操作
        # num为离散化的频率
        data = self.data
        for j in range(0, data.shape[1]-1):
            maxvalue = max(data[:,j])
            minvalue = min(data[:,j])
            value = (maxvalue - minvalue)/num
            for i in range(0, data.shape[0]):
                self.data[i,j] = int((data[i,j] - minvalue)/value)
        return self.data
    
    def myintersetion(self, set1, set2):#求二维集合的交集
        mylist=[]
        templist=[]
        for i in range(len(set1)):
            for j in range(len(set2)):
                templist = set(set1[i]).intersection(set(set2[j]))
                if len(templist)>0:
                   mylist.append(list(templist))
                else:
                   pass
        del templist
        return mylist
    
    def equivalence_class(self, data):#求data本身的等价类，即data所有属性参与求解
        myclass = []
        for j in range(0, data.shape[1]):
            tempclass = []
            numset = np.unique(data[:,j])#区间集
            for m in range(0, int(np.max(numset)+1)): tempclass.append([])
            for i in range(data.shape[0]):
                tempclass[int(data[i,j])].append(i)
            delete_num = []
            for ii in range(0, len(tempclass)):
                if len(tempclass[ii]) == 0:
                    delete_num.append(ii) 
                else:
                    pass
            for ii in range(0, len(delete_num)):
                del tempclass[delete_num[ii]]
            del delete_num
            if j==0:
                myclass = tempclass
                del tempclass
            else:
                myclass = self.myintersetion(myclass, tempclass)
        return myclass
    
    def POS_region(self):#求正域和下近似集
        data = self.data
        thisclass = set()
        thisclass.intersection
        attr_class = self.equivalence_class(np.transpose([data[:,data.shape[1]-1]]))
        myclass = self.equivalence_class(data[:,0:(data.shape[1]-1)])
        for i in range(0, len(myclass)):
            for j in range(0, len(attr_class)):
                if set(myclass[i]).issubset(set(attr_class[j])):
                    thisclass = thisclass.union(set(myclass[i]))
                    break
                else:
                    pass
        return thisclass
    
    def Upper_approximate(self):#求上近似集   
        data = self.data    
        thisclass = set()
        
        attr_class = self.equivalence_class(np.transpose([data[:,data.shape[1]-1]]))  
        myclass = self.equivalence_class(data[:, 0:(data.shape[1]-2)])
        for i in range(0, len(myclass)):
            for j in range(0, len(attr_class)):
                if len(set(myclass[i]).intersection(set(attr_class[j])))>0:#交集不为空
                    thisclass = thisclass.union(set(myclass[i]))
                else:
                    pass
        return thisclass
    
    def Boundary_region(self):#求边界域
        pos_set = self.POS_region()
        upp_set = self.Upper_approximate()
        return upp_set - pos_set
    
    def Approximate_quality(self):#求解近似质量
        pos_set = self.POS_region()
        gama = len(pos_set)/self.data.shape[0]
        return gama
    
    def Reduct(self):#求解算法的约简
        attr=[]
        gama1 = self.Approximate_quality()
        for j in range(0, (self.data.shape[1]-1)):
            tempdata = self.data
            data = np.delete(tempdata, j, axis = 1)
            rough_set = Roughset(data)
            gama2 = rough_set.Approximate_quality()
            if gama2 - gama1 >= 0:#属于冗余的属性
                attr.append(j)
            else:
                pass
        return attr  