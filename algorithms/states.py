def is_absorbing(chain, s, tol=1e-12) -> bool:
    """
    Returns true if the state can only transition to itself (Absorbing)
    :param chain: Chain of states
    :param s: State to check
    :param tol: Optional tolerance for absorbing states
    :return: True if the state can only transition to itself (Absorbing)
    """
    nbrs = chain._trans.get(s, {})
    if not nbrs:
        return True

    if len(nbrs) == 1 and s in nbrs:
        return abs(nbrs[s].get("p", 0) - 1.0) < tol

    return False


def absorbing_states(chain) -> set:
    """
    Returns a set of absorbing states
    :param chain: Chain of states
    :return: Set of absorbing states
    """
    return {s for s in chain.states if is_absorbing(chain, s)}


def is_transient(chain, s) -> bool:
    """
    Returns true if the state can transition to other states (Transient)
    :param chain: Chain of states
    :param s: State to check
    :return: True if the state can transition to other states (Transient)
    """
    return not is_absorbing(chain, s)


def outgoing_mass(chain, s) -> float:
    """
    Returns the sum of all probabilities leaving this state (Useful for diagnostics)
    :param chain: Chain of states
    :param s: State to check
    :return: Sum of all probabilities leaving this state.
    """
    total = 0.0
    for attr in chain._trans.get(s, {}).values():
        p = attr.get("p")
        if isinstance(p, (int, float)):
            total += p
    return total
