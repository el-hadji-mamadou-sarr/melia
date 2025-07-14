from jinja2 import FileSystemLoader, Environment
import os

STARTER_OUTPUT = "output/fastapi_starter"
STARTER_INPUT = "fastapi_starter"

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
    