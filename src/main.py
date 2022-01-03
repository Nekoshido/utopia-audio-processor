import argparse

from extractor import Extractor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract audio features')
    parser.add_argument('--config', dest='config_file', help='Config File', default="extractor.yaml",
                        required=True)
    args = parser.parse_args()
    extractor = Extractor()
    extractor.run(args.config_file)
    print("FINISHED!!")
