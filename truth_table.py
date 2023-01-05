import itertools

truth_table = {}

def implies(p,q):
    ans = []

    for i in range(len(p)):
        if p[i] == True and q[i] == False:
            ans.append( False)
        else:
            ans.append(True)   
    return ans


def negation(p):
    ans = []
    for i in range(len(p)):
            ans.append( not p[i])   
    return ans


def conjuction(p,q):
    ans = []
    for i in range(len(p)):       
        ans.append(p[i] and q[i])
    return ans


def disjuction(p,q):
    ans = []
    for i in range(len(p)):       
        ans.append (p[i] or q[i])
    return ans


def equivalance(p,q):
    ans = []
    for i in range(len(p)):       
        ans.append(p[i] ^ q[i])
    return ans


def print_table(truth_table,ans):
    print("    p   |    q   |    p->q  \n")
    for i in range(len(ans)):
        print(f"{'  True' if truth_table['p'][i] else ' False' }  |{'  True ' if truth_table['q'][i] else '  False'}  |  {ans[i]}\n")



    

def is_validiation(expression):
    if not check_characters_paranthesis(expression):
        return False
    

def check_characters_paranthesis(expression):
    st = [] #stack for paranthesis chekcing

    for i in range(len(expression)):
        char = ord(expression[i])
        
        # valid characters a-z or A-Z or ( ) or - or < > or ^  or ~ or |
        if not((char >=65 and char <=90 ) or (char >=97 and char <=122) or char == 40 or char == 41 or char ==45 or char ==60 or char ==62 or char == 94 or char == 124 or char == 126) : return False

        #valid paranthesis
        if expression[i] == '(' :
            st.append(expression[i])
        else:
            if st and expression[i] == ')' :
                if st[-1] != '(':
                    return False
                else : st.pop()

    return True if not st else False
    
def valid_expression(expression):

    if(not check_characters_paranthesis(expression)):
        return False
    
    operand = []
    operator = []
    i = 0
    size = len(expression)

    while(i < size):
        char = ord(expression[i])
        # ~
        if(char == 126):
            if operator and operand:
                operator.pop()
                operand.pop()
            
            elif operand:
                return False
            
            operator.append(expression[i])

        # a-z A-Z
        elif((char >=65 and char <=90 ) or (char >=97 and char <=122)):
            if(operand and operator):
                operator.pop() 
                operand.pop()
                operand.append(expression[i])

            elif(not operand and not operator):
                operand.append(expression[i])

            elif(operator and operator[0] == '~'):
                while(operator and operator[0] == '~'):
                    operator.pop()
                operand.append(expression[i])
            
            else : return False

        #  ^ and |
        elif(char == 94 or char == 124):
            if(operand and not operator):
                operator.append(expression[i])
            else : return False

        elif(char == 60):
            if(i +2 < size and expression[i+1] == '-' and expression [i+2] == '>'):
                if(operand and not operator):
                    operator.append("<->")
                    i+=2
                else : return False
            else : return False
        
        elif( char == 45):
            if(i +1 < size and expression [i+1] == '>'):
                if(operand and not operator):
                    operator.append("->")
                    i+=1
                else : return False
            else : return False
        
        elif(char == 41):
            if(operator) : return False
            if(i+1<size):
                char = ord(expression[i+1])
                if((char >=65 and char <=90 ) or (char >=97 and char <=122)):
                    return False
       
        i+=1    

    if operator:
        return False
    return True

# (p->q)^(q->p)   
def calculate(operand1,optr,operand2 =None):
    if(optr=="^"):
        return conjuction(truth_table[operand1],truth_table[operand2])
    if(optr=="|"):
        return disjuction(truth_table[operand1],truth_table[operand2])
    if(optr=="->"):
        return implies(truth_table[operand1],truth_table[operand2])
    if(optr=="<->"):
        return equivalance(truth_table[operand1],truth_table[operand2])
    if(optr=="~"):
        return negation(truth_table[operand1])
   


def evaluation(expression):
    if(not valid_expression(expression)):
        return 0

    operand  = []
    operator=[]

    i = 0;
    size = len(expression)
    while(i < size):
        char =ord( expression[i])
        
        if(char == 40):
            operator.append(expression[i])

        elif(char == 41):
            operator.pop()

        elif((char >=65 and char <=90 ) or (char >=97 and char <=122)):
            if(not operand and not operator ):
                operand.append(expression[i])

            elif(operator and operator[-1] == '('):
                operand.append(expression[i])

            else : 
                oprd1 = operand.pop()
                optr = operator.pop()

                truth_table[oprd1+optr+expression[i]] = calculate(operand1=oprd1,operand2=expression[i],optr= optr)
                operand.append(oprd1+optr+expression[i])

        elif(char == 94 or char == 124):
            operator.append(expression[i])
            
        elif(char == 60):
            operator.append("<->")
            i+=2
        
        elif( char == 45):
            operator.append("->")
            i+=1
       
        i+=1
    return truth_table[operand[0]]

        
def start():
    while(True):

        expression = input("Enter Propositional logic : ")
        if(not valid_expression(expression=expression)):
            print("Invalid expression")
            continue
    
        variables = list(set(map(lambda x: ord(x),filter(lambda x: x != None,map(lambda x: x if x.isalpha() else None,'_'.join(expression).split('_'))))))
        variables.sort()
        variables = list(map(lambda x: chr(x),variables ))
        table = list(itertools.product([True,False], repeat=len(variables)))

        for i in range(len(variables)):
            var = variables[i]
            truth_table[var] =[]
            for j in range(len(table)):
                truth_table[var]  += [table[j][i]]
    
        ansTT = evaluation(expression)
        print(ansTT)
        break
    


start()