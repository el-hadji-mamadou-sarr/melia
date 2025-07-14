from __future__ import annotations
from jinja2 import FileSystemLoader, Environment
import os
import json

OUTPUT = "output"
STARTER_TREE = "templates/fastapi_starter/tree.json"

class TreeFile:
    def __init__(self, name:str):
        self.name = name
        
class Tree:
    def __init__(self, folder_name:str, sub:list['Tree'], files:list[TreeFile]):
        self.folder_name = folder_name
        self.sub = sub
        self.files = files
    
    @classmethod
    def from_dict(cls, data:dict) ->'Tree':
        return cls(
            folder_name=data['folder_name'],
            sub=[cls.from_dict(item) for item in data['sub']],
            files=[TreeFile(**item) for item in data["files"]]
        )
   
class MeliaTemplate:
    
    def __init__(self):
        self.environnement = Environment(loader=FileSystemLoader("templates/"))
    
    
    def make_files(self, tree:Tree, base=None):
        if base:
            base = f"{base}/{tree.folder_name}"
        else:
            base = tree.folder_name
        
        os.makedirs(f"{OUTPUT}/{base}", exist_ok=True)
        
         # create the files
        for file in tree.files:
            path = f"{base}/{file.name}"
            template = self.environnement.get_template(path)
            rendered = template.render()
            
            with open(f"{OUTPUT}/{path}", "w") as f:
                f.write(rendered)
        
        # create sub
        for sub in tree.sub:
            self.make_files(sub, base)
    
    def make_starter_from_tree(self):
        with open(STARTER_TREE, "r") as f:
            result = f.read()
            data = json.loads(result)
            tree = Tree.from_dict(data)

        self.make_files(tree)
        
            
        