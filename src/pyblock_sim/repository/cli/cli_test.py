from typing import Any, Type

from src.pyblock_sim.repository.cli.cli import CLI
from src.pyblock_sim.repository.cli.object_printer import ObjectPrinter


class TestCLI:
    def test_prints(self, capfd):
        cli = CLI(force_color_support=False)

        cli.print('Hello World!')

        out, _ = capfd.readouterr()
        assert 'Hello World!' in out

    def test_object_printer(self, capfd):
        class Foo:
            pass

        class FooPrinter(ObjectPrinter):
            def get_type(self) -> Type:
                return Foo

            def print(self, obj: Any) -> str:
                return 'foo'

        cli = CLI(force_color_support=False)
        cli.register_obj_printer(FooPrinter())

        cli.print(Foo())

        out, _ = capfd.readouterr()
        assert 'foo' in out
