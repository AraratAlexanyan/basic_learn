import requests
import json
import yaml
import os

json_url = 'https://raw.githubusercontent.com/AraratAlexanyan/App/master/twoarrayjson.json'

request = requests.get(json_url)
response = request.json()

''' **** Json - Text **** '''

try:
    os.mkdir("network")
except FileExistsError:
    pass

with open('network/re-json-text.txt', 'w') as j_t:
    json.dump(response, j_t, indent=4)


''' **** Json - Yaml **** '''

with open('network/req-json-yaml.yml', 'w') as j_y:
    yaml.dump(response, j_y)


''' **** Yaml - Json **** '''
request = None
response = None

yaml_url = 'https://raw.githubusercontent.com/AraratAlexanyan/App/master/simple_yaml.yml'

request = requests.get(yaml_url)
response = request.text
with open('network/req-yaml-json.json', 'w') as y_j:
    json.dump(yaml.safe_load(response), y_j, indent=4)


''' **** Yaml - Text **** '''

with open('network/req-yaml-text.txt', 'w') as y_t:
    yaml.dump(yaml.safe_load(response), y_t)


print('Second variant load data from local files')

''' **** Json - Text **** '''

path_json = 'data/test_json.json'
path_yaml = 'data/test_yaml.yml'

try:
    os.mkdir("local")
except FileExistsError:
    pass

with open(path_json) as load_json:
    with open('local/loc-json-text.txt', 'w') as json_text:
        for f in load_json:
            json_text.write(f)


''' **** Json - Yaml **** '''

with open(path_json) as load_json:
    data_json = json.load(load_json)
    with open('local/loc-json-yaml.yml', 'w') as json_yaml:
        yaml.dump(data_json, json_yaml)

''' **** Yaml - Json **** '''

with open(path_yaml) as load_yaml:
    data_yaml = yaml.safe_load(load_yaml)
    with open('local/loc-yaml-json.json', 'w') as yaml_json:
        json.dump(data_yaml, yaml_json, indent=4)

''' **** Yaml - Text **** '''

with open(path_yaml) as load_yaml:
    with open('local/loc-yaml-text.txt', 'w') as yaml_text:
        for f in load_yaml:
            yaml_text.write(f)
