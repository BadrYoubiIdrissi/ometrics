import unittest
from ometrics import Metrics

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.deep_nest = {
            'accuracy': 0.8,
            'loss': 10,
            'int': {
                'correct': 50,
                'incorrect': {
                    'world': 10
                }
            }
        }
        self.metr_deep = Metrics(self.deep_nest)
        self.append_metr = Metrics()
        self.dictio_1 = {
            'accuracy': 0.8,
            'loss': 8,
            'int': {
                'correct': 4,
                'incorrect': 10
            }
        }
        self.dictio_2 = {'kl_div': 0.8, 'loss': 10, 'int': {'correct': 50}}

    def test_init(self):
        self.assertEqual(self.deep_nest, self.metr_deep.dict)
        self.assertEqual(self.deep_nest, Metrics(self.metr_deep).dict)

    def test_contains(self):
        self.assertTrue('accuracy' in self.metr_deep)
        self.assertTrue(('int', 'correct') in self.metr_deep)
        self.assertTrue('int/correct' in self.metr_deep)
        self.assertFalse('accura' in self.metr_deep)
        self.assertFalse('inte/correct' in self.metr_deep)

    def test_get(self):
        self.assertEqual(self.metr_deep['accuracy'], 0.8)
        self.assertEqual(self.metr_deep['int', 'correct'], 50)
        self.assertEqual(self.metr_deep['int/correct'], 50)
        self.assertEqual(self.metr_deep['int/incorrect', 'world'], 10)
        self.assertRaises(KeyError, lambda: self.metr_deep['hello'])
        self.assertRaises(KeyError, lambda: self.metr_deep['hello', 'world'])

    def test_set(self):
        new_value = 5
        self.metr_deep['accuracy'] = new_value
        self.metr_deep['int', 'correct'] = new_value
        self.metr_deep['int/new'] = new_value
        self.assertEqual(self.metr_deep['accuracy'], new_value)
        self.assertEqual(self.metr_deep['int', 'correct'], new_value)
        self.assertEqual(self.metr_deep['int/new'], new_value)

        self.metr_deep['loss'] = {'int/vadv': 10, 'tag/vadv': 10}

        self.assertEqual(self.metr_deep['loss'].dict, {
            'int': {
                'vadv': 10
            },
            'tag': {
                'vadv': 10
            }
        })

    def test_iter(self):
        count = 0
        for keys, value in self.metr_deep.flatten():
            self.assertTrue(isinstance(keys, tuple))
            count += 1
        self.assertEqual(len(self.metr_deep), 4)
        self.assertEqual(count, 4)

        for key, value in self.metr_deep.items():
            self.assertTrue(key in self.metr_deep.dict)
            self.assertTrue(not isinstance(value, dict))

    def test_append(self):
        self.append_metr.append(self.dictio_1)
        self.assertEqual(
            self.append_metr.dict, {
                'accuracy': [0.8],
                'loss': [8],
                'int': {
                    'correct': [4],
                    'incorrect': [10]
                }
            })
        self.append_metr.append(self.dictio_2)
        self.assertEqual(
            self.append_metr.dict, {
                'accuracy': [0.8],
                'kl_div': [0.8],
                'loss': [8, 10],
                'int': {
                    'correct': [4, 50],
                    'incorrect': [10]
                }
            })


if __name__ == '__main__':
    unittest.main()
