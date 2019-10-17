# OMetrics (Organised Metrics)

Lightweight library that implements a Metrics object to neatly and flexibly organise all your metrics and information needed to calculate them.

The simple idea behind ometrics is to simplify the aggregation of metrics throughout a program. It is made to avoid the following very verbose situations :

```python
metric_1_list = []
metric_2_list = []
metric_3_list = []
metric_4_list = []

for step in iterator:
    # Some code
    metric_1 = value_1(step)
    metric_2 = value_2(step)
    metric_3 = value_3(step)
    metric_4 = value_4(step)

    # Some other code
    metric_1_list.append(metric_1)
    metric_2_list.append(metric_2)
    metric_3_list.append(metric_3)
    metric_4_list.append(metric_4)

metric_1_list = process_1(metric_1_list)
metric_2_list = process_1(metric_2_list)
metric_3_list = process_2(metric_3_list)
metric_4_list = process_2(metric_4_list)

```

Instead you can now organise your metrics in the deeply nested dictionary Metrics with a pleasant interface !

```python
import ometrics

metrics = ometrics.Metrics()

for step in iterator:
    metric = ometrics.Metrics()
    # Some code
    metric['group1/1'] = value_1(step)
    metric['group1/2'] = value_2(step)
    metric['group2/3'] = value_3(step)
    metric['group2/4'] = value_4(step)

    metrics.append(metric)

metrics['group1'].apply(process1)
metrics['group2'].apply(process2)

```

On top of being way shorter and more readable with less variables that cluter your program, you can now automate calculations by choosing to regroup information that can be processed or displayed in a similar fashion. 

You can also dump your metrics to disk and retrieve them later to view your data differently without having to execute your code.  

Metrics objects can be nested with multiple levels! For example :

```python
m_1 = ometrics.Metrics()
for step1 in iterator1:
    m_2 = ometrics.Metrics()
    for step2 in itereator2:
        m_3 = ometrics.Metrics()
        for step3 in iterator3:
            m_4 = ometrics.Metrics()
            m_4['metric_1'] = some_value
            #Other code
            m_3.append(m4)
        m_2.append(m_3)
    m_1.append(m_2)
```

You can end up structuring your metrics in matrices instead of just lists in this fashion. It is then easier to use numpy or other libraries to process this information.

With organised and serializable metrics, you can more easily seperate your code from metric calculation for more readability and flexibity.

## Who is it for?

You'll find ometrics to be especially useful if you have a lot of metrics in your program!

## Installation

Available for python>=3.6 with

```bash
pip install ometrics
```

## Contribution

Feel free to file an issue or create a pull request :) 