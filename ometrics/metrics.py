import json
from ometrics import utils
from ometrics import aggregate

class Metrics(utils.NestedDict):
    def __init__(self, filepath, aggregation_functions=None):
        super().__init__()
        self.filepath = filepath
        self.agg_functions = aggregation_functions

    def append(self, src):
        for keys, value in utils.NestedDict(src):
            if keys in self:
                self[keys].append(value)
            else:
                self[keys] = [value]
    
    # TODO : test aggregation functions

    def _get_agg_function(self, keys):
        def get_first_func(keys, d):
            if callable(d):
                return d
            elif isinstance(d, dict) and keys[0] in d:
                get_first_func(keys[1:], d[keys[0]])
            else:
                return aggregate.default
        return get_first_func(keys, self.agg_functions)

    def aggregate(self):
        for keys, value in self:
            self[keys] = self._get_agg_function(keys)(value)
    
    def reset(self):
        del self.dict
        self.dict = dict()

    def dump(self):
        with open(self.filepath, 'a+') as fh:
            fh.write(json.dumps(self.dict)+'\n')
        self.reset()
    
    def load_all(self):
        with open(self.filepath, 'r') as fh:
            for l in fh:
                d = json.loads(l)
                self.append(d)

    def load_last(self):
        with open(self.filepath, 'r') as fh:
            self.dict = json.loads(fh.readlines()[-1])
    
    def __repr__(self):
        return f'Metrics({self.dict.__repr__()})'

__all__= ['Metrics']