from scarnd import ScarNetworkDatasets
import unittest


class TestUtil(unittest.TestCase):

    def setUp(self):
        self.ond = ScarNetworkDatasets()

    # def test_github_has_issue_doi(self):
    #     self.assertTrue(self.ond.github_has_issue(["10.15468/jth3pz", "12d42f40-cb7b-4249-8b0d-bba4c3d48e45"]))
