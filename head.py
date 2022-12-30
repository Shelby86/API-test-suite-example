import argparse
import sys
import os
import pkg_resources
import pprint


def validate_path(path):
    if path:
        return path.split(os.pathsep)
    else:
        return None


def get_environ() -> dict:
    e = {}
    for i, v in os.environ.items():
        e[i] = v
    return e


def build_info(all):
    d = {
        'general_info': {
            'sys.prefix': sys.prefix,
            'sys.executable': sys.executable,
            '__file__': __file__,
            'sys.version_info': sys.version_info,
        },
        'sys.path': sys.path,
        'pkg_resources.working_set': list(pkg_resources.working_set),
    }

    environ = get_environ() if all else {
        'PATH': validate_path(os.getenv('PATH')),
        'PYTHONPATH': validate_path(os.getenv('PYTHONPATH')),
        'VIRTUAL_ENV': os.environ.get('VIRTUAL_ENV'),
        'CONDA_PREFIX': os.environ.get('CONDA_PREFIX'),
        'PYCHARM_HOSTED': os.environ.get('PYCHARM_HOSTED'),
    }

    d['environ'] = environ

    if sys.version_info < (3, 8):
        return pprint.pformat(d, width=200)
    else:
        return pprint.pformat(d, sort_dicts=False,
                              width=200)  # The sort_dicts parameter appeared in Python 3.8


def main():
    parser = argparse.ArgumentParser(
        description='Prints various diagnostic info about the interpreter',
    )
    parser.add_argument("-a", "--all", action='store_true',
                        help="Print all environment variables")
    args = parser.parse_args()
    info = build_info(args.all)
    print(info)


if __name__ == '__main__':
    main()
    import pyodbc