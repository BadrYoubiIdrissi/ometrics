import warnings
import collections
import copy

def _update(d, u):
        for k, v in u.items():
            dv = d.get(k, {})
            if not isinstance(dv, collections.Mapping):
                d[k] = v
            elif isinstance(v, collections.Mapping):
                d[k] = _update(dv, v)
            else:
                d[k] = v
        return d
class Metrics:
    """NestedDictionary utility class. Implements the bulk of functionality for ometrics
    
    Raises:
        ValueError: [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], Metrics):
            self.dict = args[0].dict
        elif args and isinstance(args[0], dict):
            self.dict = args[0]
        else:
            self.dict = dict(*args, **kwargs)

    def __contains__(self, keys):
        try:
            self.__getitem__(keys)
        except (IndexError, KeyError):
            return False
        return True

    def __getitem__(self, keys):
        # Allows getting top-level branch when a single key was provided
        keys = self._validate_keys(keys)

        branch = self.dict
        for key in keys:
            branch = branch[key]

        # If we return a branch, and not a leaf value, we wrap it into a NestedDict
        return Metrics(branch) if isinstance(branch, dict) else branch

    def __setitem__(self, keys, value):
        # Allows setting top-level item when a single key was provided
        keys = self._validate_keys(keys)

        branch = self.dict
        for key in keys[:-1]:
            if not key in branch:
                branch[key] = {}
            elif not isinstance(branch[key], dict):
                warnings.warn('Overriding existing value with group')
                branch[key] = {}
            branch = branch[key]

        if isinstance(value, Metrics):
            value = value.dict
        elif isinstance(value, dict):
            nd = Metrics()
            for key, v in value.items():
                nd[key] = v
            value = nd.dict

        branch[keys[-1]] = value

    def __iter__(self):
        yield from self.dict.__iter__()
    
    def __len__(self):
        return self._dict_len(self.dict)
    
    def __repr__(self):
        return f'Metrics({self.dict.__repr__()})'
        
    def flatten(self):
        yield from self._dict_generator(self.dict)

    @staticmethod
    def _validate_keys(keys):
        if isinstance(keys, str):
            return tuple(keys.split('/'))
        elif isinstance(keys, tuple):
            k = tuple()
            for key in keys:
                k += tuple(key.split('/'))
            return k
        else:
            raise ValueError(f"key {keys} is neither string nor tuple")
    
    @staticmethod
    def _dict_generator(indict, keys=None):
        keys = keys[:] if keys else ()
        if isinstance(indict, dict):
            for key, value in indict.items():
                if isinstance(value, dict): yield from Metrics._dict_generator(value, keys + (key,))
                else: yield keys + (key,), value
        else:
            yield indict

    @staticmethod
    def _dict_len(indict, count=0):
        if isinstance(indict, dict):
            count = 0
            for _, value in indict.items():
                if isinstance(value, dict): count+=Metrics._dict_len(value, count)
                else: count += 1
            return count
        else:
            return count + 1

    def get(self, key, default=None):
        return self[key] if key in self else default

    def keys(self):
        return self.dict.keys()

    def values(self):
        childs = []
        for d in self.dict.values():
            if isinstance(d, dict):
                childs.append(Metrics(d))
            else:
                childs.append(d)
        return childs
        
    def items(self):
        childs = []
        for k, d in self.dict.items():
            if isinstance(d, dict):
                childs.append((k,Metrics(d)))
            else:
                childs.append((k,d))
        return childs

    def update(self, d):
        if isinstance(d, dict):
            self.dict = _update(self.dict, d)
        elif isinstance(d, Metrics):
            self.dict = _update(self.dict, d.dict)
        else:
            raise ValueError("Can't update with non dict like object")

    def get_existent_root(self, keys):
        keys = self._validate_keys(keys)
        if not keys in self:
            return None
        for i in range(1,len(keys)+1):
            if keys[:i] in self:
                return keys[:i]

    def copy(self):
        return Metrics(copy.deepcopy(self.dict))

    def append(self, src):
        for keys, value in Metrics(src).flatten():
            if keys in self:
                self[keys].append(value)
            else:
                self[keys] = [value]

    def apply_keys(self,function):
        for keys, value in self.flatten():
            self[keys] = function(keys, value)

    def apply(self, function):
        for keys, value in self.flatten():
            self[keys] = function(value)

    def apply_if(self, condition_func, function):
        for keys, value in self.flatten():
            if condition_func(keys, value):
                self[keys] = function(value)

    def reset(self):
        del self.dict
        self.dict = dict()

if __name__ == "__main__":
    Metrics({'a/b':{'c/d':{'e/f' : 1}}})