import json
with open("./queries/token_size.json", "r") as f:
    f = json.load(f)
    avg = 0
    for i in f:
        avg += i
    avg = avg / len(f)
    print(avg)