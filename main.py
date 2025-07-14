from cli.main import CLILayer
from engine.main import MeliaTemplate

if __name__ == "__main__":
    #CLILayer.init_melia() 
    melia_template = MeliaTemplate()
    melia_template.make_fastapi_starter()