#########################################   Apoiri Algorithm  ######################################
from infastructure import *
class Aporior (Item_Sets):
    def __init__(self  ,min_sup ,min_conf , db_file_name ):
       super().__init__(db_file_name )
       self.unique_transaction = self.initialize_unique_transaction()
       self.min_sup = min_sup
       self.min_conf = min_conf
       self.frquent_itemsets = {}
       self.canditates = []
 #////////////////////////////////////////////////////////////////////////////////////
    def initialize_unique_transaction(self) :
        transactions = defaultdict(int)
        for transaction in self.transactions :
            for char in transaction[0] :
                    transactions[char] += 1
        return transactions
 #////////////////////////////////////////////////////////////////////////////////////
    def Aporior_algorithm(self ) :
        L = []
        for char in self.unique_transaction.keys() :
                if self.unique_transaction[char] >=self.min_sup :
                    self.frquent_itemsets[char]={"sup_count" : self.unique_transaction[char]}
                    L.append(char)      
        while L != [] :
            C = apriori_gen(L)
            self.canditates.append(C)
            L = []
            for transaction in C :
                frequent,sup_count = is_frequent(self.transactions,transaction,self.min_sup) 
                if frequent :                   
                    self.frquent_itemsets[transaction] ={"sup_count" : sup_count }                  
                    L.append(transaction)
#////////////////////////////////////////////////////////////////////////////////////
    def max_close(self) :
        maxandclose(self.frquent_itemsets)
#////////////////////////////////////////////////////////////////////////////////////
    def draw_whole_network(self) :
        draw_network(self.unique_transaction,self.frquent_itemsets,'apoiri network.png')

#///////////////////////////////////////////////////////////////////////////////////
    def draw_frequent_itemsets(self) :
        draw_frequent_itemsets(self.frquent_itemsets,'aporiori frequent graph.png')       
#///////////////////////////////////////////////////////////////////////////////////
    def association_rules(self) :
        ass_rules_data = defaultdict(list)
        for item in self.frquent_itemsets.keys() :
            if len(item) > 1 :
                item_subsets = all_subsets(item)
                next(item_subsets)
                for subset in item_subsets :
                    if len(subset) == len(item) :
                        break
                    l = set(item) - set(subset)
                    conf =  self.frquent_itemsets[item]['sup_count']/self.frquent_itemsets[''.join(subset)]['sup_count']
                    ass_rules_data[item].append(conf_data(item,subset ,self.frquent_itemsets[item]['sup_count'] ,conf ,self.min_conf ,conf>=self.min_conf ))
        return ass_rules_data
#////////////////////////////////////////////////////////////////////////////////////
    def display_data(self):
        super().display_data()
        print("Min_Support = {} .\n".format(self.min_sup))
        items = sorted(self.frquent_itemsets.keys(),key = len )
        for item in items:
            print("SET = {} : SUP = {} >= min_sup({}) || Maximal : {} - Closed :{}.".format(set(item),self.frquent_itemsets[item]["sup_count"],self.min_sup,self.frquent_itemsets[item]['maximal'],self.frquent_itemsets[item]["closed"]))
        write_ass_rules(self.association_rules())
 #////////////////////////////////////////////////////////////////////////////////////      
 ############################### END OF THE CLASS ####################################