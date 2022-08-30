import json
from vehicle_detection.core.utility.get_package import generate_and_save_config

if __name__ == "__main__":
    config_path = r"configs\UL.json"
    output_path = r"output\UL_0830.txt"
    generate_and_save_config(config_path, output_path)