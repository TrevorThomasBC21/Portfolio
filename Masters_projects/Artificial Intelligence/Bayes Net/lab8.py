# MIT 6.034 Lab 8: Bayesian Inference
# Written by 6.034 staff

from nets import *


#### Part 1: Warm-up; Ancestors, Descendents, and Non-descendents ##############

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    ancestry = net.get_parents(var)
    for i in net.get_parents(var):
        ancestry = get_ancestors(net, i) | ancestry
    return ancestry

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    desc = net.get_children(var)
    for i in net.get_children(var):
        desc = get_descendants(net, i) | desc
    return desc

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    all_vars = set(net.get_variables())
    for i in get_descendants(net, var):
        all_vars.discard(i)
    all_vars.remove(var)
    return all_vars


#### Part 2: Computing Probability #############################################

def simplify_givens(net, var, givens):
    """
    If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens.
    """
    parents = net.get_parents(var)
    descendants = get_descendants(net, var)
    keys = givens.keys()
    if all(elem in keys for elem in parents):
        for d in descendants:
            if d in keys:
                return givens
        new_givens = {}#
        for key in parents:#
            new_givens[key] = givens[key]#
        return new_givens#
    return givens
        
    
def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"

    hypo_key = [i for i in hypothesis.keys()][0]
    if givens is None:
        try:
            return net.get_probability(hypothesis)
        except:
            raise LookupError
    simple = simplify_givens(net, hypo_key, givens)
    try:
        return net.get_probability(hypothesis, simple)
    except:
        raise LookupError

def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    reverse_nodes = sorted(net.topological_sort(), reverse=True)
    j_prob = 1
    for node in reverse_nodes:
        temp_hypo = {node: hypothesis[node]}
        parents = net.get_parents(node)
        conditions = {}
        if parents is not set():
            for p in parents:
                conditions.update({p : hypothesis[p]})
        j_prob *= probability_lookup(net, temp_hypo, conditions)
    return j_prob
    
def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    nodes = net.get_variables()
    permutations = net.combinations(nodes, hypothesis)
    marg_prob = 0
    for perm in permutations:
        marg_prob += probability_joint(net, perm)
    return marg_prob

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    def key_finder(dictionary):
        return [i for i in dictionary.keys()][0]    
    events = hypothesis
    if givens:
        hyp_key = key_finder(hypothesis)
        giv_key = key_finder(givens)
        if hyp_key == giv_key:
            if hypothesis[hyp_key] == givens[giv_key]:
                return 1
            else:
                return 0
        events.update(givens)
    p_intersection = probability_marginal(net, events)
    p_evidence = probability_marginal(net, givens)
    p_conditional = p_intersection/p_evidence
    return p_conditional


    
def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    return probability_conditional(net, hypothesis, givens)


#### Part 3: Counting Parameters ###############################################

def number_of_parameters(net):
    """
    Computes the minimum number of parameters required for the Bayes net.
    """
    nodes = net.get_variables()
    params = []
    for node in nodes:
        parents = net.get_parents(node)
        node_value = len(net.get_domain(node)) - 1
        conditional = 1
        for parent in parents:
            parent_domain = len(net.get_domain(parent))
            conditional *= parent_domain
        params.append(conditional*node_value)
    return sum(params)

#### Part 4: Independence ######################################################

def is_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    otherwise False. Uses numerical independence.
    """
    var1_dom = net.get_domain(var1)
    var2_dom = net.get_domain(var2)
    if givens is not None:
        for val1 in var1_dom:
            for val2 in var2_dom:
                hypo = {var1: val1}
                condition = {var2: val2}
                condition.update(givens)
                prob_1 = probability(net, hypo, givens)
                prob_2 = probability(net, hypo, condition)
                if not approx_equal(prob_1, prob_2):
                    return False
        return True
    else:
        for val1 in var1_dom:
            for val2 in var2_dom:
                hypo = {var1: val1}
                condition = {var2: val2}
                prob_1 = probability(net, hypo)
                prob_2 = probability(net, hypo, condition)
                if not approx_equal(prob_1, prob_2):
                    return False
            return True
    
def is_structurally_independent(net, var1, var2, givens=None):
    """
    Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence).
    """

    if givens is None:
        if net.find_path(var1, var2) is not None:
            return False
        return True
    nodes = net.get_variables()
    searched = []
    for node in nodes:
        parents = net.get_parents(node)
        for parent1 in parents:
            for parent2 in parents:
                if parent1 != parent2 and parent1 not in searched and parent2 not in searched:
                    net.link(parent1, parent2)
                    searched.append(parent1)
                    searched.append(parent2)
    net.make_bidirectional()
    for given in givens:
        if given in nodes:
            net.remove_variable(given)
    struct_independence = net.find_path(var1, var2)
    if struct_independence is not None:
        return False
    return True

        


#### SURVEY ####################################################################

NAME = "Trevor Thomas"
COLLABORATORS = None
HOW_MANY_HOURS_THIS_LAB_TOOK = 15
WHAT_I_FOUND_INTERESTING = "Part 2: Probability"
WHAT_I_FOUND_BORING = None
SUGGESTIONS = "After finding the original assignment description for the MIT assignment (https://ai6034.mit.edu/wiki/index.php?title=Lab_8), I found a link in the description to a pdf called 'd-separation.'  This link does not contain any answers or hints, but it provides an excellent description of what the lab is referring to by 'structural independence'.  I think including this with the lab8 files would be extremely helpful, as the docstring in the final function provides little detail."
