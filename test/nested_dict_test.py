import unittest
from ometrics import NestedDict

class TestNestedDict(unittest.TestCase):

    def setUp(self):
        self.d = {'accuracy': 0.8, 'loss': 10, 'int': {'correct': 50, 'incorrect': 10}}
        self.nd = NestedDict(self.d)

    def test_init(self):
        self.assertEqual(self.d, self.nd.dict)
        self.assertEqual(self.d, NestedDict(self.nd).dict)

    def test_contains(self):
        self.assertTrue('accuracy' in self.nd)
        self.assertTrue(('int', 'correct') in self.nd)
        self.assertFalse('accura' in self.nd)
        self.assertFalse(('inte', 'correct') in self.nd)

    def test_get(self):
        self.nd['accuracy']
        self.nd['int', 'correct']
        self.assertRaises(KeyError, lambda : self.nd['hello'])
        self.assertRaises(KeyError, lambda : self.nd['hello', 'world'])

    def test_set(self):
        new_value = 5
        self.nd['accuracy'] = new_value
        self.nd['int', 'correct'] = new_value
        self.assertEqual(self.nd['accuracy'], new_value)
        self.assertEqual(self.nd['int', 'correct'], new_value)

    def test_iter(self):
        count = 0
        for keys, value in self.nd:
            self.assertTrue(isinstance(keys, tuple))
            count += 1
        self.assertEqual(len(self.nd), 4)
        self.assertEqual(count, 4)

    
if __name__ == '__main__':
    unittest.main()
