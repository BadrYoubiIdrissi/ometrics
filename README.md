# OMetrics (Organised Metrics)

Convenient interface to collect and aggregate code defined metrics during the execution of a program and dumping them to disk.

## Installation

Available for python 3.6 with

```bash
pip install ometrics
```

## Sample usage :

```python
import ometrics
from pprint import pprint

metrics = ometrics.Metrics('file.jsonl')

for i in range(3):
    
    '''
        You can use a dictionary to group all of your metrics 
        inside a loop or function.
    ''' 
    
    metric = {
        'metric_1' : i**2,
        'metric_2' : i**3,
        'metric_group' : {
            'sub_metric' : i**4
        }
    }

    '''
        Or you can use the NestedDict object that facilitates usage 
        of nested dictionaries
    ''' 

    metric_nd = ometrics.NestedDict()

    metric_nd['metric_1'] = i+i**2
    metric_nd['metric_group', 'sub_metric'] = i**4

    metrics.append(metric)
    metrics.append(metric_nd)

pprint(metrics.dict)

metrics.dump()
```

Result 

```
{
    'metric_1': [0, 0, 1, 2, 4, 6],
    'metric_2': [0, 1, 8],
    'metric_group': {
        'sub_metric': [0, 0, 1, 1, 16, 16]
    }
}
```