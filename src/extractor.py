import librosa
import glob
import yaml
from pathlib import Path

import numpy

from typing import Optional, Any
from sklearn.preprocessing import MinMaxScaler, StandardScaler


class Extractor:

    def __init__(self, config_file_path: str):
        config_dict = self._yaml_reader(config_file_path)
        self.feature_type = config_dict['feature']
        self.normalization_type = config_dict['normalization']

    @staticmethod
    def _yaml_reader(path: str):
        return yaml.load(path)

    def feature_extractor(self, audio_array: numpy.ndarray, sampling_rate: int,
                          spectrogram: Optional[Any], n_mfcc: Optional[Any], dct_type: Optional[Any],
                          norm: Optional[Any], lifter: Optional[Any], n_fft: Optional[Any],
                          hop_length: Optional[Any], win_length: Optional[Any],
                          window: Optional[Any], center: Optional[bool], pad_mode: Optional[str],
                          power: Optional[Any]) -> numpy.ndarray:
        if self.feature_type == 'mfcc':
            return librosa.feature.mfcc(y=audio_array, sr=sampling_rate, S=spectrogram, n_mfcc=n_mfcc,
                                        dct_type=dct_type, norm=norm, lifter=lifter)
        elif self.feature_type == 'melspectrogram':
            return librosa.feature.melspectrogram(y=audio_array, sr=sampling_rate, n_fft=n_fft,
                                                  hop_length=hop_length, win_length=win_length,
                                                  window=window, center=center, pad_mode=pad_mode,
                                                  power=power)

    def normalization(self, dataset: numpy.ndarray) -> numpy.ndarray:
        if self.normalization_type == 'MinMax':
            return MinMaxScaler().fit_transform(dataset)
        elif self.normalization_type == 'Standard':
            return StandardScaler().fit_transform(dataset)

    def run(self, config_file_path: str):
        audio_path = f'{Path(__file__).parents[1]}\data'
        extractor = Extractor(config_file_path)
        for filename in glob.iglob(audio_path + '**/**', recursive=True):
            if filename.endswith('.wav'):
                y, sr = librosa.load(filename)
