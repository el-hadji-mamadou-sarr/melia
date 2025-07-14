from __future__ import annotations
from jinja2 import FileSystemLoader, Environment
import os
import json

STARTER_OUTPUT = "output/fastapi_starter"
STARTER_INPUT = "fastapi_starter"
STARTER_TREE = "templates/fastapi_starter/tree.json"

class TreeFile:
    def __init__(self, name:str):
        self.name = name
        
class Tree:
    def __init__(self, folder_name:str, sub:list[Tree], files:list[TreeFile]):
        self.folder_name = folder_name
        self.sub = sub
        self.files = files
   
class MeliaTemplate:
    
    def __init__(self):
        self.environnement = Environment(loader=FileSystemLoader("templates/"))
    
    def make_fastapi_starter(self):
        os.makedirs(f"{STARTER_OUTPUT}/app/core", exist_ok=True)
        os.makedirs(f"{STARTER_OUTPUT}/app/api", exist_ok=True)
        
        template = self.environnement.get_template(f'{STARTER_INPUT}/app/main.py')
        rendered = template.render(test="Test")
        
        with open("{STARTER_OUTPUT}/app/main.py", "w") as f:
            f.write(rendered)
    
    def make_starter_from_tree(self):
        with open(STARTER_TREE, "r") as f:
            result = f.read()
            data = json.loads(result)
            tree = Tree(**data)

        print(tree.folder_name)