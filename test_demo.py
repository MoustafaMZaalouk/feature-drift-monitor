import unittest
import tempfile
import json
from pathlib import Path
from demo import run

class ExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.output=Path(cls.temp.name)/'results.json'
        cls.r=run(cls.output)
    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()
    def test_output_matches_returned_result(self):
        self.assertEqual(json.loads(self.output.read_text()),self.r)
    def test_identical_psi(self):
        from demo import psi,fit_bins
        import numpy as np
        x=np.arange(100.)
        self.assertAlmostEqual(psi(x,x,fit_bins(x)),0.)
    def test_shift_detected_descriptively(self):
        self.assertGreater(self.r['features']['mean_shift']['psi'],self.r['features']['stable']['psi'])
    def test_extreme_values_included(self):
        from demo import fit_bins
        import numpy as np
        self.assertEqual(np.histogram([-1e9,1e9],bins=fit_bins(np.arange(100.)))[0].sum(),2)

if __name__ == "__main__":
    unittest.main()
