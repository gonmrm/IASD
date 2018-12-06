import csp

class Problem(csp.CSP):
    def __init__(self, fh):
    #   Place here your code to load problem from opened file object fh and
    #   set variables, domains, graph, and constraint_function accordingly

        #fd = open('input.txt','r')

        variables=[]
        temp = {}
        constr= {}
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
                temp['T']=element_list
            elif key=='S':
                S = element_list
            elif key=='R':
                    temp['R']=element_list
            elif key=='W':
                for var in element_list:
                    variables.append(','.join(var))
            else:
                temp['A']=element_list
        domain={}
        neighbors={}
        for key in variables:
            lis=[]
            for block in temp['T']:
                for room in temp['R']:
                    block.append(room)
                    copy = list(block)
                    lis.append(copy)
                    block.pop()
            domain[key] = lis
            n_list=[]
            for key2 in variables:
                if key==key2:
                    continue
                n_list.append(key2)
            neighbors[key]=n_list
        classes={}
        '''
        lis=[]
        for range(1:len(S)):
            for turnos in temp['A']:
        '''


        #print(domain)
        #print(variables)
        #a=variables[0].split(',')
        #print(constr)

        def constraints_function(self, A, a, B, b):

            A=A.split(',')
            B=B.split(',')
            
            if A[0:2]==B[0:2] and a[0]==b[0]:  # Duas aulas do mesmo tipo no mesmo dia, não pode ser
                return False
            elif a[0:2]==b[0:2]:               # Duas aulas no mesmo dia à mesma hora
                if a[2]==b[2]:                 # Caso sejam na mesma sala, não pode ser
                    return False
                turnos=[]
                for conjunto in self.constr['A']: # Verificar se há turnos em comum nas duas aulas, caso haja não pode ser, há sobreposição
                    if conjunto[1]==A[0]:
                        turnos.append(conjunto[0])         # Reunir turnos com disciplina A e verificar se existem na disciplina B
                for conjunto in self.constr['A']:
                    if conjunto[1]==B[0]

                '''Pode compensar fazer um dicionario na init na forma {IASD:['turno1','turno2']} para poder fazer o que está abaixo
                for turno in S:
                    if turno in A[0] and turno in B[0]: # A[0]='IASD' B[0]='SCDTR'
                        return False
                        '''
                        return True


            return True

        super().__init__(variables, domain, neighbors, constraints_function)
        
    def dump_solution(self, fh):
      #  Place here your code to write solution to opened file object fh
        fd = open('input.txt','w')
    
    def cost_function(self, output_file):
        print(1)#for line in fh: # See solution and find latest class percorrer linhas e procurar 

    def solve(self, input_file, output_file):
        values = {}
        p = Problem(input_file)
        
        csp.backtracking_search(self,)
        p.dump_solution(output_file)


    
    """
    A descriçao desta funçao está ali em baixo.
    Se nao me engano, as várias constraints sao as que eu meti na variavel graph (neighbors).
    Basicamente acho que têm de estar aqui definidas todas as constraints.
    
      A
     / \
    S - W
    |   |
    R - T
    """

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

