import yaml

def parse_yaml_to_dic(path):
    with open(path) as yaml_file:
        try:
            dict_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
            return dict_yaml
        except Exception:
            return None