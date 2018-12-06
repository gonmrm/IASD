import csp

class Problem(csp.CSP):
    upper_bound=0
    def __init__(self, fh):
    
        variables=[]
        domain=dict()
        neighbors={}
        blocks=[]
        constrA=[]
        rooms=[]
        solution=dict()
        
        for line in fh:
            key = line[0]
            element_list = []
            for element in line[2:].split(' '):
                if ',' in element: # means it is tuple
                    item_list = []
                    for item in element.split(','):
                        if '\n' in item:
                            item = item[:-1]
                        item_list.append(item)
                    element_list.append(item_list)
                else:
                    if '\n' in element:
                        element = element[:-1]
                    element_list.append(element)
            if key=='T':
                for var in element_list:
                    blocks.append(','.join(var))
            elif key=='S':
                S = list(element_list)
            elif key=='R':
                rooms = list(element_list)
            elif key=='W':
                for var in element_list:
                    variables.append(','.join(var))
            else:
                constrA = list(element_list)
        
        
        for key in variables:
            lis=[]
            for block in blocks:
                for room in rooms:
                    lis.append(block+','+room)
            domain[key] = lis
            n_list=[]
            for key2 in variables:
                if key==key2:
                    continue
                n_list.append(key2)
            neighbors[key]=n_list
        
        #classes={}
        '''
        lis=[]
        for range(1:len(S)):
            for turnos in temp['A']:
        '''

        def constraints_function(A, a, B, b):

            A=A.split(',')
            B=B.split(',')
            a=a.split(',')
            b=b.split(',')

            if int(a[1])>self.upper_bound or int(b[1])>self.upper_bound:
                return False
            elif A[0:2]==B[0:2] and a[0]==b[0]:  # Duas aulas do mesmo tipo no mesmo dia, não pode ser
                return False
            elif a[0:2]==b[0:2]:               # Duas aulas no mesmo dia à mesma hora
                if a[2]==b[2]:                 # Caso sejam na mesma sala, não pode ser
                    return False
                turnos=[]
                for conjunto in constrA: # Verificar se há turnos em comum nas duas aulas, caso haja não pode ser, há sobreposição
                    if conjunto[1]==A[0]:
                        turnos.append(conjunto[0])    # Reunir turnos com disciplina A e verificar se existem na disciplina B
                for conjunto in constrA:
                    if conjunto[1]==B[0]:
                        if conjunto[0] in turnos:     # Verificar se turnos com a disciplina têm também a disciplina B
                            return False
            else:
                return True
                '''Pode compensar fazer um dicionario na init na forma {IASD:['turno1','turno2']} para poder fazer o que está abaixo
                for turno in S:
                    if turno in A[0] and turno in B[0]: # A[0]='IASD' B[0]='SCDTR'
                        return False
                '''

        super().__init__(variables, domain, neighbors, constraints_function)
        
    def dump_solution(self, fh):
        #  Place here your code to write solution to opened file object fh
        for key in self.solution:
            fh.write(key+' '+','.join(self.solution[key].split(',')[0:2])+' '+self.solution[key].split(',')[2]+'\n')
        return
    def cost_function(self, output_file):
        print(1)#for line in fh: # See solution and find latest class percorrer linhas e procurar 
        cost=0
        for line in output_file:
            if line.split(' ')[1].split(',')[1]>cost:
                cost = line.split(' ')[1].split(',')[1]
        return cost

def solve(input_file, output_file):
    p=Problem(input_file)
    p.upper_bound=10
    optimal=False
    down=True
    up=False
    p.solution=csp.backtracking_search(p)
    if p.solution!=None: # Solution exists must decrease bound
        p.upper_bound-=1
        down=True
    else:               # Solution does not exist must increase bound
        p.upper_bound+=1
        up=True
    while True:
        p.solution=csp.backtracking_search(p)
        if p.solution==None:
            if down==True:
                p.upper_bound+=1
                p.solution=csp.backtracking_search(p)
                break
            elif up==True:
                p.upper_bound+=1
        elif p.solution!=None:
            if down==True:
                p.upper_bound-=1
            elif up==True:
                break
    p.dump_solution(output_file)


    
"""
This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
""" 

