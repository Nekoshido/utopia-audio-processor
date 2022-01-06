from numpy import array, ndarray

from src.extractor import Extractor
from unittest import TestCase


class ExtractorTest(TestCase):
    extractor = Extractor("test.yaml")

    @staticmethod
    def _sample_numpy() -> ndarray:
        return array([1, 2, 3, 4, 5])

    def _extractor_result_template(self):

    def test_feature_extractor(self):
        audio_array = self._sample_numpy()
        real = self.extractor.feature_extractor(audio_array, 5)
        # assert real == expected


extractor = Extractor("test.yaml")
audio_array = array([1.0, 2.0, 3.0])
real = extractor.feature_extractor(audio_array, 2)
print(real)
