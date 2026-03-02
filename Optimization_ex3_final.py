# -*- coding: utf-8 -*-
"""
This is the final solution for Assignment 3 of optimization assignment for course
Algorithmic programming for operations management [1BK50]
by Muhammad Umer 1686909
and Lars Wouters 1725076
"""

#importing libraries
import pulp
import pandas as pd
import ast


class ProductionPlant:
    def __init__(self):
        self.material_types = list()
        self.product_types = list()        
        self.avail_materials = dict()
        self.recipes = dict()
        self.production_times = dict()
        self.minimum_production = dict()
        self.profit = dict()
        
        self.employee = list()
        self.employee_hours = dict()
        self.production_speed = dict()
    
    def load(self, pfile, mfile, efile):
        # mfile: file with material types and available materials
        # pfile: file with product types, production times, minimum production and profit
        
        df_materials = pd.read_csv(mfile, delimiter=';')
        df_products = pd.read_csv(pfile, delimiter=';')
        df_employees = pd.read_csv(efile, delimiter=';')
        
        
        df_employees['production_speed'] = df_employees['production_speed'].apply(ast.literal_eval)
        df_employees['production_speed'] = df_employees['production_speed'].apply(lambda x: dict(x))


        self.material_types = list(df_materials['material_type'])
        self.product_types = list(df_products['product_type'])
        self.avail_materials = dict(zip(df_materials['material_type'], df_materials['available']))
        self.recipes = dict(zip(df_products['product_type'], df_products['recipe'].apply(ast.literal_eval)))
        self.production_times = dict(zip(df_products['product_type'], df_products['required_time']))
        self.minimum_production = dict(zip(df_products['product_type'], df_products['min_production']))
        self.profit = dict(zip(df_products['product_type'], df_products['profit']))
        
        self.employee = list(df_employees['employee_type'])
        self.employee_hours = dict(zip(df_employees['employee_type'], df_employees['available_hours']))
        self.production_speed = dict(zip(df_employees['employee_type'], df_employees['production_speed']))
        
        return
    
    def solve(self):      
        self._problem = pulp.LpProblem( "MaxProf",  pulp.LpMaximize)
                
        raw_materials = {}

        #Create Lp variables for raw materials
        for key in self.material_types:
            raw_materials[key] = pulp.LpVariable(key, lowBound = 0, upBound=self.avail_materials[key], cat=pulp.LpInteger)  # Integer production quantities
        
        #Create Lp variable for X, where X[e,p] represents the number of p products made by employee e
        X = pulp.LpVariable.dicts("X", ((e, p) for e in self.employee for p in self.product_types), lowBound = 0, cat=pulp.LpInteger)

        #defining the problem / objective function
        self._problem += pulp.lpSum([X[e,p]*self.profit[p] for e in self.employee for p in self.production_speed[e]])
        
    
        #Constraints

        #minimum production
        for p in self.product_types:
            self._problem += pulp.lpSum([X[e,p] for e in self.employee]) >= self.minimum_production[p]

        
        #Production time constraint
        self._problem += pulp.lpSum([X[e, p] * (self.production_times[p]*self.production_speed[e][p]) for e in self.employee for p in self.production_speed[e]]) <= 3000

            
        #Employee availability constraint
        for e in self.employee:
            self._problem += pulp.lpSum([X[e,p]*(self.production_times[p]*self.production_speed[e][p]) for p in self.production_speed[e]]) <= self.employee_hours[e] 

        
        #Raw material per product constraint
        for key in self.avail_materials:
            self._problem += pulp.lpSum([self.recipes[key1].get(key, 0)*sum(X[e, key1] for e in self.employee) for key1 in self.recipes.keys()]) <= self.avail_materials[key]
        
        #Employees unable to produce a certain products constraint
        for e in self.employee:
            for p in list(set(self.product_types) - set(self.production_speed[e].keys())):
                self._problem += X[e, p] ==  0  

        #Solving the optimization problem
        self._problem.solve()

        #assignment and packaging of the solution
        optimal_solution = []

        for e in self.employee:
            for p in self.product_types:
                if X[e, p].varValue > 0:  # Only consider variables with positive values
                    optimal_solution.append((p, int(X[e, p].varValue), e))
        return optimal_solution
            
    

##########################
##### SOLUTION CHECK #####
##########################

print("\n\nDISCLAIMER\nNote that if you pass the solution check that does not mean that you will get full points. " +
      "We will test more and different things. Also note that you should see DONE at the end of the tests. " +
      "If you do not see DONE, this means that the program got stuck somewhere and consequently does not work properly. " +
      "Finally, note that you must use all attributes and functions that are defined in the template and give them correct values according to the assignment description. " +
      "You must not change names or signatures of predefined classes, attributes or functions. Doing so may lead to severe deduction of points. " +
      "\n\nSOLUTION CHECK\n" +
      "All of the following should be True:")

problem = ProductionPlant()
problem.load("3_1_products.txt", "3_1_materials.txt", "3_1_employees.txt")
#problem.load("3_2_products.txt", "3_2_materials.txt", "3_2_employees.txt") # You can uncomment this line to evaluate another problem instance

solution = problem.solve()
print("- An optimal solution was found:", problem._problem.status == 1)
print("- The solution contains an assignment:", len(solution) > 0)
print("- The solution is a list of 3-tuples:", type(solution) == list and all([type(sol) == tuple and len(sol) == 3 for sol in solution]) if len(solution) > 0 else False)
print("- All variables are loaded:", (len(problem.material_types) > 0 and 
                                      len(problem.product_types) > 0 and 
                                      len(problem.avail_materials) > 0 and 
                                      len(problem.recipes) > 0 and 
                                      len(problem.production_times) > 0 and 
                                      len(problem.minimum_production) > 0 and 
                                      len(problem.profit) > 0 and
                                      len(problem.employee) > 0))
print("DONE\n")  
print("Found solution:")
print(solution)