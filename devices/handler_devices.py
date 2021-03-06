import os

SYSTEM = os.uname().sysname

# configuração para Linux
if SYSTEM == 'Linux':
    USERNAME = os.getenv('USER')
    LINUX_PATH_DEVICES = [f'/media/{USERNAME}']


class HandlerDevice:
    @staticmethod
    def check_devices() -> [list, bool]:
        """Procura por dispositivos
        USB ou discos que estão conectados."""

        def check_mount(a) -> [str, bool]:
            if os.path.ismount(a):
                return a

            return False

        connected_devices = []

        for d in LINUX_PATH_DEVICES:
            complete_path = lambda a: f'{d}/{a}'

            # retorna apenas o caminho
            # de dispositivos que estejam
            # montados.
            list_media = map(complete_path, os.listdir(d))

            connected_devices.extend(map(check_mount, list_media))

        return connected_devices


if __name__ == '__main__':
    connected = HandlerDevice.check_devices()
