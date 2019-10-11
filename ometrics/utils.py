from six.moves import reduce

def _dict_generator(indict, keys=None):
    keys = keys[:] if keys else ()
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict): yield from _dict_generator(value, (key,) + keys)
            else: yield keys + (key,), value
    else:
        yield indict

def _dict_len(indict, count=0):
    if isinstance(indict, dict):
        count = 0
        for _, value in indict.items():
            if isinstance(value, dict): count+=_dict_len(value, count)
            else: count += 1
        return count
    else:
        return count + 1
"""
Returns:
    NestedDict -- Nested dict utility class for easier access with key tuples

Thanks to Olivier Melançon from stackoverflow for class base
"""
class NestedDict:
    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], NestedDict):
            self.dict = args[0].dict
        else:
            self.dict = dict(*args, **kwargs)

    def __contains__(self, keys):
        try:
            self.__getitem__(keys)
        except KeyError:
            return False
        return True

    def __getitem__(self, keys):
        # Allows getting top-level branch when a single key was provided
        if not isinstance(keys, tuple):
            keys = (keys,)

        branch = self.dict
        for key in keys:
            branch = branch[key]

        # If we return a branch, and not a leaf value, we wrap it into a NestedDict
        return NestedDict(branch) if isinstance(branch, dict) else branch

    def __setitem__(self, keys, value):
        # Allows setting top-level item when a single key was provided
        if not isinstance(keys, tuple):
            keys = (keys,)

        branch = self.dict
        for key in keys[:-1]:
            if not key in branch:
                branch[key] = {}
            branch = branch[key]
        branch[keys[-1]] = value

    def __iter__(self):
        yield from _dict_generator(self.dict)
    
    def __len__(self):
        return _dict_len(self.dict)
    
    def __repr__(self):
        return f'NestedDict({self.dict.__repr__()})'

    def __dict__(self):
        return self.dict