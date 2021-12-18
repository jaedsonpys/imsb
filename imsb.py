from files.handler_files import HandlerFile
from devices.handler_devices import HandlerDevice
from exceptions.exceptions import NotIsADiretoryError

from string import ascii_letters, digits
from random import choice
import os


class IMSB:
    def __init__(self):
        self.pwd = os.getcwd()
        self.home = os.getenv('HOME')

        self.backup_id = None
        self.finished = False
        self.finished_diretories = 0

    @staticmethod
    def __generate_id():
        caracters = ascii_letters + digits
        id_backup = ''.join([choice(caracters) for __ in range(16)])

        return id_backup

    def backup(self, path: str):
        """Realiza o backup do último
        diretório do caminho.

        O método backup() pode ser utilizado
        em threads. Use o atributo IMSB.finished
        para consultar o estado do backup.

        Também é possível ver quantos diretórios
        já foram percorridos em
        IMSB.finished_diretories.

        :param path: Caminho do diretório
        :return: None
        """

        # Esse é o método que realiza o backup
        # de todos os arquivos do diretório.
        #
        # O método backup() pode ser utilizado
        # com threads, pois os arquivos JSON
        # de backup são identificados por um
        # ID único e aleatório, fazendo com
        # que os arquivos possam ser manipulados
        # individualmente.
        #
        # Em questão de otimização, um buffer
        # de arquivos em base64 é guardado,
        # e após todos os arquivos do diretório
        # serem percorridos, o buffer é adicionado
        # ao arquivo JSON e salvo, pronto para
        # o próximo diretório.

        self.backup_id = self.__generate_id()

        if not os.path.isdir(path):
            raise NotIsADiretoryError

        basename, index = HandlerFile.get_basename(path)

        for root, dirs, files in os.walk(path):
            self.finished_diretories += 1
            diretory = '/'.join(root.split('/')[index:])
            map_dir = {}

            if files:
                for file in files:
                    src_file = f'{root}/{file}'

                    with open(src_file, 'rb') as file_read:
                        base64_file = HandlerFile.file_to_base64(file_read)
                        map_dir[file] = base64_file

            HandlerFile.save_json_data(self.backup_id, diretory, map_dir)

        self.finished = True


if __name__ == '__main__':
    from threading import Thread
    from time import sleep

    backup_1 = IMSB()
    path_1 = '/home/jaedson/Documentos/PythonDIO'

    backup_2 = IMSB()
    path_2 = '/home/jaedson/Documentos/reconhecimentoImagens'

    Thread(target=backup_1.backup, args=[path_1]).start()
    Thread(target=backup_2.backup, args=[path_2]).start()

    while True:
        print(f'Backup 1: {backup_1.finished_diretories}, '
              f'Backup 2: {backup_2.finished_diretories}\r', end='')

        if backup_1.finished and backup_2.finished:
            print('Finalizado')
            break

        sleep(2)
