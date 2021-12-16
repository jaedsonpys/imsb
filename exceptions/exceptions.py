class Base(Exception):
    pass


class NotIsADiretoryError(Base):
    def __init__(self):
        super().__init__('O caminho especificado não é um diretório.')


if __name__ == '__main__':
    raise NotIsADiretoryError
