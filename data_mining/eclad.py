######################################################################################
 ###########################    Eclad algorithm     ###################################
from infastructure import *
class Eclad(Item_Sets) :
    def __init__(self, min_sup , min_conf , db_file_name):
        super().__init__(db_file_name)
        self.unique_transaction = self.initialize_unique_transaction()
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.frquent_itemsets = {}

    def initialize_unique_transaction(self) :
        transactions = defaultdict(set)
        for column,transaction in enumerate(self.transactions) :
            for char in transaction[0] :
                    transactions[char].add(column+1)
        return transactions

    def eclad_algorithm(self) :
        L = []
        for item in self.unique_transaction.keys() :
            if len(self.unique_transaction[item]) >= self.min_sup :
                self.frquent_itemsets[item]={"sup_count" : self.unique_transaction[item]}
                L.append(item)
        while L :
            length = len(L)
            length_i = len(L[0])
            if length_i == 1 :
                for i in range(length-1) :
                    for j in range(i+1,length) :
                        id = self.unique_transaction[L[i]].intersection(self.unique_transaction[L[j]])
                        if len(id) >= self.min_sup :
                            item = L[i]+L[j]
                            self.frquent_itemsets[item] = {"sup_count" : id }
                            L.append(item)
            else :
                for i in range(length-1) :
                    for j in range(i+1,length) :            
                        if L[i][:length_i-1] == L[j][:length_i-1] :
                            id = self.frquent_itemsets[L[i]]["sup_count"].intersection(self.frquent_itemsets[L[j]]["sup_count"])
                            if len(id) >= self.min_sup :
                                item =''.join(sorted(set(L[i]).union(set(L[j]))))
                                self.frquent_itemsets[item] = {"sup_count" : id}
                                L.append(item)
            L = L[length:]

    def max_close(self) :
        maxandclose(self.frquent_itemsets)

    def draw_whole_network(self) :
        draw_network(self.unique_transaction,self.frquent_itemsets,'eclad network.png')

    def draw_frequent_itemsets(self) :
        draw_frequent_itemsets(self.frquent_itemsets,'eclad frequent graph.png')       

    def display_data(self):
        super().display_data()
        print("Min_Support = {} .\n".format(self.min_sup))
        items = sorted(self.frquent_itemsets.keys(),key = len )
        for item in items:
            print("SET = {} : SUP = {} >= min_sup({}) || Maximal : {} - Closed :{}.".format(set(item),self.frquent_itemsets[item]["sup_count"],self.min_sup,self.frquent_itemsets[item]['maximal'],self.frquent_itemsets[item]["closed"]))
###############################End of The Class###########################################################
########################################################################################################
