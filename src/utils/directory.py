# type: ignore
import os
from pathlib import Path, _posix_flavour, _windows_flavour


class DotPath(Path):
    """To enable adding Paths as nested attributes of other Paths, which is not possible with
    standard pathlib Path. Replicating _flavour setting from Path source code gets around an
    issue with inheriting from Path.
    """

    # why this? because of Path's __new__ method,
    # see https://codereview.stackexchange.com/questions/162426/subclassing-pathlib-path
    _flavour = _windows_flavour if os.name == "nt" else _posix_flavour


# base DIR Path is (Dot)Path of the repository root directory
DIR = DotPath(__file__).parent.parent.parent.resolve()
"""
DIR DotPath allows object-based access to all project directories with a single import.
The use of make_dirs(DIR) anytime the file is accessed ensures no errors from trying to access
folders that do not exist when code is run on new virtual machines.

Usage:

from src.common.directory import DIR

df = pd.read_csv(DIR.DATA.RAW / "raw_filename.csv")
...
df_results.to_parquet(DIR.DATA.RESULTS / "results.parquet")
"""


# src code folders
DIR.SRC = DIR / "src"
DIR.ASSIGN = DIR / "assignments"

# assignment folders
DIR.ASSIGN.KNAPSACK_02 = DIR.ASSIGN / "a02_knapsack"

# data folder with standard subfolders (should be gitignored)
DIR.DATA = DIR / "data"
DIR.DATA.LOGS = DIR.DATA / "logs"

# folder to put all figures in (should be gitignored)
DIR.FIGURES = DIR / "figures"

# all pytest test_**.py go under tests
DIR.TESTS = DIR / "tests"
# test data is nested under dir/tests
DIR.TESTS.TEST_FILES = DIR.TESTS / "test_files"

# config files
DIR.CONFIG = DIR / "config"


def make_dirs(indir: DotPath = DIR):
    """Recursively make all project directories of initial DotPath object fed in
    by looping through class attributes that are also custom added DotPath objects.

    :param indir: a DotPath object with child DotPath attributes already attached"""
    custom_child_attributes = (attr_name for attr_name in dir(indir) if "_" not in attr_name)
    for attr_name in custom_child_attributes:
        attribute = getattr(indir, attr_name)
        if isinstance(attribute, Path) and attr_name != "parent":
            attribute.mkdir(exist_ok=True, parents=False)
            make_dirs(attribute)


# run any time DIR is imported, even when __name__ != "__main__" to avoid any folder issues
make_dirs(DIR)
