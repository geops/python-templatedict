import string

from templatedict.toposort import topological_sort, TopologicalSortError

class StringTemplate(string.Template):

    def variables(self):
        """return a set of all variables used in the string"""
        variables = set()
        for mo in self.pattern.finditer(self.template):
            var = mo.group('named') or mo.group('braced')
            if var:
                variables.add(var)
        return variables

class TemplateDict(dict):
    """
    A string dictionary which allows its keys being replaced in its values.

    performs a topological ordering to substitute values

    example:

    td = TemplateDict()
    td['server_name'] = 's1 ${arch} $arch'
    td['instance'] = "${server_name}_instance"
    td['arch'] = "64"
    print td.substitute()
    """

    def substitute(self, extra_values={}):
        """returns a simple dictiionary with all values
        substituded

        extra_values is a dictionary of optional values which will be used
        for substitution, but will not be part of the returned dict
        """
        substituted = {}

        mappings = extra_values
        mappings.update(self)

        # collect all key, variable pairs
        pairs = []
        for k, v in mappings.iteritems():
            if type(v) not in (str, unicode):
                raise ValueError("Unsupported type {0} for key {1}".format(type(v).__name__, k))
            pairs.append((k, StringTemplate(v).variables()))

        # replace
        source = mappings
        for k in topological_sort(pairs):
            try:
                value = StringTemplate(mappings[k]).substitute(source)
            except ValueError, e:
                raise ValueError("Could not substitute variables in: {0}: {1}".format(mappings[k], e.message))
            substituted[k] = value
            source[k] = value

        # only return the substituted values present in self (ignore keys only present in extra_values)
        return dict([(item, substituted[item]) for item in substituted.keys() if self.has_key(item)])
