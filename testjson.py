import json

def main():
    with open("countiesxy.json", "r") as file:
        counties = json.load(file)
    print(counties[0]["name"])

main ()