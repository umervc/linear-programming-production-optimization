# -*- coding: utf-8 -*-
"""
This is the final solution for Assignment 3 of optimization assignment for course
Algorithmic programming for operations management [1BK50]
by Muhammad Umer 1686909
and Lars Wouters 1725076
"""

#importing libraries
import pulp
import math
        
class ProductionPlant:
    def __init__(self):
        self.material_types = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10']
        self.product_types = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
        self.avail_materials = {'M1': 75, 'M2': 90, 'M3': 85, 'M4': 60, 'M5': 70, 'M6': 95, 'M7': 55, 'M8': 100, 'M9': 80, 'M10': 50}
        self.recipes = {'P1': {'M1': 3, 'M2': 2, 'M3': 1, 'M4': 4},
                        'P2': {'M1': 1, 'M2': 4, 'M3': 2, 'M4': 3},
                        'P3': {'M1': 2, 'M3': 3, 'M5': 4, 'M7': 1},
                        'P4': {'M4': 3, 'M6': 2, 'M8': 1, 'M9': 4},
                        'P5': {'M2': 4, 'M5': 1, 'M7': 3, 'M8': 2},
                        'P6': {'M3': 1, 'M8': 4, 'M9': 3, 'M1': 2},
                        'P7': {'M1': 4, 'M6': 3, 'M9': 2, 'M2': 1},
                        'P8': {'M4': 2, 'M7': 1, 'M8': 3, 'M3': 4},
                        'P9': {'M5': 3, 'M6': 4, 'M9': 1, 'M4': 2},
                        'P10': {'M5': 1, 'M6': 2, 'M9': 4, 'M4': 3},}

        self.production_times = {'P1': 2.5, 'P2': 1.5, 'P3': 2.0, 'P4': 1.8, 'P5': 1.2, 'P6': 2.3, 'P7': 1.7, 'P8': 2.1, 'P9': 1.9, 'P10': 1.0}
        self.minimum_production = {'P1': 1, 'P2': 2, 'P3': 1, 'P4': 1, 'P5': 2, 'P6': 3, 'P7': 3, 'P8': 2, 'P9': 1, 'P10': 3}
        self.profit = {'P1': 7, 'P2': 10, 'P3': 8, 'P4': 20, 'P5': 17, 'P6': 11, 'P7': 25, 'P8': 18, 'P9': 8, 'P10': 31}
    
        self.employees = ['E1', 'E2', 'E3', 'E4', 'E5']
        self.max_timeslots_per_employee = 20;
        self.max_time_for_all_employees = 60;

        self.max_timeslots = int(self.max_time_for_all_employees/len(self.employees));
        self.timeslots = list(range(0,self.max_timeslots))

    def solve(self):
        self._problem = pulp.LpProblem( "MaxProf",  pulp.LpMaximize)
        
        products = {}
        raw_materials = {}

        #Create Lp variables for products and raw materials
        for key in self.product_types:
            products[key] = pulp.LpVariable(key, lowBound=self.minimum_production[key], cat=pulp.LpInteger)  # Integer production quantities

            
        for key in self.material_types:
            raw_materials[key] = pulp.LpVariable(key, lowBound = 0, upBound=self.avail_materials[key], cat=pulp.LpInteger)  # Integer production quantities

        #Create Lp variable for X, where X[p,e,t] represents in binary form, whether the production of product p is started by the employee e at time t
        X = pulp.LpVariable.dicts("X", ((p, e, t) for p in self.product_types for e in self.employees for t in self.timeslots), 0, 1 , cat=pulp.LpInteger)
        
        #defining the problem / objective function
        self._problem += pulp.lpSum([X[p,e,t]*self.profit[p] for p in self.product_types for e in self.employees for t in self.timeslots])

        #Constraints

        #minimum production
        for p in self.product_types:
            self._problem += pulp.lpSum([X[p,e,t] for e in self.employees for t in self.timeslots]) >= self.minimum_production[p]
        
        #Raw material per product constraint
        for key in self.avail_materials:
            self._problem += pulp.lpSum([self.recipes[key1].get(key, 0)*sum(X[key1, e, t] for e in self.employees for t in self.timeslots) for key1 in self.recipes.keys()]) <= self.avail_materials[key]

        #Inidividual Employee availability time constraint
        for e in self.employees:
            self._problem += pulp.lpSum([X[p, e, t]*math.ceil(self.production_times[p]) for t in self.timeslots for p in self.product_types]) <= self.max_timeslots_per_employee
        
        #Restriction on the total number of time units the employees can be actively working
        self._problem += pulp.lpSum([X[p, e, t] * self.production_times[p] for e in self.employees for p in self.product_types for t in self.timeslots]) <= self.max_time_for_all_employees

        #An employee can produce at maximum only one product at the same time
        for e in self.employees:  
            for l in self.timeslots: 
                self._problem += pulp.lpSum(X[p, e, t] for p in self.product_types for t in range(max(0, int(l - math.ceil(self.production_times[p]))), l)) <= 1
        
        #All started products must be finished within the valid timeslots
        for t in self.timeslots[-math.ceil(max(self.production_times.values())):]:
            self._problem += pulp.lpSum([X[p, e, t]*(self.production_times[p] + t)] for e in self.employees for p in self.product_types) <= self.max_timeslots
        
        #Solving the optimization problem
        self._problem.solve()

        #assignment and packaging of the solution
        optimal_solution = []
        for p in self.product_types:
            for e in self.employees:
                for t in self.timeslots:
                    if pulp.value(X[p, e, t]) > 0:  # Check if the variable is set to 1 in the solution
                        optimal_solution.append((p, e, t))
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
print("- The solution contains an assignment:", len(solution) > 0)
print("- The solution is a list of 3-tuples:", type(solution) == list and all([type(sol) == tuple and len(sol) == 3 for sol in solution]) if len(solution) > 0 else False)
print("DONE\n")
print("Found solution:")
print(solution)