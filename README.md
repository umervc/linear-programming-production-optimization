# Linear Programming — Production Planning Optimization

A PuLP-based integer linear programming solution for production planning and scheduling, built as part of **1BK50: Algorithmic Programming for Operations Management** at **Eindhoven University of Technology (TU/e)**.

---

## Assignment Overview

A manufacturing company produces multiple product types from a set of raw materials, each with limited availability. Each product has a recipe (material requirements), a production time, a minimum production quantity enforced by customer contracts, and a profit margin. The objective across all exercises is to determine the optimal production plan that maximizes total profit, subject to material, time, and workforce constraints.

---

## Exercises

### Exercise 1 — Base ILP Model
Formulates and solves the core integer linear program using a hardcoded problem instance. Decision variables represent integer production quantities per product type. Constraints enforce material availability, a global production time budget of 3000 time units, and minimum production quantities per product. Returns a list of (product, quantity) tuples representing the optimal plan.

### Exercise 2 — File-Based Problem Loading
Extends Exercise 1 with a `load()` function that parses product and material data from structured text files, decoupling the model from hardcoded instances. Handles type conversion and dictionary parsing to populate all class attributes, allowing the same solver to run across multiple problem instances without modification.

### Exercise 3 — Employee-Aware Scheduling
Introduces a workforce dimension: each employee is only eligible to produce a subset of products and operates at a product-specific speed multiplier that scales actual production time. Adds per-employee availability constraints alongside the existing material and time constraints. The decision variable becomes a (product, quantity, employee) assignment, requiring a 2D variable space over employees and products.

### Exercise 4 — Timeslot-Based Scheduling
Moves from aggregate quantity planning to explicit timeslot scheduling. Each product is assigned to a specific employee and discrete timeslot, with constraints ensuring no employee works on more than one product simultaneously, production fits within the available timeslot window, and a global active-work budget is respected. Introduces a binary 3D decision variable over (product, employee, timeslot).

### Exercise 5 — Priority-Constrained Production Slots
Extends Exercise 4 by introducing a priority system: within each employee's schedule, higher-priority products must be produced before lower-priority ones. Production slots must be filled sequentially with no gaps. Implements an auxiliary binary variable Y[p, p_other, e] to encode ordering relationships between products, enabling priority enforcement through linear constraints.

---

## Skills Demonstrated

### Integer Linear Programming (PuLP)
Formulated and solved ILP problems of increasing complexity using PuLP — defining decision variables, objective functions, and constraint sets from scratch, and interpreting solver output into structured results.

### Mathematical Modelling
Translated real-world operational constraints — material availability, workforce capacity, production speed multipliers, timeslot granularity, and priority ordering — into precise mathematical formulations suitable for a linear solver.

### Multi-Dimensional Decision Variables
Progressed from scalar production quantities to 2D employee-product and 3D product-employee-timeslot binary variable spaces, managing variable indexing and constraint scoping across increasingly complex combinatorial structures.

### Constraint Engineering
Designed and implemented a range of constraint types including resource capacity constraints, individual and aggregate time budgets, mutual exclusion constraints for concurrent production, boundary constraints for timeslot feasibility, and sequentiality and priority-ordering constraints using auxiliary variables.

### Data Ingestion and Model Flexibility
Implemented file-based data loading using Pandas and `ast.literal_eval`, ensuring the solver generalises across problem instances without code changes — a practical requirement for any reusable optimisation tool.

### Scheduling Under Combinatorial Complexity
Addressed the NP-hard nature of timeslot and priority scheduling by carefully scoping constraints to avoid redundancy, and by structuring the variable space to keep the problem tractable within PuLP's default solver.

---

## Getting Started

**Prerequisites:**
```bash
pip install pulp pandas
```

**Run any exercise:**
```bash
python Optimization_ex1_final.py
python Optimization_ex2_final.py
python Optimization_ex3_final.py
python Optimization_ex4_final.py
python Optimization_ex5_final.py
```

Note: Exercises 2 and 3 require the corresponding `.txt` data files to be in the same directory.

---

## Files

| File | Description |
|---|---|
| `Optimization_ex1_final.py` | Base ILP model |
| `Optimization_ex2_final.py` | + File-based data loading |
| `Optimization_ex3_final.py` | + Employee scheduling |
| `Optimization_ex4_final.py` | + Timeslot-based scheduling |
| `Optimization_ex5_final.py` | + Priority-constrained production slots |
| `2_1_products.txt`, `2_1_materials.txt` | Problem instance 1 for Exercise 2 |
| `2_2_products.txt`, `2_2_materials.txt` | Problem instance 2 for Exercise 2 |
| `3_1_products.txt`, `3_1_materials.txt`, `3_1_employees.txt` | Problem instance 1 for Exercise 3 |
| `3_2_products.txt`, `3_2_materials.txt`, `3_2_employees.txt` | Problem instance 2 for Exercise 3 |
