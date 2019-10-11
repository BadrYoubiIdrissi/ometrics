import ometrics
import unittest
import json
import os

def dict_equality(d1,d2):
    return json.dumps(d1) == json.dumps(d2)

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.m = ometrics.Metrics(os.path.abspath('test/fixtures/test.jsonl'))
        self.d1 = {'accuracy': 0.8, 'loss': 8, 'int': {'correct': 4, 'incorrect': 10}}
        self.d2 = {'kl_div': 0.8, 'loss': 10, 'int': {'correct': 50}}
        self.nd = ometrics.NestedDict(self.d1)
    
    def test_append(self):
        self.m.append(self.d1)
        self.assertTrue(
            dict_equality(
                self.m.dict,
                {'accuracy': [0.8], 'loss': [8], 'int': {'correct': [4], 'incorrect': [10]}}
            )
        )
        self.m.append(self.d2)
        self.assertEqual(
                self.m.dict,
                {'accuracy': [0.8], 'kl_div': [0.8], 'loss': [8,10], 'int': {'correct': [4,50], 'incorrect': [10]}}
            )
    
    def test_dump(self):
        if os.path.exists(self.m.filepath) : os.remove(self.m.filepath)
        self.m.reset()
        self.m.append(self.d1)
        self.m.dump()
        with open(self.m.filepath,'r') as fh:
            l = fh.readline()
            self.assertEqual(json.dumps({'accuracy': [0.8], 'loss': [8], 'int': {'correct': [4], 'incorrect': [10]}}), l.rstrip())
            self.assertEqual(self.m.dict, {})
    
    def test_load(self):
        if os.path.exists(self.m.filepath) : os.remove(self.m.filepath)
        self.m.reset()
        self.m.append(self.d1)
        self.m.dump()
        self.m.load_last()
        self.assertEqual(self.m.dict, {'accuracy': [0.8], 'loss': [8], 'int': {'correct': [4], 'incorrect': [10]}})

if __name__ == '__main__':
    unittest.main()