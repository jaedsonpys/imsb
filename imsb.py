from files.handler_files import HandlerFile
from devices.handler_devices import HandlerDevice

from exceptions.exceptions import DeviceDiretoryNotFindError
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
    def __generate_id() -> str:
        caracters = ascii_letters + digits
        id_backup = ''.join([choice(caracters) for __ in range(16)])

        return id_backup

    def backup(self, path: str) -> None:
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

    def recovery(self, backup_id: str, recovery_local: str = None) -> bool:
        """Recupera o backup com o
        ID especificado.

        Você pode obter o ID pelo
        nome do arquivo no diretório
        backups.

        :param backup_id: ID do backup
        :param recovery_local: Caminho para onde
        o backup recuperado irá. Exemplo:
        "/media/username/device_name"

        :return:
        """

        # Como funciona o recovery:
        #
        # Primeiramente, obtemos os dados em JSON
        # do arquivo de backup apartir do ID e
        # guardamamos em uma variável denominada
        # de "backup".
        #
        # No primeiro loop for, obtemos o nome
        # do diretório e o conteúdo dele. Logo
        # em seguida, criamos este diretório
        # na pasta HOME do usuário. Se o diretório
        # já existir, um erro é disparado.
        #
        # No segundo loop, iteramos sob o conteúdo
        # do diretório obtido no primeiro loop, assim
        # conseguimos obter o nome e o base64 do arquivo
        # que está dentro desse diretório. Após isso,
        # convertemos o base64 para o conteúdo original
        # do arquivo e salvamos.

        recovery_path = self.home

        if recovery_local:
            devices = HandlerDevice.check_devices()

            if recovery_local not in devices:
                raise DeviceDiretoryNotFindError

            recovery_path = recovery_local

        backup = HandlerFile.get_backup_content(backup_id)
        if not backup:
            return False

        for dir, content in backup.items():
            path = f'{recovery_path}/{dir}'

            try:
                os.mkdir(path)
            except FileExistsError:
                raise FileExistsError(f'Já existe um diretório: {path}.')

            for name, base in content.items():
                path_file = f'{path}/{name}'

                with open(path_file, 'wb') as file:
                    content_file = HandlerFile.base64_to_string(base.encode())
                    file.write(content_file)


IMSB().recovery('Y5nEs03vbApzDFkR', recovery_local='/media/jaedson/JSDN21')
