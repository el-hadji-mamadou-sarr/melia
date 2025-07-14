from jinja2 import FileSystemLoader, Environment
class MeliaTemplate:
    
    def __init__(self):
        self.environnement = Environment(loader=FileSystemLoader("templates/"))
         
    def test_jinja(self):
        test_template = self.environnement.from_string("Hello, {{name}}")
        test_template.render(name="Hello jinja") 
    