import json

with open('cell_no.json') as cell:
    cell = json.load(cell)
print(type(cell))