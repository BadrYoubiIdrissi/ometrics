import json
from ometrics import Metrics

def dump(metrics, filepath):
    with open(filepath, 'a+') as fh:
        fh.write(json.dumps(metrics.dict)+'\n')
    metrics.reset()

def load_all(filepath):
    m = Metrics()
    with open(filepath, 'r') as fh:
        for l in fh:
            d = json.loads(l)
            m.append(d)
    return m

def load_last(filepath):
    m = Metrics()
    with open(filepath, 'r') as fh:
        m.dict = json.loads(fh.readlines()[-1])
