import json

path = r"C:\Users\Shruti\jk\Python\Python_GUI\Project_series\6.BRD_Agent\dataPush\pattern_dataset.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(len(data))
print(data[0])