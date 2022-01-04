import librosa
import glob
from yaml import safe_load, YAMLError
from pathlib import Path

import numpy

from sklearn.preprocessing import MinMaxScaler, StandardScaler


class Extractor:

    def __init__(self, config_file_path: str):
        config_dict = self._yaml_reader(config_file_path)
        self.feature_type = config_dict['feature']
        self.normalization_type = config_dict['normalization']

    @staticmethod
    def _yaml_reader(path: str):
        with open(path, "r") as stream:
            try:
                return safe_load(stream)
            except YAMLError as exc:
                print(exc)

    def feature_extractor(self, audio_array: numpy.ndarray, sampling_rate: int) -> numpy.ndarray:
        if self.feature_type['name'] == 'mfcc':
            return librosa.feature.mfcc(y=audio_array, sr=sampling_rate,
                                        S=self.feature_type.get('spectrogram', None),
                                        n_mfcc=self.feature_type.get('n_mfcc', 20),
                                        dct_type=self.feature_type.get('dct_type', 2),
                                        norm=self.feature_type.get('norm', 'ortho'),
                                        lifter=self.feature_type.get('lifter', 0))
        elif self.feature_type['name'] == 'melspectrogram':
            return librosa.feature.melspectrogram(y=audio_array, sr=sampling_rate,
                                                  S=self.feature_type.get('spectrogram', None),
                                                  n_fft=self.feature_type.get('n_fft', 2048),
                                                  hop_length=self.feature_type.get('hop_length', 512),
                                                  win_length=self.feature_type.get('win_length', None),
                                                  window=self.feature_type.get('window', 'hann'),
                                                  center=self.feature_type.get('center', True),
                                                  pad_mode=self.feature_type.get('pad_mode', 'reflect'),
                                                  power=self.feature_type.get('power', 2.0))

    def normalization(self, dataset: numpy.ndarray) -> numpy.ndarray:
        if self.normalization_type['name'] == 'MinMax':
            return MinMaxScaler().fit_transform(dataset)
        elif self.normalization_type['name'] == 'Standard':
            return StandardScaler().fit_transform(dataset)

    def run(self):
        audio_path = f'{Path(__file__).parents[1]}\data'
        print(self.normalization_type)
        print(self.feature_type)
        for filename in glob.iglob(audio_path + '**/**', recursive=True):
            if filename.endswith('.wav'):
                y, sr = librosa.load(filename)

