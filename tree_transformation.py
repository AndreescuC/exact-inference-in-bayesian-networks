import factor_operators
from copy import deepcopy
from Inference import Inference
from TreeNode import TreeNode


def reduce_factors_obs(node: TreeNode, inference: Inference):
    if node.factor:
        node.factor = factor_operators.reduce_factor(node.factor, inference.observations)
    for kid in node.children:
        reduce_factors_obs(kid, inference)


def project_factor(factor, source_content, dest_content):
    to_be_eliminated = source_content - dest_content
    for var in to_be_eliminated:
        factor = factor_operators.sum_out(var, factor)
    return factor


def update_factor(node, payloads):
    factors = [deepcopy(node.factor)] + payloads if node.factor else payloads

    return factor_operators.multiple_apply(
        factors,
        factor_operators.multiply
    )


def bottom_up_propagation(node: TreeNode, parent_content):
    payloads = []
    for kid in node.children:
        payloads.append(bottom_up_propagation(kid, node.content))

    if payloads:
        node.factor = update_factor(node, payloads)

    if parent_content:
        return project_factor(node.factor, node.content, parent_content)


def compute_final_believes(node, payload):
    pass


def up_to_bottom_propagation(node, payload=None):
    new_payload = compute_final_believes(node, payload) if node.parent else (node.content, node.factor)
    for kid in node.chilren:
        up_to_bottom_propagation(kid, new_payload)
