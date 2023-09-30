import daemonize

class AlarmBox:
    def __init__(self):
        _read_settings()
        self.settings = {}

    def _read_settings(self, file_name):
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('=')
                    if len(parts) == 2:
                        name, value = parts
                        name = name.strip()
                        value = value.strip()
                        self.settings[name] = value


def my_daemon_function():
    while True:
        with open('/tmp/daemon_example.txt', 'a') as f:
            f.write('Daemon is running...\n')

if __name__ == '__main__':
    # Define the options for daemonization
    daemon = daemonize.Daemonize(
        app="my_daemon",
        pid='/tmp/my_daemon.pid',
        action=my_daemon_function,
        foreground=False,
    )

    # Start the daemon
    daemon.start())
