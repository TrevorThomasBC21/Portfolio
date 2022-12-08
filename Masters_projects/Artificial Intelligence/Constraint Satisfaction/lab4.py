# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem


#### Part 1: Warmup ############################################################

def has_empty_domains(csp) :
    """Returns True if the problem has one or more empty domains, otherwise False"""
    for variable in csp.get_all_variables():
        if not csp.get_domain(variable):
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    if not csp.constraints or not csp.assignments:
        return True
    for constraint in csp.constraints:
        a = csp.get_assignment(constraint.var1)
        b = csp.get_assignment(constraint.var2)
        if not constraint.check(a,b) and a is not None and b is not None:
            return False
    return True


#### Part 2: Depth-First Constraint Solver #####################################

def solve_constraint_dfs(problem) :
    """
    Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values)
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple.
    """
    csp_stack = [problem]
    ext = 0
    while csp_stack:
        ext += 1
        cur_prob = csp_stack.pop()
        if check_all_constraints(cur_prob) and not has_empty_domains(cur_prob):
            cur_node = cur_prob.pop_next_unassigned_var()
            if not cur_node:
                print("Number of extensions:", ext)
                return cur_prob.assignments, ext
            cur_domain = cur_prob.get_domain(cur_node)
            new_probs = []
            for val in cur_domain:
                new_csp = [cur_prob.copy().set_assignment(cur_node, val)]
                new_probs = new_csp + new_probs
            csp_stack += new_probs
    return (None, ext)


# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with DFS?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

ANSWER_1 = 20


#### Part 3: Forward Checking ##################################################

def eliminate_from_neighbors(csp, var) :
    """
    Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None.
    """
    duplicate_csp = csp.copy()
    neighbors = duplicate_csp.get_neighbors(var)
    var_domain = duplicate_csp.get_domain(var)
    reduced_domain = set()
    for neighbor in neighbors:
        constraints = duplicate_csp.constraints_between(neighbor, var)
        n_domain = duplicate_csp.get_domain(neighbor)
        for n_element in n_domain:
            const_violations = []
            for var_element in var_domain:
                for constraint in constraints:
                    if not constraint.check(n_element, var_element):
                        const_violations.append(n_element)
                    if len(const_violations) == len(var_domain):
                        csp.eliminate(neighbor, n_element)
                        if not csp.get_domain(neighbor):
                            return None
                        reduced_domain.add(neighbor)

    if has_empty_domains(csp):
        return None
    return sorted(list(reduced_domain))

""" 2/15/21
I found, by using the original CSP, that reducing the domain mid loop was messing with the for loop's ability to continue iterating.  Made some logical changes to where statements are nested.  When working on this again, my next step will be to read over the print statements (already in file) and see what can be improved.  Right now, for Test 20, my problem is that the function needs to return None as soon as B's domain is emptied.  Right now it is returning the "reduced" variable containing B.
"""
""" 2/16/21
Fixed most issues by creating a duplicate CSP to work with while making the updates to the original CSP.  This made each for loop continue despite reducing the domain of the iterable governing the for loop. Need to find a way for function to handle multiple constraints on the same two nodes.
"""
""" 2/20/21
Function now working.  Reversed order of for loops iterating on constraints and var_elements.  Problem was the function needed to 'remember' the limitations of the first constraint while analyzing the second, which was only possible if the loop iterating over the elements of the primary variable was nested in the loop iterating over constraints.  This allowed the function to look at each element for a constraint, remember which elements violate the constraint, and then repeat the process for the following constraint.  When the loops were inverted, it would check all constraints for a single element at a time, which never revealed contradictions.
"""
# Because names give us power over things (you're free to use this alias)
forward_check = eliminate_from_neighbors

def solve_constraint_forward_checking(problem) :
    """
    Solves the problem using depth-first search with forward checking.
    Same return type as solve_constraint_dfs.
    """
    csp_stack = [problem]
    ext = 0
    while csp_stack:
        cur_prob = csp_stack.pop()
        ext += 1
        if check_all_constraints(cur_prob) and not has_empty_domains(cur_prob):
            cur_node = cur_prob.pop_next_unassigned_var()
            if not cur_node:
                print("Number of extensions:", ext)
                return cur_prob.assignments, ext
            cur_domain = cur_prob.get_domain(cur_node)
            new_probs = []
            for val in cur_domain:
                new_csp = [cur_prob.copy().set_assignment(cur_node, val)]
                forward_check(new_csp[0], cur_node)
                new_probs = new_csp + new_probs
            csp_stack += new_probs
    return (None, ext)
#    nodes = problem.variables
#    for node in nodes:
#        eliminate_from_neighbors(problem, node)
#    return solve_constraint_dfs(problem)


# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking?

ANSWER_2 = 9


#### Part 4: Domain Reduction ##################################################

def domain_reduction(csp, queue=None) :
    """
    Uses constraints to reduce domains, propagating the domain reduction
    to all neighbors whose domains are reduced during the process.
    If queue is None, initializes propagation queue by adding all variables in
    their default order. 
    Returns a list of all variables that were dequeued, in the order they
    were removed from the queue.  Variables may appear in the list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None.
    This function modifies the original csp.
    """
    duplicate_csp = csp.copy()
    dequeued = []
    if not queue and queue != []:
        queue = csp.get_all_variables()
    while queue:
        node = queue.pop(0)
        dequeued.append(node)
        neighbors = csp.get_neighbors(node)
        eliminate_from_neighbors(duplicate_csp, node)
        if has_empty_domains(duplicate_csp):
            for neighbor in neighbors:
                if csp.get_domain(neighbor) != duplicate_csp.get_domain(neighbor):
                    csp.set_domain(neighbor, duplicate_csp.get_domain(neighbor))
            return None
        for neighbor in neighbors:
            if csp.get_domain(neighbor) != duplicate_csp.get_domain(neighbor):
                csp.set_domain(neighbor, duplicate_csp.get_domain(neighbor))
                if neighbor not in queue:
                    queue.append(neighbor)
    return dequeued


# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with DFS (no forward checking) if you do domain reduction before solving it?

ANSWER_3 = 6


def solve_constraint_propagate_reduced_domains(problem) :
    """
    Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs.
    """

    csp_stack = [problem]
    ext = 0
    while csp_stack:
        cur_prob = csp_stack.pop()
        ext += 1
        if check_all_constraints(cur_prob) and not has_empty_domains(cur_prob):
            cur_node = cur_prob.pop_next_unassigned_var()
            if not cur_node:
                print("Number of extensions:", ext)
                return cur_prob.assignments, ext
            cur_domain = cur_prob.get_domain(cur_node)
            new_probs = []
            for val in cur_domain:
                new_csp = [cur_prob.copy().set_assignment(cur_node, val)]
                domain_reduction(new_csp[0], [cur_node])
                new_probs = new_csp + new_probs
            csp_stack += new_probs
    return (None, ext)


#    domain_reduction(problem)
#    return solve_constraint_forward_checking(problem)


# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through reduced domains?

ANSWER_4 = 7


#### Part 5A: Generic Domain Reduction #########################################

def propagate(enqueue_condition_fn, csp, queue=None) :
    """
    Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced. Same return type as domain_reduction.
    """
    duplicate_csp = csp.copy()
    dequeued = []
    if not queue and queue != []:
        queue = csp.get_all_variables()
    while queue:
        node = queue.pop(0)
        dequeued.append(node)
        potential_queue = eliminate_from_neighbors(duplicate_csp, node)
        if potential_queue is None:
            for var in csp.get_all_variables():
                csp.set_domain(var, duplicate_csp.get_domain(var))
            return None
        for var in potential_queue:
            csp.set_domain(var, duplicate_csp.get_domain(var))
            if enqueue_condition_fn(csp, var):
                    queue.append(var)
    return dequeued

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    if len(csp.get_domain(var)) == 1:
        return True
    return False

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### Part 5B: Generic Constraint Solver ########################################

def solve_constraint_generic(problem, enqueue_condition=None) :
    """
    Solves the problem, calling propagate with the specified enqueue
    condition (a function). If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs.
    """
    csp_stack = [problem]
    ext = 0
    while csp_stack:
        ext += 1
        cur_prob = csp_stack.pop()
        if check_all_constraints(cur_prob) and not has_empty_domains(cur_prob):
            cur_node = cur_prob.pop_next_unassigned_var()
            if not cur_node:
                print("Number of extensions:", ext)
                return cur_prob.assignments, ext
            cur_domain = cur_prob.get_domain(cur_node)
            new_probs = []
            for val in cur_domain:
                new_csp = [cur_prob.copy().set_assignment(cur_node, val)]
                if enqueue_condition:
                    propagate(enqueue_condition, new_csp[0], [cur_node])
                new_probs = new_csp + new_probs
            csp_stack += new_probs
    return (None, ext)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with forward checking and propagation through singleton domains? (Don't
#    use domain reduction before solving it.)

ANSWER_5 = 8


#### Part 6: Defining Custom Constraints #######################################

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    return abs(m - n) == 1

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return not (abs(m - n) == 1)

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraints = []
    for i in range(len(variables)):
        for j in range(len(variables) - i):
            if variables[i] != variables[j+i]:
                constraints.append(Constraint(variables[i], variables[i+j], constraint_different))
    return list(constraints)

#### SURVEY ####################################################################

NAME = "Trevor Thomas"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = "17 including last week's work"
WHAT_I_FOUND_INTERESTING = "Part 2"
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
