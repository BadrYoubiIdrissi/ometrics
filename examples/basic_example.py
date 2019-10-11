import ometrics
from pprint import pprint

metrics = ometrics.Metrics('path/to/file.jsonl')

for i in range(100):
    
    '''
        You can use a dictionary to group all of your metrics 
        inside a loop or function.
    ''' 
    
    metric = {
        'metric_1' : i**2,
        'metric_1' : i**3,
        'metric_group' : {
            'sub_metric' : i**4
        }
    }

    '''
        Or you can use the NestedDict object that facilitates usage 
        of nested dictionaries
    ''' 

    metric_nd = ometrics.NestedDict()

    metric_nd['metric1'] = i+i**2
    metric_nd['metric_group', 'sub_metric'] = i**4

    metrics.append(metric_nd)
    metrics.append(metric_nd)
    pprint(metrics.dict)