import datetime
import re
from pathlib import Path

import click

# Global configuration for required project directories
DIRECTORIES = ["figures", "data"]


@click.group()
def prototyping() -> None:
    """Tools for prototyping in jupyter notebooks."""
    pass


@prototyping.command()
@click.argument(
    "directory",
    type=Path,
)
@click.argument(
    "name",
    type=str,
)
def new_project(directory: Path, name: str) -> None:
    """
    Create a new project directory structure for Jupyter notebook prototyping.

    Creates a timestamped project directory with the format YYYY-MM_<name> and
    initializes it with all directories specified in the global DIRECTORIES
    configuration. By default, this includes 'figures' and 'data' subdirectories.

    Parameters
    ----------
    directory : Path
        The parent directory where the new project directory will be created.
        Must be an existing directory with write permissions.
    name : str
        The name of the project. Must contain only alphanumeric characters,
        underscores (_), and hyphens (-). This will be appended to the current
        year-month to form the project directory name.

    Returns
    -------
    None
        This function does not return a value. It creates the directory structure
        and prints the location of the created project.

    Raises
    ------
    ValueError
        If the project name contains invalid characters (anything other than
        alphanumeric characters, underscores, or hyphens).
    FileExistsError
        If a directory with the generated name already exists in the specified
        parent directory.
    PermissionError
        If there are insufficient permissions to create directories in the
        specified location.

    Examples
    --------
    Create a new project in the current directory:

    >>> new_project(Path("."), "my_analysis")
    New project generated here: ./2025-07_my_analysis

    The created directory structure will be:
    2025-07_my_analysis/
    ├── figures/
    └── data/

    Notes
    -----
    The project directory name format is YYYY-MM_<name>, where YYYY-MM represents
    the current year and month. This helps organize projects chronologically.

    The subdirectories created are determined by the global DIRECTORIES variable,
    which can be configured to include different directory names as needed.
    """
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValueError(
            "Project names must only contain alphanumeric characters, '_' and '-'."
        )

    top_dir = directory / f"{datetime.date.today().strftime("%Y-%m")}_{name}"

    top_dir.mkdir()

    # Create all configured directories
    for dir_name in DIRECTORIES:
        (top_dir / dir_name).mkdir()

    print(f"New project generated here: {top_dir}")


@prototyping.command()
@click.argument(
    "project-dir",
    type=Path,
)
@click.argument(
    "name",
    type=str,
)
def new_notebook(project_dir: Path, name: str) -> None:
    """
    Create a new Jupyter notebook within an existing project directory.

    Creates a new .ipynb file in the specified project directory and sets up
    corresponding subdirectories for organizing notebook-specific outputs.
    For each directory specified in the global DIRECTORIES configuration,
    a subdirectory with the notebook's name is created to store related files.

    Parameters
    ----------
    project_dir : Path
        The path to an existing project directory. This directory must contain
        all subdirectories specified in the global DIRECTORIES configuration
        (by default: 'figures' and 'data').
    name : str
        The name of the notebook to create. Must contain only alphanumeric
        characters, underscores (_), and hyphens (-). The .ipynb extension
        will be added automatically.

    Returns
    -------
    None
        This function does not return a value. It creates the notebook file
        and associated directories, then prints the location of the created notebook.

    Raises
    ------
    ValueError
        If the notebook name contains invalid characters (anything other than
        alphanumeric characters, underscores, or hyphens).
    FileNotFoundError
        If the project directory does not exist, or if any of the required
        subdirectories (specified in DIRECTORIES) are missing from the project.
    FileExistsError
        If a notebook with the specified name already exists in the project
        directory.
    PermissionError
        If there are insufficient permissions to create files or directories
        in the specified location.

    Examples
    --------
    Create a new notebook in an existing project:

    >>> new_notebook(Path("./2025-07_my_analysis"), "data_exploration")
    New notebook generated here: /path/to/2025-07_my_analysis/data_exploration.ipynb

    This will create:
    - data_exploration.ipynb (empty notebook file)
    - figures/data_exploration/ (directory for plots and charts)
    - data/data_exploration/ (directory for processed data files)

    Notes
    -----
    The function validates that the project directory contains all required
    subdirectories as specified in the global DIRECTORIES configuration.
    This ensures that notebooks are only created in properly structured projects.

    The notebook-specific subdirectories help organize outputs by keeping
    each notebook's generated files separate and easily identifiable.

    If multiple directories are missing, the error message will list all
    missing directories to help with troubleshooting.
    """
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValueError(
            "Notebook names must only contain alphanumeric characters, '_' and '-'."
        )

    if not project_dir.exists():
        raise FileNotFoundError(f"Project directory does not exist: {project_dir}")

    # Use global configuration for expected directories
    expected_dirs = DIRECTORIES
    missing_dirs = []

    # Check each expected directory
    for dir_name in expected_dirs:
        dir_path = project_dir / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)

    # Handle missing directories
    if missing_dirs:
        if len(missing_dirs) == 1:
            # Single directory missing
            dir_name = missing_dirs[0]
            dir_path = project_dir / dir_name
            message = f"Project {dir_name} directory does not exist: {dir_path}. Make sure you're running this command in a valid project directory."
        else:
            # Multiple directories missing
            dirs_str = " and ".join(missing_dirs)
            message = f"Project {dirs_str} directories do not exist. Make sure you're running this command in a valid project directory."

        raise FileNotFoundError(message)

    notebook_path = (project_dir / name).with_suffix(".ipynb").absolute()

    if notebook_path.exists():
        raise FileExistsError(f"Notebook: {notebook_path} already exists.")

    with notebook_path.open("w+"):
        pass

    # Create notebook-specific directories
    for dir_name in expected_dirs:
        (project_dir / dir_name / name).with_suffix("").mkdir()

    print(f"New notebook generated here: {notebook_path}")


# need to be able to easily save figures and data to the correct folders
# https://claude.ai/chat/9bdc039b-345b-4f5d-ba51-53ebf1585696
