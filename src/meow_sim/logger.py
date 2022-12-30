from typing import Tuple, Any

from rich.console import Console


class _Logger:
    _console: Console

    def __init__(self):
        self._console = Console()
        if self._console.color_system is None:
            print("[Warning] Console doesn't support color. Will try overriding.")
            self._console = Console(color_system="256", width=120)

    def info(self, *args, **kwargs):
        self._print_with_tag(r'[blue]\[Info][/blue]', args, kwargs)

    def warn(self, *args, **kwargs):
        self._print_with_tag(r'[yellow]\[Warn][/yellow]', args, kwargs)

    def error(self, *args, **kwargs):
        self._print_with_tag(r'[red]\[Error][/red]', args, kwargs)

    def verbose(self, *args, **kwargs):
        self._print_with_tag(r'[white]\[Verbose][/white]', args, kwargs)

    def _print_with_tag(self, tag: str, args, kwargs):
        args_list = list(args)

        no_tag = False
        if 'no_tag' in kwargs and bool(kwargs['no_tag']):
            no_tag = True
            del kwargs['no_tag']

        has_string_arg = len(args_list) > 0 and isinstance(args_list[0], str)
        if has_string_arg and no_tag is False:
            args_list[0] = f'{tag} {args_list[0]}'

        self._console.print(*tuple(args_list), **kwargs)


logger = _Logger()
