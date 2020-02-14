#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import logging
import pathlib

PROJECT = pathlib.Path(__file__).absolute().parent.parent
LIBRARY = PROJECT / 'jamf'
SCRIPT = PROJECT / 'scripts/patch.py'
DESTINATION = pathlib.Path('/Library/Python/3.6/site-packages')

def install(src, directory):
    logger = logging.getLogger(__name__)
    if not src.exists():
        raise SystemExit(f"no such file: {src}")
    if not directory.exists():
        logger.debug(f"creating: {directory}")
        directory.mkdir(mode=0o755, parents=True, exist_ok=True)
    dst = directory / src.name
    if dst.exists() and dst.is_dir():
        logger.debug(f"shutil.rmtree({dst})")
        shutil.rmtree(dst)
    logger.info(f"installing: {src} -> {dst}")
    if src.is_dir():
        logger.debug(f"shutil.copytree({src}, {dst})")
        shutil.copytree(src, dst)
    elif src.is_file():
        logger.debug(f"shutil.copyfile({src}, {dst})")
        shutil.copyfile(src, dst)
        dst.chmod(src.stat().st_mode)


def check_python_path_env(destination):
    logger = logging.getLogger(__name__)
    # doesn't seem to work if run as root (root appears to drop the env)
    pythonpath = os.environ.get('PYTHONPATH', '')
    paths = [pathlib.Path(x) for x in pythonpath.split(':')]
    logger.debug(f"pythonpaths: {paths}")
    if not paths:
        msg = f"export PYTHONPATH={str(destination)}"
    elif destination not in paths:
        msg = f"export PYTHONPATH=$PYTHONPATH:{str(destination)}"
    print(f"add the following to your profile:\n{msg}", file=sys.stderr)


def main():
    logger = logging.getLogger(__name__)
    logger.debug(f"PROJECT: {PROJECT}")
    install(LIBRARY, DESTINATION)
    install(SCRIPT, pathlib.Path('/usr/local/bin'))
    check_python_path_env(DESTINATION)


if __name__ == '__main__':
    fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.INFO, format=fmt)
    if os.getuid() == 0:
        main()
    else:
        raise SystemExit("run me as root")
