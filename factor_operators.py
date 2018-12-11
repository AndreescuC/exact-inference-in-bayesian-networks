import itertools
from copy import deepcopy
from collections import namedtuple
Factor = namedtuple("Factor", ["vars", "values"])


# -------------------------
# -------Normalize---------
# -------------------------
def normalize(phi):
    normalize_factor = max(list(phi.values.values()))
    values = {k: v / normalize_factor for k, v in phi.values.items()}

    return Factor(vars=phi.vars, values=values)


# -------------------------
# -----Multiplication------
# -------------------------
def join_vars(phi1, phi2):
    new_vars = []
    for var in phi1[0]:
        if var not in new_vars:
            new_vars.append(var)
    for var in phi2[0]:
        if var not in new_vars:
            new_vars.append(var)

    return new_vars


def generate_empty_values(length):
    values = {}
    inner_list = []
    for i in range(length + 1):
        puppet = []
        for j in range(i):
            puppet.append(0)
        for k in range(i, length):
            puppet.append(1)
        perms = list(itertools.permutations(puppet))
        for permutation in perms:
            if permutation not in inner_list:
                inner_list.append(permutation)

    for element in inner_list:
        values[tuple(element)] = None

    return values


def get_valid_value(combination, variables, phi):
    valid_rows = list(phi[1].keys())

    for var in variables:
        if var not in phi[0]:
            continue
        value = combination[variables.index(var)]
        valid_rows = list(filter(lambda x: x[phi[0].index(var)] == value, valid_rows))

    if len(valid_rows) > 1:
        raise ValueError("More than on rows found as compatible")

    return phi[1][valid_rows[0]]


def compute_value(combination, variables, phi1, phi2):
    return get_valid_value(combination, variables, phi1) * \
           get_valid_value(combination, variables, phi2)


def multiply(phi1, phi2):
    #TODO: INNER JOIN (2 cu 4 da 2)
    new_vars = join_vars(phi1, phi2)
    new_values = generate_empty_values(len(new_vars))

    for combination, value in new_values.items():
        new_values[combination] = compute_value(combination, new_vars, phi1, phi2)

    return Factor(vars=new_vars, values=new_values)


# -------------------------
# --------Sum out----------
# -------------------------
def add_occurrences(phi, new_vars, combination):
    sum = 0
    for values_list, value in phi[1].items():
        is_a_match = True
        for var in new_vars:
            if combination[new_vars.index(var)] != values_list[phi[0].index(var)]:
                is_a_match = False
        if is_a_match:
            sum += value

    return sum


def sum_out(var, phi):
    assert isinstance(phi, Factor) and var in phi.vars

    new_vars = deepcopy(phi[0])
    new_vars.remove(var)
    new_values = generate_empty_values(len(new_vars))

    for combination, value in new_values.items():
        new_values[combination] = add_occurrences(phi, new_vars, combination)

    return Factor(vars=new_vars, values=new_values)


# -------------------------
# -------Prod sum----------
# -------------------------
def multiple_apply(factors, f):
    if len(factors) == 1:
        return factors[0]
    if len(factors) == 0:
        return None

    result_factor = f(factors[0], factors[1])
    for factor in factors[2:]:
        result_factor = f(result_factor, factor)

    return result_factor


def prod_sum(var, Phi, verbose=False):
    assert isinstance(var, str) and all([isinstance(phi, Factor) for phi in Phi])

    factors = list(filter(lambda x: var in x[0], Phi))
    result_factor = sum_out(var, multiple_apply(factors, multiply))

    return list(filter(lambda x: x not in factors, Phi)) + [result_factor]


# -------------------------
# --Variable elimination---
# -------------------------
def variable_elimination(Phi, Z, verbose=False):
    theta = deepcopy(Phi)
    for var in Z:
        theta = prod_sum(var, theta)
    return multiple_apply(theta, multiply)


# -------------------------
# ------Obs reduction------
# -------------------------
def reduce_factor(phi, obs):
    reduced_values = phi.values
    for obs_var, obs_val in obs.items():
        if obs_var not in phi.vars:
            continue
        value_index = phi.vars.index(obs_var)
        reduced_values = {k: v for k, v in reduced_values.items() if k[value_index] == obs_val}

    return Factor(vars=phi.vars, values=reduced_values)


def condition_factors(Phi : list, Z : dict, verbose=False):
    return list(map(
        lambda phi: reduce_factor(phi, Z) if list(set(list(Z.keys())) & set(phi.vars)) else phi,
        Phi
    ))
