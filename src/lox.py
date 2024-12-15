import argparse
import sys
from lox.scanner import Scanner, Token
from dataclasses import dataclass


@dataclass
class Lox():
    had_error: bool = False

    def run(self, source: str) -> None:
        scanner: Scanner = Scanner(source)
        tokens: list[Token] = scanner.scan_tokens()

        for token in tokens:
            print(token)


    def error(self, line: int, message: str) -> None:
        self.report(line, "", message)


    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}", file=sys.stderr)
        self.had_error = True


    def run_file(self, path: str) -> None:
        with open(path, "r") as file:
            self.run(file.read())
        
        if self.had_error:
            sys.exit(65)


    def run_prompt(self) -> None:
        while True:
            print("> ", end="")
            try:
                self.run(input())
                self.had_error = False
            except EOFError:
                print("Exiting...")
                break


lox = Lox()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hello from crafting-interpreters!")
    args = parser.parse_args()
    lox = Lox()
    if args.length > 1:
        raise ValueError("Usage: jlox [script]")

    elif args.length == 1:
        lox.run_file(args[0])
    else:
        lox.run_prompt()
