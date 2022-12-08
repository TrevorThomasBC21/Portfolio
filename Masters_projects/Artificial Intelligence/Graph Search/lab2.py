# MIT 6.034 Lab 2: Search
# Written by 6.034 staff

from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs
from functools import reduce

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']


# Please see wiki lab page for full description of functions and API.

#### PART 1: Helper Functions ##################################################

def path_length(graph, path):
    """Returns the total length (sum of edge weights) of a path defined by a
    list of nodes coercing an edge-linked traversal through a graph.
    (That is, the list of nodes defines a path through the graph.)
    A path with fewer than 2 nodes should have length of 0.
    You can assume that all edges along the path have a valid numeric weight."""
    path_costs = []
    if len(path) > 1:
#        if graph.get_edge(path[0], path[1]).length is None:
 #           return len(path) - 1
        for i in range(1, len(path)):
            path_costs.append(graph.get_edge(path[i-1], path[i]).length)
        return sum(path_costs)
    else:
        return 0

def has_loops(path):
    """Returns True if this path has a loop in it, i.e. if it
    visits a node more than once. Returns False otherwise."""
    searched = []
    for i in path:
        if i in searched:
            return True
        searched.append(i)
    return False

def extensions(graph, path):
    """Returns a list of paths. Each path in the list should be a one-node
    extension of the input path, where an extension is defined as a path formed
    by adding a neighbor node (of the final node in the path) to the path.
    Returned paths should not have loops, i.e. should not visit the same node
    twice. The returned paths should be sorted in lexicographic order."""
    new_frontier = graph.get_neighbors(path[-1])
    new_paths = []
    for i in new_frontier:
        if i not in path:
            new_path = path + [i]
            new_paths.append(new_path)
    return new_paths


def sort_by_heuristic(graph, goalNode, nodes):
    """Given a list of nodes, sorts them best-to-worst based on the heuristic
    from each node to the goal node. Here, and in general for this lab, we
    consider a smaller heuristic value to be "better" because it represents a
    shorter potential path to the goal. Break ties lexicographically by 
    node name."""
    for i in range(len(nodes) - 1):
        for node in range(len(nodes) - i - 1):
            heur_1 = graph.get_heuristic_value(nodes[node], goalNode)
            heur_2 = graph.get_heuristic_value(nodes[node + 1], goalNode)
            if heur_1 > heur_2:
                nodes[node], nodes[node + 1] = nodes[node + 1], nodes[node]
            elif heur_1 == heur_2:
                if ord(nodes[node]) > ord(nodes[node + 1]):
                    nodes[node], nodes[node + 1] = nodes[node + 1], nodes[node]
    return nodes

# You can ignore the following line.  It allows generic_search (PART 3) to
# access the extensions and has_loops functions that you just defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE


#### PART 2: Basic Search ######################################################

def basic_dfs(graph, startNode, goalNode):
    """
    Performs a depth-first search on a graph from a specified start
    node to a specified goal node, returning a path-to-goal if it
    exists, otherwise returning None.
    Uses backtracking, but does not use an extended set.
    """
    frontier = [startNode]
    if startNode in graph.nodes and goalNode in graph.nodes:
        while frontier is not []:
            current_path = list(frontier.pop())
            new_paths = extensions(graph, current_path)
            new_paths.reverse()
            frontier += new_paths
            if current_path[-1] == goalNode:
                return current_path
    return None

def basic_bfs(graph, startNode, goalNode):
    """
    Performs a breadth-first search on a graph from a specified start
    node to a specified goal node, returning a path-to-goal if it
    exists, otherwise returning None.
    """
    frontier = [startNode]
    if startNode in graph.nodes and goalNode in graph.nodes:
        while frontier is not []:
            current_path = list(frontier.pop(0))
            new_paths = extensions(graph, current_path)
            frontier += new_paths
            if current_path[-1] == goalNode:
                return current_path
    return None


#### PART 3: Generic Search ####################################################

# Generic search requires four arguments (see wiki for more details):
# sort_new_paths_fn: a function that sorts new paths that are added to the agenda
# add_paths_to_front_of_agenda: True if new paths should be added to the front of the agenda
# sort_agenda_fn: function to sort the agenda after adding all new paths 
# use_extended_set: True if the algorithm should utilize an extended set


# Define your custom path-sorting functions here.
# Each path-sorting function should be in this form:
# def my_sorting_fn(graph, goalNode, paths):
#     # YOUR CODE HERE
#     return sorted_paths
def hc_sorter(graph, goalNode, paths):
    hc_sorted = paths
    for i in range(len(hc_sorted) - 1):
        for j in range(len(hc_sorted) - i - 1):
            if graph.get_heuristic_value(hc_sorted[j][-1], goalNode) > graph.get_heuristic_value(hc_sorted[j + 1][-1], goalNode):
                hc_sorted[j], hc_sorted[j + 1] = hc_sorted[j + 1], hc_sorted[j]
    return hc_sorted
    
def path_sorter(graph, goalNode, paths):
    paths_sorted = paths
    for i in range(len(paths_sorted) - 1):
        for j in range(len(paths_sorted) - i - 1):
            if path_length(graph, paths_sorted[j]) > path_length(graph, paths_sorted[j + 1]):
                paths_sorted[j], paths_sorted[j + 1] = paths_sorted[j + 1], paths_sorted[j]
    return paths_sorted

def hc_plus_path_sorter(graph, goalNode, paths):
    cost_sorter = paths
    for i in range(len(cost_sorter) - 1):
        for j in range(len(cost_sorter) - i - 1):
            total_cost_1 = path_length(graph, cost_sorter[j]) + graph.get_heuristic_value(cost_sorter[j][-1], goalNode)
            total_cost_2 = path_length(graph, cost_sorter[j + 1]) + graph.get_heuristic_value(cost_sorter[j + 1][-1], goalNode)
            if total_cost_1 > total_cost_2:
                cost_sorter[j], cost_sorter[j + 1] = cost_sorter[j + 1], cost_sorter[j]
    return cost_sorter


generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

generic_hill_climbing = [hc_sorter, True, do_nothing_fn, False]

generic_best_first = [hc_sorter, True, hc_sorter, False]

generic_branch_and_bound = [do_nothing_fn, False, path_sorter, False]

generic_branch_and_bound_with_heuristic = [do_nothing_fn, False, hc_plus_path_sorter, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn, False, path_sorter, True]

generic_a_star = [do_nothing_fn, False, hc_plus_path_sorter, True]


# Here is an example of how to call generic_search (uncomment to run):
# my_dfs_fn = generic_search(*generic_dfs)
# my_dfs_path = my_dfs_fn(GRAPH_2, 'S', 'G')
# print(my_dfs_path)

# Or, combining the first two steps:
# my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
# print(my_dfs_path)


### OPTIONAL: Generic Beam Search

# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = False

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
# def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
#     # YOUR CODE HERE
#     return sorted_beam_agenda

generic_beam = [None, None, None, None]


# Uncomment this to test your generic_beam search:
# print(generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2))


#### PART 4: Heuristics ########################################################

def is_admissible(graph, goalNode):
    """Returns True if this graph's heuristic is admissible; else False.
    A heuristic is admissible if it is either always exactly correct or overly
    optimistic; it never over-estimates the cost to the goal."""
    nodes = graph.nodes
    sp_finder = generic_search(*generic_branch_and_bound_with_extended_set)
    for node in nodes:
        shortest_path = sp_finder(graph, node, goalNode)
        path_cost = path_length(graph, shortest_path)
        heur_cost = graph.get_heuristic_value(node,goalNode)
        if path_cost < heur_cost:
            return False
    else:
        return True

def is_consistent(graph, goalNode):
    """Returns True if this graph's heuristic is consistent; else False.
    A consistent heuristic satisfies the following property for all
    nodes v in the graph:
        Suppose v is a node in the graph, and N is a neighbor of v,
        then, heuristic(v) <= heuristic(N) + edge_weight(v, N)
    In other words, moving from one node to a neighboring node never unfairly
    decreases the heuristic.
    This is equivalent to the heuristic satisfying the triangle inequality."""
    arcs = graph.edges
    for arc in arcs:
        current_heur = graph.get_heuristic_value(arc.startNode, goalNode)
        next_heur = graph.get_heuristic_value(arc.endNode, goalNode)
        path_cost = arc.length
        difference = 0
        if current_heur > next_heur:
            difference = current_heur - next_heur
        else:
            difference = next_heur - current_heur
        if path_cost < difference:
            return False
    return True


### OPTIONAL: Picking Heuristics

# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True.
#  Note that you MUST have completed generic a_star in order to do this:
TEST_HEURISTICS = False


# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [None, None, None, None, None]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G


# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [None, None, None, None, None]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G


# heuristic_3: admissible but A* returns non-optimal path to G

[h3_S, h3_A, h3_B, h3_C, h3_G] = [None, None, None, None, None]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G


# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [None, None, None, None, None]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G


##### PART 5: Multiple Choice ##################################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '1'

ANSWER_4 = '3'


#### SURVEY ####################################################################

NAME = "Trevor Thomas"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 11
WHAT_I_FOUND_INTERESTING = "The generic search algorithm, while difficult to understand at first, was a cool way to generalize the search functions."
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the online tester. DO NOT CHANGE!

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]

# Creates the beam search using generic beam args, for optional beam tests
beam = generic_search(*generic_beam) if TEST_GENERIC_BEAM else None

# Creates the A* algorithm for use in testing the optional heuristics
if TEST_HEURISTICS:
    a_star = generic_search(*generic_a_star)
