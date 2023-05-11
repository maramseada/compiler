import collections.abc
collections.Iterable = collections.abc.Iterable
from tabulate import tabulate
from ParseTable import computeAllFirsts, computeAllFollows, createParseTable
from grammar import keyword_keys, comment_keys, comments, keyword, identifier
from ParseTree import buildParseTree


f = open('codefile','r')



i = f.read()

count = 0
program =  i.split('\n')
symbol_table = []
name = []
data_type = []
value = []
countt = []

class Entry:
    def __init__(self, name, data_type, value,count):
        self.name = name
        self.data_type = data_type
        self.value = value 
        self.count = count
        
def isIdentifier(tn):
    if tn in identifier:
        return True
    return False

def is_equal_separated(my_input):
    for charecter in my_input:
        if charecter == '=':
            return True
    return False

def is_match_found(name):
    index = -1
    if len(symbol_table) > 0:
        for index, element in enumerate(symbol_table):
            if element.name == name:
                return True, index
        return False, index

    return False, index

def buildSymbolTable(my_input):
    if is_equal_separated(my_input):
        # tokens
        users_input = my_input.split(' ')
        name.append(users_input[0])
        data_type.append(users_input[1])
        value.append(users_input[3])
        countt.append(count)
        new_entry = Entry(name, data_type,value, countt)
        # a int= 5 
        
        match_found, index = is_match_found(name)
        list = zip(name, data_type, value, countt)
        # value line of declartion
        
        hd = ["id","identifier","Type","Value", "line of declaration"]
        print(tabulate(list,hd,showindex  = True, tablefmt = "github"))
        if not match_found:
            symbol_table.append(new_entry)
            return 'Successfully insert'
        return "Name already exists."


for line in program:
    count = count+1
    print ("Line #",count,"\n \n",line,"\n")
    
    tokens = line.split(' ')
    
    print ("Tokens are",tokens,"\n")
    print("Symbol Table \n")
    buildSymbolTable(line)
    print("\nParse Tree \n")
    buildParseTree(line)
    print("\n")

    
    for token in tokens:
        if '\r' in token:
            position = token.find('\r')
            token=token[:position]
    
        if token in comment_keys:
            print ("(Comment Type: ", comments[token])
    
        if token in keyword_keys:
            print (keyword[token])
      
        if token == "print":
            print(tokens.index(token)+1) 
        if token == "+":
            res = int( token[-1] + token[1] )
            print("result is ",res)
        if token == "-":
            res = int(tokens.index(token)-1) - int(tokens.index(token)+1)
            print("result is ",res)
        if token == "*":
            res = int(tokens.index(token)-1) * int(tokens.index(token)+1)
            print("result is ",res)
    

    
    print ("________________________\n")


computeAllFirsts()
computeAllFollows()
createParseTable()
f.close()