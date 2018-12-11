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
        payload = bottom_up_propagation(kid, node.content)
        node.children_messages[kid.content] = payload
        payloads.append(payload)

    if payloads:
        node.factor = update_factor(node, payloads)

    if parent_content:
        return project_factor(node.factor, node.content, parent_content)


def divide(messages, kid_content, factor):
    assert kid_content in messages
    return factor_operators.divide(factor, messages[kid_content])


def up_to_bottom_propagation(node: TreeNode, payload=None):
    new_payload = factor_operators.multiply(node.factor, payload) if node.parent else node.factor
    node.final_believe = new_payload
    for kid in node.children:
        designed_factor = divide(node.children_messages, kid.content, new_payload)
        projected_factor = project_factor(designed_factor, node.content, kid.content)
        up_to_bottom_propagation(kid, projected_factor)
