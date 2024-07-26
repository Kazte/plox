import lox
import sys


if __name__ == "__main__":
    python_version = sys.version_info
    if python_version.major < 3:
        print("Python 3 is required to run plox.")
        sys.exit(1)

    lox.main(sys.argv)
