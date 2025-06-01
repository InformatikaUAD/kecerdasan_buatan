from collections import deque


class Graph:
    def __init__(self, graph_dict=None, directed=False):
        self.graph_dict = graph_dict or {}
        self.directed = directed

    def get(self, a):
        return self.graph_dict.get(a, {})


class Problem:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def goal_test(self, state):
        return state == self.goal


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def expand(self, problem):
        return [
            self.child_node(problem, action) for action in problem.actions(self.state)
        ]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        new_cost = problem.path_cost(self.path_cost, self.state, action, next_state)
        return Node(next_state, self, action, new_cost)

    def solution(self):
        return [node.state for node in self.path()[::-1]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return path_back

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state


city_map = Graph(
    dict(
        Jakarta=dict(Bandung=150, Yogyakarta=500, Surabaya=700),
        Bandung=dict(Jakarta=150, Semarang=400),
        Yogyakarta=dict(Jakarta=500, Surabaya=300),
        Surabaya=dict(Jakarta=700, Yogyakarta=300, Denpasar=800),
        Semarang=dict(Bandung=400, Surabaya=350),
        Denpasar=dict(Surabaya=800, Makassar=1200),
        Makassar=dict(Denpasar=1200),
    ),
    directed=True,
)


class CityProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, A):
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        return action

    def path_cost(self, cost, A, action, B):
        return cost + (self.graph.get(A).get(B) or infinity)


def breadth_first_search(problem):
    global track_path
    frontier = deque([Node(problem.initial)])
    explored = set()
    track_path = [problem.initial]
    while frontier:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        expanded = node.expand(problem)
        for child in expanded:
            # Pastikan child belum ada di explored dan frontier
            if child.state not in explored and all(
                child.state != n.state for n in frontier
            ):
                track_path.append(child.state)
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
    return None


if __name__ == "__main__":
    start = "Jakarta"
    goal = "Denpasar"
    infinity = float("inf")
    track_path = []

    city_problem = CityProblem(start, goal, city_map)
    node = breadth_first_search(city_problem)

    if node is not None:
        final_path = node.solution()

        total_cost = 0
        for i in range(len(final_path) - 1):
            A = final_path[i]
            B = final_path[i + 1]
            cost = city_map.get(A).get(B, infinity)
            total_cost += cost

        print("TRACKING PATH: ", " -> ".join(track_path))
        print("SOLUTION PATH: ", " -> ".join(final_path))
        print("COST: ", total_cost)
    else:
        print("Tidak ditemukan solusi.")