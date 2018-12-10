import factor_operators


def reduce_factors_obs(node, inferences):
    # for inference in inferences:
    #     if node.content in inference[]
    # observations = {inference[1] for inference in inferences}
    # factor = factor_operators.reduce_factor(node.factor, inferences)
    # for kid in node.chilren:
    #     reduce_factors_obs(kid)


def update_factor(node, payload):
    pass


def bottom_up_propagation(node):
    payloads = []
    for kid in node.chilren:
        payloads.append(bottom_up_propagation(kid))
    return update_factor(node, payloads) if payloads else (node.content, node.factor)


def compute_final_believes(node, payload):
    pass


def up_to_bottom_propagation(node, payload=None):
    new_payload = compute_final_believes(node, payload) if node.parent else (node.content, node.factor)
    for kid in node.chilren:
        up_to_bottom_propagation(kid, new_payload)
