import os

import librosa
import glob
from yaml import safe_load, YAMLError
from pathlib import Path

from numpy import ndarray, save

from sklearn.preprocessing import MinMaxScaler, StandardScaler


class Extractor:

    def __init__(self, config_file_path: str):
        config_dict = self._yaml_reader(config_file_path)
        self.load_folder = config_dict['load_folder']
        self.save_folder = config_dict['save_folder']
        self.feature_type = config_dict['feature']
        self.normalization_type = config_dict['normalization']

    @staticmethod
    def _yaml_reader(path: str):
        with open(path, "r") as stream:
            try:
                return safe_load(stream)
            except YAMLError as exc:
                print(exc)

    @staticmethod
    def store_data(norm_array: ndarray, file_path: str, file_name: str):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        path_destination = file_path + r'\\' + file_name
        return save(path_destination, norm_array)

    def feature_extractor(self, audio_array: ndarray, sampling_rate: int) -> ndarray:
        if self.feature_type['name'] == 'mfcc':
            return librosa.feature.mfcc(y=audio_array, sr=sampling_rate,
                                        S=self.feature_type.get('feature.spectrogram', None),
                                        n_mfcc=self.feature_type.get('feature.n_mfcc', 20),
                                        dct_type=self.feature_type.get('feature.dct_type', 2),
                                        norm=self.feature_type.get('feature.norm', 'ortho'),
                                        lifter=self.feature_type.get('feature.lifter', 0))
        elif self.feature_type['name'] == 'melspectrogram':
            return librosa.feature.melspectrogram(y=audio_array, sr=sampling_rate,
                                                  S=self.feature_type.get('feature.spectrogram', None),
                                                  n_fft=self.feature_type.get('feature.n_fft', 2048),
                                                  hop_length=self.feature_type.get('feature.hop_length', 512),
                                                  win_length=self.feature_type.get('feature.win_length', None),
                                                  window=self.feature_type.get('feature.window', 'hann'),
                                                  center=self.feature_type.get('feature.center', True),
                                                  pad_mode=self.feature_type.get('feature.pad_mode', 'reflect'),
                                                  power=self.feature_type.get('feature.power', 2.0))

    def normalization(self, dataset: ndarray) -> ndarray:
        if self.normalization_type['name'] == 'minmaxnormalizer':
            return MinMaxScaler().fit_transform(dataset)
        elif self.normalization_type['name'] == 'standardcaler':
            return StandardScaler().fit_transform(dataset)

    def run(self):
        audio_path = f'{Path(__file__).parents[1]}\data'
        for filename in glob.iglob(audio_path + '**/**', recursive=True):
            if filename.endswith('.wav'):
                file_path = os.path.split(filename)
                audio_file_name = file_path[1].replace('wav', 'npy')
                audio_folders = r'\\'.join(file_path[0].split("\\")[-2:])
                path_destination = self.save_folder + audio_folders
                y, sr = librosa.load(filename)
                feature_extractor = self.feature_extractor(y, sr)
                normalization = self.normalization(feature_extractor)
                self.store_data(normalization, path_destination, audio_file_name)

