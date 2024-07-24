import sys


# You would want to store the information about every state transitions and actions taken
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# Using StackFrontier, you achieve last in first out, this provides for Depth First Search(DFS)
class StackFrontier():
    def __init__(self):
        # It could contain an array that hold the nodes
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        # In stack frontier, the last append value goes out first
        node = self.frontier[-1]
        # Remove the node from the stack
        self.frontier = self.frontier[:-1]
        # Return the node that is removed
        return node

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)


# Using QueueFrontier, you achieve First In First Out, this provides for Breadth First Search (BFS)
# QueueFrontier has similar functions as the StackFrontier other than the remove function, hence it inherits
# those funcions from StackFrontier.
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")

        node = self.frontier[0] # first element from the frontier
        self.frontier = self.frontier[1:]
        return node

class Maze:
    # Maze is initialized with the source filepath
    def __init__(self, filename):
        self.filename = filename

        # Read the content of the file name
        with open(self.filename) as f:
            self.contents = f.read()

        # Validate start and goal
        if self.contents.count('A') != 1:
            raise Exception(" Maze must have exactly one start point")

        if self.contents.count('B') != 1:
            raise Exception(" Maze must have exactly one goal")

        # Figure out the structure of the maze by noting the walls, path,
        # start point and goal
        self.contents = self.contents.splitlines()
        self.walls = []

        for i, row in enumerate(self.contents):
            wall_unit = []
            for j, column in enumerate(row):
                if column == 'A':
                    self.start = (i, j)
                    wall_unit.append(False)
                elif column == 'B':
                    self.goal = (i, j)
                    wall_unit.append(False)
                elif column == ' ':
                    wall_unit.append(False)
                else:
                    wall_unit.append(True)

            self.walls.append(wall_unit)

        # Also define a solutions variable

        self.solution = None

    def solve(self):
        # We begin at the start point
        # Create an initial node
        initial_node = Node(state=self.start, parent=None, action=None)
        # Create a frontier object
        frontier = StackFrontier()
        # Add the initial node to the frontier
        frontier.add(initial_node)

        # Create an empty explored set
        self.explored = set()

        while True:
            # If there is nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # pick an element from the frontier
            current_node = frontier.remove()
            # if element is goal, return the solution path

            if current_node.state == self.goal:
                cells = []
                actions = []
                while current_node.parent is not None:
                    cells.append(current_node.state)
                    actions.append(current_node.action)
                    current_node = current_node.parent
                cells.reverse()
                actions.reverse()

                # solution is a list of tuples
                self.solution = (actions, cells)
                return self.solution

            # Mark node as explored
            self.explored.add(current_node.state)

            neighbours_list = self.neighbours(current_node.state)
            for action, state in neighbours_list:
                if state not in self.explored and not frontier.contains_state(state):
                    child = Node(state=state, action=action, parent=current_node)
                    frontier.add(child)

    def neighbours(self, state):
        true_neighbours = []
        x, y = state
        all_neighbours = [
            ("left", (x - 1, y)),
            ("right", (x + 1, y)),
            ("down", (x, y - 1)),
            ("up", (x, y + 1))
        ]

        for action, (i,j) in all_neighbours:
            if i >= 0 and j >= 0:
                try:
                    if not self.walls[i][j]:
                        true_neighbours.append((action, (i, j)))
                except IndexError:
                    continue

        return true_neighbours

    # This function prints the maze
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        # print based on walls, start and goal point information
        for i, row in enumerate(self.walls):
            for j, column in enumerate(row):
                if column:
                    print("#", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i,j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()


# The user should run this program along with the maze source file
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

source_file = sys.argv[1]
print("sys.argv: ", sys.argv)
print("sys.argv[1]: ", sys.argv[1])

# source_file = input("Enter filename: ")

# Initializing the Maze class
print("Loading maze...")
m = Maze(source_file)
m.print()

print("Solving maze... ")
m.solve()
m.print()


