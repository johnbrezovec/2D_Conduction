__doc__ = """
John Brezovec 2018

Helper script to build the relevant finite difference equations
for a 2-d conduction problem. These equations can be solved and
visualized using multidim_conduction_solver.py
"""


class node(object):
    """
    very simple node class, just contains index of the node, the coordinates
    of the node, as well as the equation for the particular node
    """

    def __init__(self, index, col, row):
        self.index = index
        self.col = col
        self.row = row
        self.leftside = []
        self.rightside = []
        self.type = None

    def __repr__(self):
        if self.type in (None, 0):
            return str(0)
        leftstring = ""
        rightstring = ""
        for n in self.leftside:
            leftstring += str(n)
        for n in self.rightside:
            if rightstring == "":
                rightstring += str(n)
            else:
                rightstring += " + " + str(n)
        return leftstring + " == " + rightstring

    def init_eq(self):
        if self.type == 0:
            pass
        if self.type == 'outer':
            self.leftside.append("To")
            self.rightside.append("T{}".format(self.index))
        if self.type == 'inner':
            self.leftside.append("Ti")
            self.rightside.append("T{}".format(self.index))
        if self.type == 'bulk':
            self.leftside.append("0")
            # constructing right side of equation
            rightside = []
            above = [0, None]
            below = [0, None]
            left = [0, None]
            right = [0, None]
            # look above
            try:
                if self.row - 1 < 0:
                    raise IndexError
                above[1] = nodalSys[self.row - 1][self.col].index
                above[0] += 1
            except IndexError:
                below[0] += 1
            try:
                below[1] = nodalSys[self.row + 1][self.col].index
                below[0] += 1
            except IndexError:
                above[0] += 1
            try:
                right[1] = nodalSys[self.row][self.col + 1].index
                right[0] += 1
            except IndexError:
                left[0] += 1
            try:
                if self.col - 1 < 0:
                    raise IndexError
                left[1] = nodalSys[self.row][self.col - 1].index
                left[0] += 1
            except IndexError:
                right[0] += 1
            if above[1] is not None:
                rightside.append("{}T{}".format(above[0], above[1]))
            if below[1] is not None:
                rightside.append("{}T{}".format(below[0], below[1]))
            if left[1] is not None:
                rightside.append("{}T{}".format(left[0], left[1]))
            if right[1] is not None:
                rightside.append("{}T{}".format(right[0], right[1]))
            rightside.append("-4T{}".format(self.index))
            self.rightside.extend(rightside)


def initNodalSys(nrows, ncols):
    # makes a nrows x ncols 'matrix' of lists
    return [[[] for _ in range(ncols)] for _ in range(nrows)]


def initNodes(nodalSys):
    index = 1
    for row in range(len(nodalSys)):
        for col in range(len(nodalSys[0])):
            if nodalSys[row][col] == []:
                nodalSys[row][col] = node(index, col, row)
                index += 1
            else:
                pass
    # no need to return anything since we're directly mutating the list


# initializing the node types for my particular setup
nrows = 50
ncols = 50
nodalSys = initNodalSys(nrows, ncols)

rowcounter = 0
for i in range(nrows):
    for n in range(int(ncols * 0.6) + rowcounter, nrows):
        nodalSys[i][n] = 0
    rowcounter += 1

initNodes(nodalSys)
# assign outer nodes
for n in range(nrows):
    nodalSys[n][0].type = 'outer'
# assign inner nodes
i = 0
for n in range(int(0.6 * ncols) - 1, ncols):
    print(i, n, nodalSys[i][n].index)
    nodalSys[i][n].type = "inner"
    i += 1

# make the rest bulk
for row in range(len(nodalSys)):
    for col in range(len(nodalSys[0])):
        try:
            if nodalSys[row][col].type is None:
                nodalSys[row][col].type = 'bulk'
            nodalSys[row][col].init_eq()
        except AttributeError:
            pass

# now store the results
with open("equations.txt", "w") as f:
    f.write("# CONSTANT # To = 30\n")
    f.write("# CONSTANT # Ti = 230\n")
    f.write("## START EQUATIONS ##\n")
    for n in nodalSys:
        for i in n:
            if str(i) == "0":
                continue
            f.write(str(i) + "\n")
    f.write("## END ##")

# now create the node coordinate file
with open("index_coordinates.csv", "w") as f:
    f.write("index, x, y\n")
    for n in nodalSys:
        for i in n:
            if str(i) == "0":
                continue
            index = str(i.index)
            x = str(i.col)
            y = str(nrows - i.row - 1)
            f.write(index + ", " + x + ", " + y + "\n")
