import sqlite3
from math import factorial
import itertools
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
#################################################################################
class Item_Sets :
    def __init__(self , db_file_name   ) :
        self.transactions = self.initialize_transactions(db_file_name)
      
    def initialize_transactions(self,db_file_name) :
        conn = sqlite3.connect(db_file_name)
        cur  = conn.cursor()
        data= cur.execute("select transactions from  data_table"+input("PLEASE: Enter the data_table # from (1->4)  : ")).fetchall()
        return [list(transaction) for transaction in data]

    def display_data(self) :
        print("Data_set = {} .".format(self.transactions) )
        print("Unique_Transaction : ")
        for item,sup_count in self.unique_transaction.items() :
            print("                    item : {} , sup_count : {} ".format(item,sup_count))
        print("_________________________")
################################END Of The Class###################################
######################################################################################
def get_subsets(Set, m) :
    return itertools.combinations(Set,m)
def all_subsets(ss):
  return itertools.chain(*map(lambda x: itertools.combinations(ss, x), range(0, len(ss)+1)))
#////////////////////////////////////////////////////////////////////////////////////
def is_frequent(item_sets , canditate , min_sup ) :
    count = 0
    for transaction in item_sets :
        if set(canditate) <= set(transaction[0] ) :
            count += 1
    if count >= min_sup :
        return True,count
    return False,count

def has_infrequent_itemset(canditate , frequent_itemsets) :
    canditate_subsets = get_subsets(canditate , len(canditate)-1 )
    for subset in canditate_subsets:
        if ''.join(subset) not in frequent_itemsets :
            return True
    return False

def apriori_gen(frequent_itemsets) :
    length = len(frequent_itemsets[0])
    if length ==1 :
        for i in range(len(frequent_itemsets)-1) :
            for j in range(i+1,len(frequent_itemsets)) :
                canditate = sorted([frequent_itemsets[i],frequent_itemsets[j]])
                yield ''.join(canditate)
    else : 
        for i in range(len(frequent_itemsets)-1) :
            for j in range(i+1,len(frequent_itemsets)) :            
                if frequent_itemsets[i][:length-1] == frequent_itemsets[j][:length-1] :
                    canditate = set(frequent_itemsets[i]).union(set(frequent_itemsets[j]))
                    canditate = sorted(canditate)
                    if not has_infrequent_itemset(''.join(canditate) , frequent_itemsets) :
                        yield ''.join(canditate)                   
#////////////////////////////////////////////////////////////////////////////////////
def maxandclose(frquent_itemsets) :
    list1 = []
    list2 = []
    item_sets = sorted(frquent_itemsets.keys(),key = len ,reverse=True)
    for item in item_sets :
        if len(item) == len(item_sets[0]) :
            frquent_itemsets[item]['maximal'] = True
            frquent_itemsets[item]['closed'] = True
            list1.append(item) 
        else :
            maximal = True
            closed  = True
            if  len(list1[0]) - len(item) == 2 :
                list1 = list2
                list2 = []    
            list2.append(item)
            for super_set in list1 :               
                if set(item) <= set(super_set) :
                    maximal = False
                    if frquent_itemsets[item]['sup_count'] == frquent_itemsets[super_set]['sup_count'] :
                        closed = False
                if not maximal and not closed :
                    break
            frquent_itemsets[item]['maximal'] = maximal
            frquent_itemsets[item]['closed'] = closed   
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def node_data(frequent_itemsets ,node) :
    if node in frequent_itemsets :
        return "{}| {} {}({})".format(node
                                      ,'m' if frequent_itemsets[node]['maximal'] else ''
                                      ,'c' if frequent_itemsets[node]['closed'] and not frequent_itemsets[node]['maximal'] else ''
                                      ,frequent_itemsets[node]['sup_count']
                                      )
    else :
        return node

def node_color(node) :
    if not node['maximal'] and  node['closed'] :
        return 'orange'
    elif node['maximal'] :
        return 'green'
    else :
        return '#CCCCFF'
#///////////////////////////////////////////////////////////////////////////////////////////
def write_ass_rules(ass_rules_data,filename = 'association.txt') :
    with open(filename,'w') as file :
        for item in ass_rules_data.keys() :
            file.write('Item : {} \n'.format(set(item)))
            for rule in ass_rules_data[item] :
                file.writelines(rule)
                file.write('\n')
            file.write('______________________________________________\n')

def conf_data(item , subset ,item_sup , conf , min_conf , case ) :
    p1 = ''.join(['{} ^ '.format(char) for char in subset[:-1]])
    p1 += '{}'.format(subset[-1])
    p2_items = sorted(set(item)-set(subset))
    p2 = ''.join(['{} ^ '.format(char) for char in p2_items[:-1]])
    p2 += '{}'.format(p2_items[-1])
    return '\tR: {} --> {} \t\t\n'.format(p1,p2),'\tConfidence = SC{}/SC{} = {} / {} = {}% {} min_conf({}%) \n'.format(set(item),set(subset),item_sup,item_sup/conf,conf*100,'>=' if case else '<',min_conf*100),'\tR is Selected.\n' if case else '\tR is Rejected.\n'
#////////////////////////////////////////////////////////////////////////////////////
'''  NOTE : X and index functions depends on the combinations rule 1/k!(n!/(n-k)!) 
    Target of it :
        If we the itemset is 'abc' 3-len item so we want only all 2-len items 
        We can get the num of k-len items by the above law 
        Get n-len items by adding k0,k1,...,kn items . 
 '''
def x(n,_n  ,num) :
    if n == _n-num+1 :
            return n
    else :
            return n * x(n-1,_n,num)
def index(n,num) :
    if num == 0 :
        return 1
    else :
        return index(n,num-1) + (x(n,n,num) / factorial(num))
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#'''''''''''''''''''''''''''''''''''Drawing Network'''''''''''''''''''''''''''''''''''
def draw_network(unique_transaction,frquent_itemsets,network_name) :
    network = list(all_subsets(''.join(unique_transaction.keys())) )
    g = nx.DiGraph()
    g.add_node('Start',style='filled',fillcolor= "red"  )
    for item in network[1:len(unique_transaction)+1] :
        g.add_node(node_data(frquent_itemsets , ''.join(item)),style='filled',fillcolor= node_color(frquent_itemsets[''.join(item)]) if ''.join(item) in frquent_itemsets else 'white' )
        g.add_edge('Start',node_data(frquent_itemsets , ''.join(item)))
    for item in network[len(unique_transaction)+1:] :
        item = sorted(item)
        item = ''.join(item)
        g.add_node(node_data(frquent_itemsets , item),style='filled',fillcolor= node_color(frquent_itemsets[item]) if item in frquent_itemsets else 'white'  )          
        index1 = index(len(unique_transaction),len(item)-2)
        index2 = index(len(unique_transaction),len(item)-1)
            
        for item2 in network[int(index1):int(index2)] :   
            item2 = sorted(item2)
            item2 = ''.join(item2)            
            if set(item) >= set(item2) :    
                g.add_edge(node_data(frquent_itemsets , item2),node_data(frquent_itemsets , item) )        
    A = to_agraph(g)  
    A.layout('dot')
    A.draw(network_name)

def draw_frequent_itemsets(frquent_itemsets,network_name) :
    list1 = []
    list2 = []
    g = nx.DiGraph()
    item_sets = sorted(frquent_itemsets.keys(),key = len ,reverse=True)
    for item in item_sets :
        if len(item) == len(item_sets[0]) :         
            g.add_node(node_data(frquent_itemsets,item),style='filled',fillcolor=node_color(frquent_itemsets[item]) )
            list1.append(item)
        else :
            if  len(list1[0]) - len(item) == 2 :
                list1 = list2
                list2 = []    
            list2.append(item)
            g.add_node(node_data(frquent_itemsets,item),style='filled',fillcolor=node_color(frquent_itemsets[item]))
            for super_set in list1 :               
                if set(item) <= set(super_set) :    
                    g.add_edge(node_data(frquent_itemsets,super_set),node_data(frquent_itemsets,item),color ='brown' )                                                
    A = to_agraph(g)  
    A.layout('dot')
    A.draw(network_name)  