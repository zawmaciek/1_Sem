import random
import time
from itertools import chain, combinations
from typing import Optional

import networkx
import networkx as nx


def valid_result(graph: nx.DiGraph, group: set[int]) -> bool:
    # checks if independent set is connected to the other nodes
    unconnected_nodes = set(graph.nodes) - group
    for node in unconnected_nodes:
        if not group & set(graph.successors(node)):
            return False
    return True


def get_all_maximal_independent_subsets(graph: nx.Graph) -> list[set[int]]:
    """
    https://blog.actorsfit.com/a?ID=00700-d24fd865-1a37-4932-93cc-288a39ba765b
    all maximal independent subsets contain all the non-maximal independent subsets,
    hence we can just focus on maximal ones
    """
    return [set(group) for group in nx.find_cliques(nx.complement(nx.Graph(graph)))]


def get_all_unconnected_groups(graph: networkx.DiGraph) -> list[set[int]]:
    # LEGACY
    # bruteforce, doesn't work for >10 nodes
    def powerset(nodes: list[str]) -> list[set[str]]:
        """
        https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset/1482316#1482316
        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
        """
        return [set(subset) for subset in chain.from_iterable(combinations(nodes, r) for r in range(1, len(nodes) + 1))]

    possible_groups = powerset(list(graph.nodes))
    # remove connected groups
    for edge in list(graph.edges):
        edge_set = {edge[0], edge[1]}
        groups_to_remove = list()
        for group in possible_groups:
            if edge_set.issubset(group):
                groups_to_remove.append(group)
        possible_groups = [group for group in possible_groups if group not in groups_to_remove]
    return possible_groups


def solve(graph: nx.DiGraph) -> Optional[set[int]]:
    # For bruteforce uncomment line below, and comment line 52
    # indepentent_subsets = get_all_unconnected_groups(graph)
    indepentent_subsets = get_all_maximal_independent_subsets(graph)
    sorted_all_maximal_independent_subsets = sorted(indepentent_subsets, key=lambda x: len(x), reverse=True)
    for group in sorted_all_maximal_independent_subsets:
        if valid_result(graph, group):
            print(group)
            return group
    print('no solution found')
    return None


def load_example(path: str) -> nx.DiGraph:
    # open file and process
    with open(path, 'r') as f:
        graph = nx.drawing.nx_pydot.read_dot(f)
    graph.remove_node('\\n')  # only needed if not formatted correctly
    # remove groups that aren't connected to rest of the nodes
    return graph


def create_random_directed_graph(nodes: int, edges: int) -> networkx.DiGraph:
    G = nx.DiGraph()
    for node in range(nodes):
        G.add_node(str(node))
    edges_set = set()
    for edge in range(edges):
        num_1 = random.randint(0, nodes)
        num_2 = random.randint(0, nodes)
        while num_1 == num_2:
            num_2 = random.randint(0, nodes)
        edges_set.add((str(num_1), str(num_2)))
    for edge in edges_set:
        G.add_edge(edge[0], edge[1])
    return G


def validate_solution(graph: networkx.DiGraph, solution: set[int]) -> bool:
    # check if group has no connections
    for edge in list(graph.edges):
        edge_set = {edge[0], edge[1]}
        if edge_set.issubset(solution):
            return False
    # check if every node outside of group is connected to the group
    if not valid_result(graph, solution):
        return False
    return True


if __name__ == '__main__':
    # Example
    graph = load_example('ex_1.txt')
    #graph = create_random_directed_graph(200, 14000)
    t = time.time()
    solution = solve(graph)
    print(f"time: {time.time() - t}s")
    if solution:
        print(f"RESPONSE VALID: {str(validate_solution(graph, solution)).upper()}")
