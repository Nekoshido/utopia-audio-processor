from pathlib import Path

from src.extractor import Extractor

extractor = Extractor(f"{Path(__file__).parents[1]}/test/test.yaml")
print(extractor.feature_type)
print(extractor.normalization_type)
