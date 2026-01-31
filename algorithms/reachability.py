def can_step(chain, u, v):
    """
    Returns true if state u can transition to state v
    """
    return chain.has_transition(u, v)


def reachable(chain, source):
    """
    Returns a list of reachable states from state source
    """
    visited = set()
    stack = [source]

    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        stack.extend(chain.successors(u))

    return visited


def communicates(chain, u, v):
    """
    Returns true if state u can transition to state v AND state v can transition to state u.
    """
    return v in reachable(chain, u) and u in reachable(chain, v)


def communication_classes(chain):
    """
    Returns a list of communicating classes of chain
    """
    classes = []
    seen = set()

    for s in chain.states:
        if s in seen:
            continue

        cls = {t for t in chain.states if communicates(chain, s, t)}
        classes.append(cls)
        seen |= cls

    return classes


def is_closed(chain, cls):
    """
    Returns true if state cls is closed (Cannot reach any other state)
    """
    for u in cls:
        for v in chain.successors(u):
            if v not in cls:
                return False
    return True
