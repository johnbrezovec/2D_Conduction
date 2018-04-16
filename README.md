2-D Conduction Solver by Finite Difference Method
-----------------------

This repo contains three scripts to assist in the solving and visualization
of 2-d conduction problems.

**`equation_builder.py`** provides the framework to build the equations
required for the finite difference method as well as the coordinate mappings
required for visualization.
  - resolution of the solution can be adjusted by changing the dimensions of the nodal system in this file.

**`multidim_conduction_solver.py`** reads in the equations generated by the
previous script, and solves the system using sparse matrix methods.

**`plot_solution.R`** visualizes the solution to the given conduction problem.
Currently, it is setup to accommodate 2-fold reflectional symmetry.

---
### example result
the following solution was generated with a 50x50 nodal system (2500 equations).
The left and right sides of the system are held at a constant 30ºC while the inner portion is held at 230ºC. Top and bottom are perfectly insulated.
![visualization example](https://github.com/johnbrezovec/2D_Conduction/blob/master/plot.png "example")

---
**dependencies:**

* python: `numpy`, `scipy`, `subprocess`

* R: `ggplot2`, `viridis`

_created for the honors option for CHE 350, John Brezovec_
