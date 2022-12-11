from typing import Tuple, Any

from rich.console import Console


class _Logger:
    _console: Console

    def __init__(self):
        self._console = Console()
        if self._console.color_system is None:
            print("[Warning] Console doesn't support color. Will try overriding.")
            self._console = Console(color_system="256")

    def info(self, *args, **kwargs):
        self._console.print(*self._inject_tag(args, r'[blue]\[Info][/blue]'), **kwargs)

    def warn(self, *args, **kwargs):
        self._console.print(*self._inject_tag(args, r'[yellow]\[Warn][/yellow]'), **kwargs)

    def _inject_tag(self, args: Tuple[Any], tag: str) -> Tuple[Any]:
        if len(args) == 0:
            return args

        args_list = list(args)
        if isinstance(args[0], str):
            args_list[0] = f'{tag} {args[0]}'
        else:
            args_list.insert(0, tag)

        return tuple(args_list)



logger = _Logger()
