from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        
        # Initialize the explored dictionary to be empty
        explored = {}
        distance = {grid.start: True}

        # Initialize the frontier with the initial node
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        while True:
            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)
            
            # Remove a node from the frontier
            node = frontier.pop()
            
            # Add the node to the explored dictionary
            explored[node.state] = True
            
            # Return if the node contains a goal state
            if node.state == grid.end:
                return Solution(node, explored)
            
            # UCS
            for action, state in grid.get_neighbours(node.state).items():
                cost = node.cost + grid.get_cost(state)

                if state in distance:
                    continue

                distance[state] = True

                new_node = Node("", state, cost)
                new_node.parent = node
                new_node.action = action

                frontier.add(new_node, priority = cost)
