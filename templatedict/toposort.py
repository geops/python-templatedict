
class TopologicalSortError(Exception):
    message = ""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "{0}({1})".format(self.__class__.__name__, self.message)

def topological_sort(source):
    """perform topo sort on elements.

    :arg source: list of ``(name, set(names of dependencies))`` pairs
    :returns: list of names, with dependencies listed first

    http://stackoverflow.com/questions/11557241/python-sorting-a-dependency-list
    """
    pending = [(name, set(deps)) for name, deps in source]
    emitted = []
    while pending:
        next_pending = []
        next_emitted = []
        for entry in pending:
            name, deps = entry
            if name in deps:
                raise TopologicalSortError("cyclic dependency detected: {0} depends on itself".format(name))
            deps.difference_update(set((name,)), emitted) # <-- pop self from dep, req Py2.6
            if deps:
                next_pending.append(entry)
            else:
                yield name
                emitted.append(name) # <-- not required, but preserves original order
                next_emitted.append(name)
        if not next_emitted:
            raise TopologicalSortError("cyclic dependency detected: %s %r" % (name, (next_pending,)))
        pending = next_pending
        emitted = next_emitted


