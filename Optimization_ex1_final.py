# -*- coding: utf-8 -*-
"""
This is the final solution for Assignment 1 of optimization assignment for course
Algorithmic programming for operations management [1BK50]
by Muhammad Umer 1686909
and Lars Wouters 1725076
"""
import pulp

class ProductionPlant:
    def __init__(self):
        self.material_types = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']
        self.product_types = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
        
        self.avail_materials = {'M1': 300, 'M2': 400, 'M3': 300, 'M4': 200, 'M5': 700, 'M6': 400, 'M7': 300, 'M8': 500, 'M9': 200}
        self.recipes = {'P1': {'M1': 2, 'M2': 1, 'M3': 1, 'M4': 1},
                        'P2': {'M1': 2, 'M2': 3, 'M3': 1, 'M4': 1},
                        'P3': {'M1': 1, 'M3': 2, 'M5': 3, 'M7': 1},
                        'P4': {'M4': 2, 'M6': 1, 'M8': 1, 'M9': 1},
                        'P5': {'M2': 2, 'M5': 1, 'M7': 2, 'M8': 1},
                        'P6': {'M3': 2, 'M8': 3, 'M9': 1, 'M1': 1},
                        'P7': {'M1': 2, 'M6': 1, 'M9': 2, 'M2': 1},
                        'P8': {'M4': 2, 'M7': 2, 'M8': 1, 'M3': 3},
                        'P9': {'M5': 2, 'M6': 2, 'M9': 1, 'M4': 1},
                        'P10': {'M5': 2, 'M6': 2, 'M9': 3, 'M4': 1},}

        self.production_times = {'P1': 4.5, 'P2': 15, 'P3': 11, 'P4': 14, 'P5': 15, 'P6': 12, 'P7': 13, 'P8': 8, 'P9': 25, 'P10': 4}
        self.minimum_production = {'P1': 10, 'P2': 20, 'P3': 10, 'P4': 15, 'P5': 5, 'P6': 8, 'P7': 9, 'P8': 7, 'P9': 16, 'P10': 10}
        self.profit = {'P1': 10, 'P2': 5, 'P3': 12, 'P4': 14, 'P5': 12, 'P6': 13, 'P7': 11, 'P8': 14, 'P9': 20, 'P10': 3}
    
    
    def solve(self):  
        self._problem = pulp.LpProblem( "MaxProf",  pulp.LpMaximize)
        
        products = {}
        raw_materials = {}

        #Create Lp variables for products and raw materials
        for key in self.product_types:
            products[key] = pulp.LpVariable(key, lowBound=self.minimum_production[key], cat=pulp.LpInteger)  # Integer production quantities

            
        for key in self.material_types:
            raw_materials[key] = pulp.LpVariable(key, lowBound = 0, upBound=self.avail_materials[key], cat=pulp.LpInteger)  # Integer production quantities

            
        #defining the problem / objective function
        self._problem += pulp.lpSum([products[key]*self.profit[key] for key in self.product_types])
        
        
        #Constraints
        
        #Production time constraint
        self._problem += pulp.lpSum([products[key]*self.production_times[key] for key in self.product_types]) <= 3000
         
        #Raw material per product constraint
        for key in self.avail_materials:
            self._problem += pulp.lpSum([self.recipes[key1].get(key, 0)*products[key1] for key1 in self.recipes.keys()]) <= self.avail_materials[key]
            
        #Solving the optimization problem
        self._problem.solve()

        #assignment and packaging of the solution
        optimal_solution = []
        for key in products:
            optimal_solution.append((key, int(products[key].varValue)))
        
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
solution = problem.solve()
print("- An optimal solution was found:", problem._problem.status == 1)
print(f"- The objective value found is: {pulp.value(problem._problem.objective)}. The optimal value is 3229.0.")
print("- The solution contains an assignment:", len(solution) > 0)
print("- The solution is a list of 2-tuples:", type(solution) == list and all([type(sol) == tuple and len(sol) == 2 for sol in solution]) if len(solution) > 0 else False)
print("DONE\n")

print("Found solution:")
print(solution)