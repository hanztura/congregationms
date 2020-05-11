import json, os

current_path = os.path.dirname(os.path.abspath(__file__)) 
filename = 'data/philippines/refregion.json'
filename = os.path.join(current_path, filename)
with open(filename) as f:
    data = json.load(f)

print(data)