# -*- coding: utf-8 -*-

from pathlib import Path


PROJECT_PATH = Path(__file__).parent

DATA_FOLDER = PROJECT_PATH.joinpath(".data")
DIFFS_FOLDER = DATA_FOLDER.joinpath("diffs")
