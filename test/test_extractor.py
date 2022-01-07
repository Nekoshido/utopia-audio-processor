from pathlib import Path

from numpy import testing

from src.extractor import Extractor
from unittest import TestCase

import test.test_constants as test_constants


class ExtractorTest(TestCase):
    extractor_mel = Extractor(Path(__file__).parent.parent / "test" / "test_mel.yaml")
    extractor_mfccs = Extractor(Path(__file__).parent.parent / "test" / "test_mfccs.yaml")

    def test_feature_extractor_mel(self):
        real_mel = self.extractor_mel.feature_extractor(test_constants.AUDIO_ARRAY_1, 5)
        testing.assert_array_almost_equal(test_constants.AUDIO_MEL, real_mel)

    def test_feature_extractor_mfccs(self):
        real_mfccs = self.extractor_mfccs.feature_extractor(test_constants.AUDIO_ARRAY_1, 2)
        testing.assert_array_almost_equal(test_constants.AUDIO_MFCCS, real_mfccs)

    def test_normalization_minmax(self):
        real_minmax = self.extractor_mel.normalization(test_constants.AUDIO_MEL)
        testing.assert_array_almost_equal(test_constants.AUDIO_MINMAX_NORM, real_minmax)

    def test_normalization_standard(self):
        real_standard = self.extractor_mfccs.normalization(test_constants.AUDIO_MFCCS)
        testing.assert_array_almost_equal(test_constants.AUDIO_STANDARD_NORM, real_standard)
