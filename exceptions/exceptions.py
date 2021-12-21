class Base(Exception):
    pass


class NotIsADiretoryError(Base):
    def __init__(self):
        super().__init__('O caminho especificado não é um diretório.')


class DeviceDiretoryNotFindError(Base):
    def __init__(self):
        super().__init__('O diretório do dispositivo não'
                         'foi encontrado.')

