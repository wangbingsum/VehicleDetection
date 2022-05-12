import json

def load_cfg(path):
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg

def main():
    cfg_path = "configs/config.json"
    cfg = load_cfg(cfg_path)
    print(cfg["vehicle_config"])

if __name__ == "__main__":
    main()