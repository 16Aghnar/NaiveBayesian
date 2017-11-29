# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:50:50 2017

@author: Sony
"""
import NBayesian_reader as nb_r


class NBayesian:
    
    def __init__(self, attributes, data, order_attribs):
        self.attributes = attributes
        self.data = data
        self.order_attribs = order_attribs
        self.class_probs = self.class_probs()
        self.cond_probs = self.conditionnal_probs()
        
    def class_probs(self):
        for key in self.attributes:
            if 'CLASS' in key :
                classe = key
        
        class_occurences = {}
        
        for i in range(len(self.data)):
            if self.data[i][0] in class_occurences:
                class_occurences[self.data[i][0]] += 1
            else :
                class_occurences[self.data[i][0]] = 1   
        for cl in self.attributes[classe] :
            if cl not in class_occurences:
                class_occurences[cl] = 0
        
        for key in class_occurences :
            class_occurences[key] = class_occurences[key]/len(self.data)
            
        return class_occurences
    
    def conditionnal_probs(self):
        cond_probs = {}
        for key in self.attributes:
            if 'CLASS' in key :
                classe = key
        
        for key in self.attributes :
            if 'CLASS' in key :
                continue
            cond_probs[key] = {}
            K = self.order_attribs.index(key) + 1
            for feature in self.attributes[key] :
                if 'CLASS' in key :
                    continue
                cond_probs[key][feature] = {}
                for cl in self.attributes[classe]:
                    cond_probs[key][feature][cl] = 0
                    for row in self.data :
                        if feature == row[K] and cl in row :
                            cond_probs[key][feature][cl] += 1/(len(self.data))
                    try :
                        cond_probs[key][feature][cl] = cond_probs[key][feature][cl]/self.class_probs[cl] 
                    except :
                        cond_probs[key][feature][cl] = 0
                        print(cl + 'doesn\'t appears in the data')
        return cond_probs
    
    def prediction(self, param_list):
        dico = {}
        params = {}
        for i in range(len(param_list)):
            params[self.order_attribs[i]] = param_list[i] 
        
        for key in self.attributes:
            if 'CLASS' in key :
                classe = key
                
        for cl in self.attributes[classe]:
            dico[cl] = self.class_probs[cl]
            for att in params :
                feat = params[att]
                dico[cl] = dico[cl]*self.cond_probs[att][feat][cl]
        
        inverse = [(value, key) for key, value in dico.items()]
        return max(inverse)[1]
        
if __name__ == '__main__' :
    data, attributes, order_attribs = nb_r.read_SoybeanData()
    nb = NBayesian(attributes, data, order_attribs)
    
    count = 0
    for row in data :
        params = row[1:]
        predict = nb.prediction(params)
        print(row[0] == predict)
        if row[0] == predict :
            count += 1
    print('taux de réussite :', count/len(data), '%')

