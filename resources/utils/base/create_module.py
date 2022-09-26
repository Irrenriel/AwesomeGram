import os
from string import punctuation

from resources.utils.base.consts import MODULE_HANDLERS_CONTENT, MODULE_STATES_CONTENT, IMPORT_CONTENT, \
    HANDLERS_PATTERN, MODULES_HANDLERS_CONTENT, MODULE_FUNCTION_CONTENT


class CreateModule:
    def __init__(self, path, name: str, linux_encode: bool, linux_header: str):
        self.path = path
        self.name = name
        self.linux_encode = linux_encode
        self.linux_header = f'{linux_header}\n' if self.linux_encode else ''

        self.modules_path = self.path / "modules"
        self.middlewares_path = self.modules_path / "middlewares"
        self.resources_path = self.path / "resources"

        self.module_path = self.modules_path / self.name
        self.module_functions_path = self.module_path / "functions"
        self.module_handlers_path = self.module_path / "handlers.py"
        self.module_states_path = self.module_path / "states.py"
        self.module_resources_path = self.resources_path / self.name

        self.handlers_path = self.modules_path / "handlers.py"
        self.states_path = self.modules_path / "states.py"
        self.module_function_path = self.module_functions_path / f'{self.name}.py'
        self.module_function_init_path = self.module_functions_path / f'__init__.py'

    def on_process(self):
        """
        Creating step by step folder structure:

        Step 1:
        < ROOT >
            ⊳ modules
            ⊳ resources

        Step 2:
        < ROOT >
            ⊳ modules
                ⊳ < module name > (To overwrite if exists type "y")
            ⊳ resources

        Step 3:
        < ROOT >
            ⊳ modules
                ⊳ < module name >
                    ⊳ functions
                ⊳ middlewares
            ⊳ resources
                ⊳ < module name >

        Step 4:
        < ROOT >
            ⊳ modules
                ⊳ handlers.py (Handlers from all modules are imported here)
                ⊳ states.py (States from all modules are imported here)
                ⊳ < module name >
                    ⊳ functions
                    ⊳ handlers.py
                    ⊳ states.py
                ⊳ middlewares
            ⊳ resources
                ⊳ < module name >

        """
        # Step 1:
        self._make_dirs(self.modules_path, self.resources_path)

        # Step 2:
        selection = self._make_module_dir(self.module_path)

        if not selection:
            return

        # Step 3:
        self._make_dirs(self.module_functions_path, self.module_resources_path, self.middlewares_path)

        # Step 4:
        self._create_module_files()
        self._create_modules_files()

        print(f'Module "{self.name}" was successfully created!')

    @staticmethod
    def _make_dirs(*args):
        for path in args:
            if not os.path.exists(path):
                os.makedirs(path)

    @staticmethod
    def _make_module_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)
            return True

        selection = input('A module with the same name already exists. Overwrite? (y/n)\n>')
        if selection.lower() != 'y':
            return

        return True

    @staticmethod
    def _create_file(path, content: str, mode: str = 'w'):
        with open(path, mode=mode, encoding='UTF-8') as f:
            f.write(content)

    def _create_module_files(self):
        pool = [
            {
                'path': self.module_handlers_path,
                'content': MODULE_HANDLERS_CONTENT.format(header=self.linux_header, name=self.name)
            },
            {
                'path': self.module_states_path,
                'content': MODULE_STATES_CONTENT.format(header=self.linux_header, title=self.name.title())
            },
            {
                'path': self.module_function_init_path,
                'content': IMPORT_CONTENT.format(
                    header=self.linux_header, rows=f'from .{self.name} import {self.name}_func'
                )
            },
            {
                'path': self.module_function_path,
                'content': MODULE_FUNCTION_CONTENT.format(header=self.linux_header, name=self.name)
            }
        ]

        [self._create_file(**kwargs) for kwargs in pool]

    def _create_modules_files(self):
        modules = []

        for i, d in enumerate(os.listdir(self.modules_path)):
            if d == 'middlewares' or d != d.lower() or any([ch in d for ch in punctuation]):
                continue

            modules.append(d)

        pool = [
            {
                'path': self.handlers_path,
                'content': MODULES_HANDLERS_CONTENT.format(
                    header=self.linux_header,
                    rows='\n'.join([f'from {m}.handlers import register_{m}_handlers' for m in modules]),
                    handlers='\n'.join([HANDLERS_PATTERN.format(name=m, upper=m.upper()) for m in modules])
                )
            },
            {
                'path': self.states_path,
                'content': IMPORT_CONTENT.format(
                    header=self.linux_header,
                    rows='\n'.join([f'from {m}.states import {m.title()}States' for m in modules]),
                )
            }
        ]

        [self._create_file(**kwargs) for kwargs in pool]
