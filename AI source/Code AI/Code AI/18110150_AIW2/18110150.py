
from collections import deque
import pydot

class State(object):
    """ Initialize state with missionaries and cannibals at
    left hand side. Boat=1 means boat is on the left hand side 
    and Boat=0 means boat is on the right hand side
    """
    def __init__(self, missionaries, cannibals, boat, by_move):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat = boat
        self.by_move = by_move


    def __str__(self):
        return "%s, %s %s %s" %(self.by_move, self.missionaries, self.cannibals, self.boat)

    def is_valid(self):
        if self.missionaries < 0 or self.missionaries > 3:
            return False
        if self.cannibals < 0 or self.cannibals > 3:
            return False
        if self.boat > 1 or self.boat < 0:
            return False
        if self.missionaries < self.cannibals and self.missionaries > 0:
            return False
        # Check for the other side
        if self.missionaries > self.cannibals and self.missionaries < 3 :
            return False

        return True
        
    def is_goal(self):
        return self.missionaries == 0 and self.cannibals == 0 and self.boat == 0

    def new_states(self):
        op = -1 # Subtract
        boat_move = "from left shore to right"
        if self.boat == 0:
            op = 1 # Add
            boat_move = "from right shore to left"

        for x in range(3):
            for y in range(3):
                by_move = "Move %s missionaries and %s cannibals %s" %(x, y, boat_move)
                new_state = State(self.missionaries + op*x, self.cannibals + op*y, self.boat + op*1, by_move)
                if x+y >= 1 and x+y <= 2 and new_state.is_valid():
                    yield new_state
        

class Node(object):
    def __init__(self, parent, state, depth):
        self.parent = parent
        self.state = state
        self.depth = depth
        self.dot_node = pydot.Node(str(self), style="filled", fillcolor=self.get_depth_color())

    def get_depth_color(self):
        colors = ["aliceblue", "antiquewhite", "aquamarine2", 
                  "cadetblue1", "darkslategray1", "grey100", "wheat",
                  "khaki", "lightyellow", "lightblue1", "pink", "lawngreen"]
        return colors[self.depth % 12]

    def __str__(self):
        return self.state.__str__()


    def childrens(self):
        for state in self.state.new_states():
            yield Node(parent=self, state=state, depth=self.depth+1)

    def extract_solution(self):
        print ("Extracting soln")
        solution = []
        node = self
        solution.append(node)
        while node.parent is not None:
            solution.append(node.parent)
            node = node.parent
        solution.reverse()
        return solution
def bfs(root):
    graph = pydot.Dot(graph_type='digraph')
    graph.add_node(root.dot_node)
    
    queue = deque([root])
    test_list = [] # For avoiding duplicates
    while True:
        if not queue:
            return None
        node = queue.popleft()
        if str(node) in test_list:
            continue
        test_list.append(str(node))

        dot_node = node.dot_node
        graph.add_node(node.dot_node)
        if node.parent:
            graph.add_edge(pydot.Edge(node.parent.dot_node, node.dot_node))
        if node.state.is_goal():
            graph.write_png('solution.png')
            return node.extract_solution()

        for child in node.childrens():
            queue.append(child)



def main():
    initial_state = State(3, 3, 1, "Initial State")
    root = Node(parent=None, state=initial_state, depth=0)
    for state in bfs(root):
        print (state)

if __name__ == '__main__':
    main()