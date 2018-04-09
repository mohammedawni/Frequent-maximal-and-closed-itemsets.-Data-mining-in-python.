
from aporiori import Aporior
from eclad import Eclad
if __name__ == "__main__" :
    obj = Aporior(2,0.6,"training_datatset.db")
    obj.Aporior_algorithm()
    obj.max_close()
    obj.display_data()
    obj.draw_whole_network()
    obj.draw_frequent_itemsets()
    print('\t\t------------------------------------------------\n')
    obj = Eclad(2,0.6,"training_datatset.db")
    obj.eclad_algorithm()
    obj.max_close()
    obj.display_data()
    obj.draw_whole_network()
    obj.draw_frequent_itemsets()
 