__doc__ = """
John Brezovec 2018

this file sets up and solves 2-d conduction project 4 for CHE 350, outputting
the resulting temperature distribution in a csv file.
"""
# importing needed modules
import subprocess
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

# open and read equations.txt file
with open('equations.txt', 'r') as f:
    # setup dictionary to store constants
    constants = {}
    # flag to tell when to start saving the lines
    flag = False
    raw_eq_list = []
    for line in f:
        # store line in dictionary if it's supposed to be constant
        if "CONSTANT" in line:
            line = line.replace("# CONSTANT # ", "")
            line = line.split("=")
            line = [x.strip() for x in line]  # remove whitespace
            constants[line[0]] = line[1]
            continue
        if "END" in line:  # stop after END is read
            break
        if flag:
            # save the valid lines with equations
            # also remove trailing whitespace
            raw_eq_list.append(line.rstrip('\r\n'))
        else:
            if "START" in line:  # start saving after START
                flag = True
            else:
                pass

# initialize the matrices with the correct dimensions
num_equations = len(raw_eq_list)
m_matrix = np.zeros((num_equations, num_equations))
b_vector = np.zeros((num_equations, 1))

# go through the raw equation list and shove it into the matrices.
for n in range(len(raw_eq_list)):
    # split the string on whitespace
    equation = raw_eq_list[n].split()
    # replace the constants with actual values
    # and assign + and - to variables
    for i in range(len(equation)):
        if equation[i] == "Ti":
            equation[i] = constants["Ti"]
        if equation[i] == "To":
            equation[i] = constants["To"]
        if equation[i] not in ("==", "=", "+", "-"):
            positive = True
            if i != 0:
                if equation[i - 1] == "-":
                    positive = False
            if not positive and type(equation[i]) == str:
                equation[i] = "-" + str(equation[i])
    # remove all '+' and '-" from list for peace of mind
    equation = [x for x in equation if x not in ("-", "+")]
    # actually put into the matrices now
    leftside = True
    for elem in equation:
        if elem in ("=", "=="):
            leftside = False
            continue
        # assume that there is only ever one element on the leftside of an eqn
        # and that this element will be in the b vector
        if leftside:
            b_vector[n] = elem
        # on the right side of the equation, find the coefficient and the
        # temperature index and replace the corresponding element of the
        # m matrix with this.
        else:
            elem = elem.split("T")
            if elem[0] == '':
                elem[0] = str(1)
            m_matrix[n, int(float(elem[1])) - 1] = float(elem[0])

# now solve the equation
# convert m_matrix to sparse one
m_matrix = csc_matrix(m_matrix)
# solve with sparse techniques
solution = spsolve(m_matrix, b_vector)
# output the solution in a csv file
with open("solution.csv", "w") as f:
    f.write("index, temperature\n")
    index = 1
    for row in solution:
        f.write(str(index) + ", " + str(row) + "\n")
        index += 1
# finding the heat transfer rate and the shape factor
# first we need to read in the coordinates of the indicies
# we can find the heat transfer rate in two ways, either look at the outside
# or at the inside. Since the outside is flat this will be the easier one to do

# pseudocode
# read in the indicies and save those at x = 0
outer_nodes = {}
try:
    with open('index_coordinates.csv') as f:
        for line in f:
            if 'index' in line:
                continue
            else:
                split_line = [x.strip() for x in line.split(',')]
                if split_line[1] == "0":
                    outer_nodes[int(split_line[0])] = [None, None]
except FileNotFoundError:
    print("file index_coordinates.csv does not exist")

# now we save the temperatures of the outer nodes as well as the temps of
# the nodes to the right in order to get the delta-T
for n in range(len(solution)):
    if n + 1 in outer_nodes:
        outer_nodes[n+1] = [solution[n], solution[n+1]]

# now compute the heat transfer rate per unit length
heat_xfer_rate = 0
k = 54  # thermal conductivity of carbon steel
for n in outer_nodes:
    deltaT = outer_nodes[n][1] - outer_nodes[n][0]
    heat_xfer_rate += k * deltaT
# by symmetry you have to multiply it by 4
heat_xfer_rate *= 4
print(heat_xfer_rate)
# run the R script for visualization
subprocess.check_call(['Rscript', 'plot_solution.R'], shell=False)
