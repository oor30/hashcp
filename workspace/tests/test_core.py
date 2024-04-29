import unittest

class HashcpTest(unittest.TestCase):
    def test_hashcp(self):
        from hashcp.core import hashcp
        import glob
        self.assertIsNone(hashcp(glob.glob('*'), 'test_src_dir', 'output', True))