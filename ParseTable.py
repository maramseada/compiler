import collections.abc
collections.Iterable = collections.abc.Iterable
from tabulate import tabulate
def first(rule):
    global rules, nonterm_userdef, term_userdef, diction, firsts

    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':
            return '#'

    if len(rule) != 0: #  Non-Terminals
        if rule[0] in list(diction.keys()):
            # firstV first y1    x = y1y2y3
            firstV = []
            rhs_rules = diction[rule[0]]
        
            for itr in rhs_rules:
                indivRes = first(itr)
                if type(indivRes) is list:
                    for i in indivRes:
                        firstV.append(i)
                else:
                    firstV.append(indivRes)

            if '#' not in firstV:
                return firstV
            else:
                # apply epsilon
                # rule => f(ABC)=f(A)-{e} U f(BC)
                newList = []
                firstV.remove('#')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew != None:
                        if type(ansNew) is list:
                            newList = firstV + ansNew
                        else:
                            newList = firstV + [ansNew]
                    else:
                        newList = firstV
                    return newList
        
                firstV.append('#')
                return firstV

def computeAllFirsts():
    global rules, nonterm_userdef, term_userdef, diction, firsts
    for rule in rules:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')

        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split(' ')
        diction[k[0]] = multirhs

    print("\nRules: \n")
    for y in diction:
        print("{y}->{diction[y]}")
    
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)

        # save result in 'firsts' list
        firsts[y] = t

    print("\nCalculated firsts: ")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        firstslist.append(firsts.get(gg))
        print("first({key_list[index]}) \n => {firsts.get(gg)}")
        index += 1
         

def follow(nt):
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    # for start symbol return $ (recursion base case)
    solset = set()
    if nt == start_symbol:
        solset.add('$')
  
    # solset is result of computed 'follow'
    for currentNT in diction:
        rhs = diction[currentNT]
        # all productions of NT
  
        for subrule in rhs:
            if nt in subrule:
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    # empty condition call follow on LHS
     
                    if len(subrule) != 0:
                        
                        res = first(subrule)
                        # if epsilon (A->aBX) follow(B)=(first(X)-{ep}) U follow(A)
                        if '#' in res:
                            newList = []
                            res.remove('#')
                            ansNew = follow(currentNT)
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = res + ansNew
                                else:
                                    newList = res + [ansNew]
                            else:
                                newList = res
                            res = newList
                    else:
                        # when nothing in RHS take follow of LHS						
                        if nt != currentNT:
                            res = follow(currentNT)

                    if res is not None:
                        if type(res) is list:
                            for g in res:
                                solset.add(g)
                        else:
                            solset.add(res)
    return list(solset)

def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset

    print("\nCalculated follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        followlist.append(follows[gg])
        print("follow({key_list[index]}) \n => {follows[gg]}")
        index += 1
      

def createParseTable():
    import copy
    global diction, firsts, follows, term_userdef
    print("\nFirsts and Follow Result table\n")
    
   # follow first table
    ntlist = list(diction.keys())     #list of non-terminals
    llist = zip(ntlist, firstslist, followlist)
    hdd = ["non-T","First","Follow"]
    print(tabulate(llist,hdd,showindex  = True, tablefmt = "github"))
    
    
    terminals = copy.deepcopy(term_userdef)
    terminals.append('$')
    
    
    
    # create the initial empty state of ,matrix
    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        # of $ append one more col
        mat.append(row)

    # Classifying grammar as LL(1) or not LL(1)
    grammar_is_LL = True

    # rules implementation
    for lhs in diction:
        
        rhs = diction[lhs]
        for y in rhs:
            res = first(y)
            # epsilon is present,
            # - take union with follow
            if '#' in res:
                if type(res) == str:
                    firstFollow = []
                    fol_op = follows[lhs]
                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                    res = firstFollow
                else:
                    res.remove('#')
                    res = list(res) +\
                        list(follows[lhs])
            # add rules to table
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)
            for c in res:
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '': mat[xnt][yt] = mat[xnt][yt] + "{lhs}->{' '.join(y)}"
                else:
                    # if rule already present
                    if "{lhs}->{y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                        mat[xnt][yt] = mat[xnt][yt] + ",{lhs}->{' '.join(y)}"

    # final state of parse table
    print("\nGenerated parsing table:\n")
    frmt = "{:>7}" * len(terminals)
    print(frmt.format(*terminals))
    

    j = 0
    # terminals.insert(0,"non_T") 
    # for y in mat:
        
    #     ylist.append(y)
    # lllist = zip(ntlist, ylist)
    # terminals.insert(0,"") 
    # print(tabulate(lllist,terminals, tablefmt = "github"))
    
    
    for y in mat:
        
        frmt1 = "{:>7}" * len(y)
        print("{ntlist[j]} {frmt1.format(*y)}")
        j += 1

    return (mat, grammar_is_LL, terminals)

rules=["Stmt -> ident type = val",
    "ident -> A B C D E F",
    "type -> float String char int",
    "val -> a b c d e f g | 1 2 3 4"]
nonterm_userdef=['ident','type','val']
term_userdef=['A' ,'B' ,'C' ,'D' ,'E' ,'a' ,'b' ,'c' ,'d' ,'e','1' ,'2' ,'3' ,'4' ,'=' ,'float', 'String' ,'char', 'int']

diction = {}
firsts = {}
follows = {}
firstslist = []
followlist = []
termlist = []
# ylist = []
computeAllFirsts()
start_symbol = list(diction.keys())[0]
computeAllFollows()
(parsing_table, result, tabTerm) = createParseTable()