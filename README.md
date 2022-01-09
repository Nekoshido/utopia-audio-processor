# Utopia Audio Processor
## _Summary Report_
Please write a 1 to 2 page summary of notes including the following:

- Comment your choice of algorithms, libraries and implementation design / code organization
- Describe your choice of database for feature storage that you would envision
- Mention any obstacles, difficulties or further suggestions you had/have regarding this task

### Library
Librosa library is the most popular across the Python community and the most adopted for its audio treatment. It has almost 5000 stars in their repository in [Github](https://github.com/librosa/librosa) and couple of releases every year. The library seems alive and bullet proof to use for production purposes.

### Algorithms
One of the chosen algorithms is the `Mel Spectrogram` algorithm. An algorithm that applies Mel Scale into a Spectrogram, that algorithm is capable of adjusting the frequencies of an audio spectrogram to a perceptual scale of pitches that are in equal n distance from one another judged by human listeners.

The other chosen algorithm is `MFCCs` (Mel-frequency cepstral coefficients) what extracts a small set of features that describes the overall shape of spectral sound. Those coefficients collectively make up an mel-frequency cepstrum which is a representation of the short-term power spectrum of a sound. In n the MFC, the frequency bands are equally spaced on the mel scale (mentioned above). This frequency warping can allow for better representation of sound.

Both features are important methods to extract features from an audio signal and they are used in the treatment of audio signals.

### Audio Extraction Features

I've decided to extract the features for the entire audio file. From an algorithm perspective, Mel Spectrogram uses Fast Fourier Transformation, which already handles the audio processing by reading it by a window. MFCCs also extracts sets of the main audio sample.
From a memory perspective, librosa loads all the audio first and later you can split it into segments. All the audio data is already loaded in memory, so it doesn't affect if it's by segments or for the entire audio file.
For lacking time in that assignment, I wanted to choose the simpler way to load the audio, but for the given reasons, in my opinion, it's also the best approach.
As an improvement, in the future, both ways can be handled in the code.

### Implementation Design

The code is split into src and test.
In src there is an Extractor class with all the methods used for the extractor and the main, the file in charge of reading the inputs and calling the extractor.
To initialize the extractor is only necessary to pass a path to the yaml file and it will handle the configuration. To make it run, its only necessary to call the method run and it will read and store from the paths given in the yaml file as the requirement mentioned.
As an improvement, there are general methods included in that class that can be moved into a utils file for more general purposes.

In the test folder, there are two samples of the yamls files, a file called `test_constants` with the expected results and the main file for testing the extractor called `test_extractor` that includes methods to test all the features and normalization added. As an improvement, it can be added some unit testing to check if the yaml is read correctly and if it's reading and storing the files in the correct places.

As an addition, outside these two folders, there is a general file `requirements.txt` in python to install the libraries and a file `setup.py` to handle the installation of that code as a library.

### To a Database or Datalake
Here we don’t ask you for the implementation.

Instead, please describe what type of database, or data lake, you would use to store these features, how you would store the data and what design and architecture considerations you have to make this database/data lake scalable.
If you have experience with cloud platforms (AWS, GCP) please mention considerations that you may have regarding available cloud technologies.

Include this in the Summary Report we mention below.

Before commiting to any solution, I would like to understand in what kind of context that data is going to be used. For example, is not the same the purpose of that data is to run Machine Learning features that just querying over the data. However, I would try to make some assumptions in order to where this data can be used.

My first approach would be to store the `raw` data into files. For raw data I don't want to mean only the audio files themselves, I want to mean audio file data with all the basic feature extraction and normalizations. As I said, I don't have the context in which of this features is going to be used, but we can imagine a file with columns as a `file_name`, `mel_spectogram`, `mfccs`, `normalization`, `standards`, `timestamp` and so on. Depending on how this data is going to be used in most of the cases it will make sense to store it into a columnar based file format or a row based file format. This mean, if we just want to extract certain columns for each row, a columnar format is the best choice, and the best choice for a columnar file format is `parquet` file, if we can add a `delta` format on the top of this would be perfect. `Delta` format is a parquet file with a extra layer of metadata that allows time-travelling and atomic transactions.
On the other hand, if the data is going to be used by rows as an entire piece, the recomended file format would be `avro` format, an optimzed format of files for that purpose.
Raw binaries files are more difficult to query since you don't have any knowledge of time, ids and other information.

After the Ingestion layer, and depending on how many feature extraction, audio categorization and other transformations of the data needs to be done. I would like to suggest a Cloud Distributed Database system.
In my experience, AWS Athena doesn't work fast enough to be a good Cloud Distributed Database.
On the paper, Big Query or Snowflake have better arquitecture to distribute the data over their clusters what make them faster in order to handle queries. Both accept structure and semi-structured data, which can be useful for our use case. Both options could be better than AWS Redshift, but that one released a new architecture and it will be necessary to do a POC to consider which one performs better and to estimate the cost of it as well.
I would like to mention as well the Firebolt solution, they are a smaller company than the other ones, but they claim to be faster and cheaper than the competitors. It can be an interesting product to be considered and added to the POC.

### Obstacles

The main obstacles were the area of audio treatment since is not an area that I'm familiar with. I've had to learn a basic introduction in order to be able to do a good assignment.
Other obstacles were the time since there are a lot of requests to handle in a short time.

### How to Run

For running the application is only necessary to create a yaml with all the configuration and to pass it in the command line.

```
 python3 src/main.py --config path_to_yaml.yaml
 ```

Is also possible to install the code as a library by running

```
pip install .
```
