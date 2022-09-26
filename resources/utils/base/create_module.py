import logging
import os

from resources.utils.base.consts import MODULE_HANDLER_CONTENT


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
        self.module_resources_path = self.resources_path / self.name

        self.handlers_path = self.modules_path / "handlers.py"

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
                    ⊳ handlers
                ⊳ middlewares
            ⊳ resources
                ⊳ < module name >

        Step 4:
        < ROOT >
            ⊳ modules
                ⊳ handlers.py
                ⊳ < module name >
                    ⊳ functions
                    ⊳ handlers.py

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
        self._create_file(
            self.module_handlers_path, MODULE_HANDLER_CONTENT.format(name=self.name, header=self.linux_header)
        )

        # logging.info(f'Module "{self.name}" was successfully created!')
        print(f'Module "{self.name}" was successfully created!')

    @staticmethod
    def _make_dirs(*args):
        for path in args:
            if not os.path.exists(path):
                os.makedirs(path)

    @staticmethod
    def _make_module_dir(path):
        if os.path.exists(path):
            selection = input('A module with the same name already exists. Overwrite? (y/n)\n>')
            if selection.lower() != 'y':
                return

        else:
            os.makedirs(path)

        return True

    @staticmethod
    def _create_file(path, content: str):
        with open(path, mode='w', encoding='UTF-8') as f:
            f.write(content)
