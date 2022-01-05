import argparse

from extractor import Extractor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract audio features')
    parser.add_argument('--config', dest='config_file', help='Config File', default="extractor.yaml",
                        required=True)
    args = parser.parse_args()
    # extractor = Extractor(f"{Path(__file__).parents[1]}/test/test.yaml")
    extractor = Extractor(args.config_file)
    extractor.run()
    print("FINISHED!!")
