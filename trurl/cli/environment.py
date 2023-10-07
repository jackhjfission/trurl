import os
import subprocess
import sys
import tomllib
from pathlib import Path

"""Location of the pyproject.toml file in local file system."""
TRURL_CONFIG_PATH = os.getenv("TRURL_CONFIG_PATH")


def conda_export(
    pyproject_path: os.PathLike[str] = TRURL_CONFIG_PATH,
) -> None:
    """Export the `conda` base environment to a file to the environment
    file specifed in `pyproject_path`.

    Parameters
    ----------
    pyproject_path : os.PathLike[str], optional, default = :obj:`TRURL_CONFIG_PATH`
        The path to the project's `pyproject.toml` file, which must contain
        the nested structure: `["tool"]["trurl"]["environment-file"]`
    """
    with Path(pyproject_path).open("rb") as f:
        data = tomllib.load(f)

    # Get location of file
    saved_environment_file_path = Path(data["tool"]["trurl"]["environment-file"])

    print(f"Outputting conda environment file to {saved_environment_file_path}")
    subprocess.run(["mamba", "env", "export", "--file", saved_environment_file_path])


def conda_update(
    pyproject_path: os.PathLike[str] = TRURL_CONFIG_PATH,
) -> None:
    """Update the `conda` base environment according to the environment
    file specifed in `pyproject_path`.

    Parameters
    ----------
    pyproject_path : os.PathLike[str], optional, default = :obj:`TRURL_CONFIG_PATH`
        The path to the project's `pyproject.toml` file, which must contain
        the nested structure: `["tool"]["trurl"]["environment-file"]`

    Raises
    ------
    FileNotFoundError
        If the environment file is not found.
    """
    with Path(pyproject_path).open("rb") as f:
        data = tomllib.load(f)

    # Get location of file
    saved_environment_file_path = Path(data["tool"]["trurl"]["environment-file"])

    # raise error if there is no file
    if not saved_environment_file_path.exists():
        raise FileNotFoundError(
            f"The environment file specified at {saved_environment_file_path}"
            "could not be found. "
            "Please output your file  with `trurl conda-export` "
            "and stage it before continuing."
        )

    print(f"Updating conda environment file with {saved_environment_file_path}")
    subprocess.run(["mamba", "env", "update", "--file", saved_environment_file_path])


def conda_compare(
    pyproject_path: os.PathLike[str] = TRURL_CONFIG_PATH,
) -> None:
    """Compare the current conda installation to the environment
    file specifed in `pyproject_path`.

    `conda compare` passes if all of the packages in the specified file are installed
    in the environment. If there are packages listed in the file which are not
    installed in the environment they are ignored.

    Parameters
    ----------
    pyproject_path : os.PathLike[str], optional, default = :obj:`TRURL_CONFIG_PATH`
        The path to the project's `pyproject.toml` file, which must contain
        the nested structure: `["tool"]["trurl"]["environment-file"]`

    Raises
    ------
    FileNotFoundError
        If the environment file is not found.

    ValueError
        If the two environments are not equivalent.

    """
    with Path(pyproject_path).open("rb") as f:
        data = tomllib.load(f)

    # Get location of file
    saved_environment_file_path = Path(data["tool"]["trurl"]["environment-file"])

    # raise error if there is no file
    if not saved_environment_file_path.exists():
        raise FileNotFoundError(
            f"The environment file specified at {saved_environment_file_path}"
            "could not be found. "
            "Please output your file  with `trurl conda-export` "
            "and stage it before continuing."
        )

    compare_output = subprocess.run(
        f"conda compare {saved_environment_file_path}",
        stdout=subprocess.PIPE,
        text=True,
        shell=True,
    )

    print(compare_output.stdout)
    sys.exit(compare_output.returncode)
