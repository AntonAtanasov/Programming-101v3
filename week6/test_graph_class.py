import unittest
from graph_module import DirectedGraph


class TestGraphModule(unittest.TestCase):

    def setUp(self):
        self.test_graph = DirectedGraph()

    def test_add_node(self):
        self.test_graph._add_node('test_node')
        self.assertEqual(type(self.test_graph.graph['test_node']), set)

    def test_is_node_in_graph(self):
        self.test_graph._add_node('test_node')
        self.assertTrue(self.test_graph._is_node_in_graph('test_node'))
        self.assertFalse(self.test_graph._is_node_in_graph('WTF'))

    def test_add_edge(self):
        self.test_graph.add_edge('n00dy', 'WaaDaaFaak')
        self.assertTrue(self.test_graph._is_node_in_graph('WaaDaaFaak'))
        self.assertIn('WaaDaaFaak', self.test_graph.graph['n00dy'])
        self.assertNotIn('n00dy', self.test_graph.graph['WaaDaaFaak'])

    def test_get_neighbors_for(self):
        self.test_graph.add_edge('n00dy', 'WaaDaaFaak')
        self.test_graph.add_edge('n00dy', 'Rocky')
        self.test_graph.add_edge('n00dy', 'ZooMaster')
        self.assertEqual(self.test_graph.get_neighbors_for('n00dy'), {'WaaDaaFaak', 'Rocky', 'ZooMaster'})

    def test_path_between(self):
        self.test_graph.add_edge('n00dy', 'WaaDaaFaak')
        self.test_graph.add_edge('WaaDaaFaak', 'Rocky')
        self.test_graph.add_edge('Rocky', 'ZooMaster')
        self.assertTrue(self.test_graph.path_between('n00dy', 'ZooMaster'))
        self.assertFalse(self.test_graph.path_between('WaaDaaFaak', 'n00dy'))
