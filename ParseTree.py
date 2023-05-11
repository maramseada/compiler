from treelib import Tree
from grammar import numerals, characters,  comment_keys, identifier, datatype, operators


def buildParseTree(line):
    
    currentTree = Tree()
    currentTree.create_node(line,"root")
    tokens = line.split(' ')
    

    for i in tokens:
       
        if i in comment_keys:
            return 
        elif i in identifier:

            currentTree.create_node("identifier","ident", parent="root")
            currentTree.create_node(i, parent='ident')

        elif i in datatype:
            currentTree.create_node("Data Type","DT", parent="root")
            currentTree.create_node(i, parent='DT')
           
        elif i in operators:
            
            currentTree.create_node("Operator","op", parent="root")
            currentTree.create_node(i, parent='op')
      
        elif i in numerals:
            currentTree.create_node("number","num", parent="root")
            currentTree.create_node(i, parent='num')
        elif i in characters:
            currentTree.create_node("character","char", parent="root")
            currentTree.create_node(i, parent='char')
       
    currentTree.show()
    