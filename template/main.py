import jinja2

class MeliaTemplate:
    
    def __init__(self):
        self.environnement = jinja2.Environment()
         
    def test_jinja(self):
        test_template = self.environnement.from_string("Hello, {{name}}")
        test_template.render(name="Hello jinja") 
    