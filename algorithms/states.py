def is_absorbing(chain, s, tol=1e-12):
    """
    Returns true if the state can only transition to itself (Absorbing)
    """
    nbrs = chain._trans.get(s, {})
    if not nbrs:
        return True

    if len(nbrs) == 1 and s in nbrs:
        return abs(nbrs[s].get("p", 0) - 1.0) < tol

    return False


def absorbing_states(chain):
    """
    Returns a list of absorbing states
    """
    return {s for s in chain.states if is_absorbing(chain, s)}


def is_transient(chain, s):
    """
    Returns true if the state can transition to other states (Transient)
    """
    return not is_absorbing(chain, s)


def outgoing_mass(chain, s):
    """
    Returns the sum of all probabilities leaving this state (Useful for diagnostics)
    """
    total = 0.0
    for attr in chain._trans.get(s, {}).values():
        p = attr.get("p")
        if isinstance(p, (int, float)):
            total += p
    return total
