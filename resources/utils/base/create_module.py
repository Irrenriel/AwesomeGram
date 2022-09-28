import os
from string import punctuation
from sys import argv

from jinja2 import Environment, FileSystemLoader

from config import config
from resources.utils.base.exceptions import ModuleNameNotFound, InvalidModuleName


class CreateModule:
    def __init__(self, path):
        index = argv.index('--create-module') + 1
        if index >= len(argv):
            raise ModuleNameNotFound

        self.name = argv[index].lower()

        if any([ch in self.name for ch in punctuation]):
            raise InvalidModuleName('Invalid module name. Punctuation marks are not allowed.')

        if len(self.name) > 64:
            raise InvalidModuleName('Invalid module name. The maximum number of characters is 64.')

        self.path = path
        self.linux_mode = config.LINUX_MODE
        self.linux_header = f'{config.LINUX_HEADER}\n' if self.linux_mode else ''

        self.template_path = self.path / "resources" / "utils" / "base" / "templates" / "create_module_templates"
        self.template_module_name = 'module_name'

        self.modules_path = self.path / "modules"

    def on_process(self):
        """
        Creating step by step structure:

        < ROOT >
            ⊳ modules
                ⊳ handlers.py (Handlers from all modules are imported here)
                ⊳ states.py (States from all modules are imported here)
                ⊳ < module name >
                    ⊳ functions
                        ⊳ __init__.py
                        ⊳ < module name >.py
                    ⊳ handlers.py
                    ⊳ states.py
                ⊳ middlewares
            ⊳ resources
                ⊳ < module name >

        """
        self.creating_level(self.template_path, self.path)

    def creating_level(self, tpl_path, src_path):
        for ent in os.listdir(tpl_path):
            if not ent.endswith('-tpl'):
                continue

            clean = ent.replace('-tpl', '')

            if clean.startswith(self.template_module_name):
                clean = clean.replace(self.template_module_name, self.name)

            # Python files:
            if clean.endswith('.py'):
                tpl = Environment(loader=FileSystemLoader(tpl_path)).get_template(ent)

                with open(src_path / clean, mode='w', encoding='UTF-8') as f:
                    f.write(tpl.render(**self.data))

            # Other files (useless now):
            if '.' in ent:
                continue

            # Folders:
            else:
                if not os.path.exists(src_path / clean):
                    os.makedirs(src_path / clean)

                self.creating_level(tpl_path / ent, src_path / clean)

    @property
    def data(self):
        return {
            'header': self.linux_header,
            'name': self.name,
            'modules': [i for i in os.listdir(self.modules_path) if '.' not in i and i != 'middlewares']
        }
