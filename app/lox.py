import sys
from scanner import Scanner


class Lox:
    had_error: bool = False

    def __main__(self):
        self.main(sys.argv)

    def _show_banner(self):
        version = "0.0.1"
        banner = f"""
██████╗ ██╗      ██████╗ ██╗  ██╗
██╔══██╗██║     ██╔═══██╗╚██╗██╔╝
██████╔╝██║     ██║   ██║ ╚███╔╝
██╔═══╝ ██║     ██║   ██║ ██╔██╗
██║     ███████╗╚██████╔╝██╔╝ ██╗
╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝
        made by @kazte | {version}
        """

        print(banner)

    def _run(self, source: str):
        pass
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def error(self, line: int, message: str):
        self._report(line, "", message)

    def _report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}")
        self.had_error = True

    def _run_file(self, path: str):
        try:
            with open(path) as file:
                source = file.read()

            if self.had_error:
                sys.exit(65)

            self._run(source)

        except FileNotFoundError:
            print(f"File not found: {path}")
            sys.exit(1)

    def main(self, args: list[str]):
        # self._show_banner()

        if len(args) > 2:
            print("Usage: plox [script]")
            sys.exit(64)
        elif len(args) == 2:
            self._run_file(args[1])
        else:
            # _run_prompt()
            self._show_banner()
            pass


lox = Lox()


def main(args: list[str]):
    lox.main(args)


def error(line: int, message: str):
    lox.error(line, message)
