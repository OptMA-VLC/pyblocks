from typing import Any, Type, Dict, Optional

from rich.console import Console

from src.pyblock_sim.repository.cli.object_printer import ObjectPrinter
from src.pyblock_sim.repository.cli.print_level import PrintLevel


class CLI:
    _obj_printers: Dict[Type, ObjectPrinter]
    _rich_console: Console

    def __init__(self, force_color_support: bool = True):
        self._obj_printers = {}
        self._level = PrintLevel.INFO
        self._rich_console = Console()

        if force_color_support:
            if self._rich_console.color_system is None:
                print("[Warning] Console doesn't support color. Will try overriding.")
                self._rich_console = Console(color_system="256", width=120)

    def print(self, *args, level=PrintLevel.INFO, **kwargs):
        if level is None:
            tag = ''
        else:
            tag = PrintLevel.get_tag(level)

        args_list = list(args)
        for i in range(0, len(args_list)):
            printer = self._get_printer_for(args_list[i])
            if printer is None:
                if isinstance(args_list[i], str):
                    args_list[i] = self._add_tag_before_every_line(args_list[i], tag)
            else:
                printed_obj = printer.print(args_list[i])
                args_list[i] = self._add_tag_before_every_line(printed_obj, tag)

        args = tuple(args_list)
        self._rich_console.print(*args, **kwargs)

    def register_obj_printer(self, printer: ObjectPrinter):
        if printer.get_type() == str:
            raise ValueError('Adding an ObjectPrinter for type str is unsupported!')

        self._obj_printers[printer.get_type()] = printer

    def _get_printer_for(self, obj: Any) -> Optional[ObjectPrinter]:
        if isinstance(obj, str):
            return None

        for t, printer in self._obj_printers.items():
            if isinstance(obj, t):
                return printer

        return None

    def _add_tag_before_every_line(self, input_str: str, tag: str) -> str:
        if not isinstance(input_str, str):
            raise TypeError(f"Expected input_str to be a string but it is {type(input_str)}")

        lines = input_str.split('\n')
        result = ''

        num_lines = len(lines)
        for i in range(0, num_lines):
            result += tag + lines[i]
            if i < num_lines - 1:
                result += '\n'

        return result
