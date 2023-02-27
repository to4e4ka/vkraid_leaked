import json


def get_json_param(param):
    with open('data.json', encoding='utf8') as jsonConfig:
        json_parameters = json.load(jsonConfig)
        return json_parameters[param]
