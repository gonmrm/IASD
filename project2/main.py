import csp

class Problem(csp.CSP):
    def __init__(self, fh):
    #   Place here your code to load problem from opened file object fh and
    #   set variables, domains, graph, and constraint_function accordingly

        #fd = open('input.txt','r')

        variables = []
        domains = {}
        constr= {}
        for line in fh:
            key = line[0]
            variables.append(key)
            element_list = []
            for element in line[2:].split(' '):
                if ',' in element: # means it is tuple
                    item_list = []
                    for item in element.split(','):
                        if '\n' in item:
                            item = item[:-1]
                        item_list.append(item)
                    element_list.append(tuple(item_list))
                else:
                    if '\n' in element:
                        element = element[:-1]
                    element_list.append(element)
            if key=='T':
                domains['T']=element_list
            elif key=='R':
                    domains['R']=element_list
            elif key=='W':
                variables = element_list
            else:
                constr[key]=element_list
        #print(domains)
        print(variables)
        #print(constr)
        #schedule={} # (class, type, number, day, hour, room)
        neighbors = variables
        def constraints_function(self, A, a, B, b):
            
            
           
           
            '''if A=='R':
                for block in schedule: # Não podem existir duas aulas na mesma sala
                    if block(5)==a:
                        return False
                if B=='W':
                    if b in self.domains['W']:
                        return True
            else:
                True
'''


        #if A in self.graph[B] or B in self.graph[A]:
         #   # compare the value of A and B with a and b
          #  if self.domains[A] == a and self.domains[B] == b:
           #     return True
            #else
             #   return False
      #  else:
            return False
        
        super().__init__(variables, domains, neighbors, constraints_function)
        
    def dump_solution(self, fh):
      #  Place here your code to write solution to opened file object fh
        print(1)
    
    def cost_function(self, output_file):
        print(1)  # See solution and find latest class

    def solve(self, input_file, output_file):
        values = {}
        p = Problem(input_file)
        for key in p.domains.keys():
            values[key] == []
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
