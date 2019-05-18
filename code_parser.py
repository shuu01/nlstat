import os
import ast

from typing import Generator, Any, List, Tuple

class BaseParser(object):

    extensions: Tuple[str] = ('',)

    def __init__(self, path: str, files_limit: int):

        self.path = path
        self.files_limit = files_limit

    def get_filenames(self) -> Generator[str, None, None]:

        count: int = 0

        for dirname, dirs, files in os.walk(self.path, topdown=True):
            for file in files:
                if file.endswith(self.extensions):
                    count += 1
                    yield os.path.join(dirname, file)
                if count == self.files_limit:
                    print(f'total {count} files')
                    return None

        print(f'total {count} files')
        return None

class PythonParser(BaseParser):

    extensions = (
        '.py',
    )

    def __init__(self, path: str, files_limit: int):

        super().__init__(path, files_limit)

    @staticmethod
    def is_magic(name: str) -> bool:

        if name.startswith('__') and name.endswith('__'):
            return True
        return False

    def get_trees(self,
        with_filenames: bool=False,
        with_file_content: bool=False,
    ) -> Generator[Any, None, None]:

        for filename in self.get_filenames():

            with open(filename, 'r', encoding='utf-8') as attempt_handler:
                main_file_content = attempt_handler.read()

            try:
                tree = ast.parse(main_file_content)
            except SyntaxError as e:
                print(filename, e)
                tree = ast.Module(None)

            if with_filenames:
                if with_file_content:
                    yield (filename, main_file_content, tree)
                else:
                    yield (filename, tree)
            else:
                yield tree

    def get_nodes(self, node_type):
        for tree in self.get_trees():
            for node in ast.walk(tree):
                if isinstance(node, node_type):
                    yield node

    def get_variable_names(self):
        for node in self.get_nodes(ast.Name):
            yield node.id

    def get_function_names(self):
        for node in self.get_nodes(ast.FunctionDef):
            name = node.name.lower()
            if not self.is_magic(name):
                yield name

    def get_class_names(self):
        for node in self.get_nodes(ast.ClassDef):
            yield node.name


def get_parser(lang):

    return parsers.get(lang)


parsers = {
    'python': PythonParser,
}
