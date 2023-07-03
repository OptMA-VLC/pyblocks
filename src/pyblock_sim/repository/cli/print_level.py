from enum import Enum


class PrintLevel(Enum):
    VERBOSE = 'verbose'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'

    @staticmethod
    def get_tag(level: 'PrintLevel') -> str:
        if level == PrintLevel.VERBOSE:
            return r'[white]\[Verbose][/white] '
        elif level == PrintLevel.INFO:
            return r'[blue]\[Info][/blue] '
        elif level == PrintLevel.WARNING:
            return r'[yellow]\[Warn][/yellow] '
        elif level == PrintLevel.ERROR:
            return r'[red]\[Error][/red] '

        return r'[white]\[??????][/white] '
