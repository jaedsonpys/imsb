from typing import TextIO, BinaryIO
from base64 import b64decode, b64encode
import os
import json


class HandlerFile:
    @staticmethod
    def file_to_base64(file: [TextIO, BinaryIO]):
        """Retorna o conteudo de um arquivo
        em base64."""

        file_content = file.read()
        file.close()

        file_content_base = b64encode(file_content)

        return file_content_base.decode()

    @staticmethod
    def base64_to_string(base64: bytes):
        """Retorna o conteúdo do base64 em
        ascii."""

        base64_decode = b64decode(base64)
        return base64_decode.decode()

    @staticmethod
    def get_basename(path: str):
        """Retorna o nome e index do
        último diretório do caminho"""

        split_path = path.split('/')

        basename = split_path[-1]
        index = len(split_path) - 1

        return basename, index

    @staticmethod
    def save_json_data(backup_id: str, path_key: str, content: dict):
        path_backups = f'./backups'
        path_json = f'{path_backups}/{backup_id}.json'

        def check_json():
            if os.path.isfile(path_json):
                return True

            return False

        if not check_json():
            data = {}
            data[path_key] = content

            with open(path_json, 'w') as file_backup:
                json.dump(data, file_backup, indent=4, ensure_ascii=False)

            return True

        with open(path_json, 'r') as file_backup_read:
            json_content = json.load(file_backup_read)

        with open(path_json, 'w') as file_backup_write:
            json_content[path_key] = content
            json.dump(json_content, file_backup_write, indent=4, ensure_ascii=False)

        return True


if __name__ == '__main__':
    base_file = HandlerFile.file_to_base64(open('handler_files.py'))
    print(base_file)

    string_file = HandlerFile.base64_to_string(base_file.encode())
    print(string_file)

    basename, index = HandlerFile.get_basename('/home/jaedson/Documentos/PythonDIO')
    print(basename, index)

    data = {'app.py': 'ehuasajbsjbajs'}
    result = HandlerFile.save_json_data('9034hds', '/root', data)

    print(result)
    print('\033[1;32mFinished Test\033[m')
