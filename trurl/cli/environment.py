import subprocess
import tempfile
import tomllib
from hashlib import md5
from pathlib import Path


def conda_export() -> None:
    """"""
    with Path("pyproject.toml").open("rb") as f:
        data = tomllib.load(f)

    # Get location of file
    saved_environment_file_path = Path(data["project"]["environment-file"])

    # raise error if there is no file
    if not saved_environment_file_path.exists():
        raise FileNotFoundError(
            f"The environment file specified at {saved_environment_file_path}"
            "could not be found. "
            f"Please output your file  with `conda env export "
            "--file {saved_environment_file_path}` "
            "and stage it before continuing."
        )

    with saved_environment_file_path.open("rb") as fp:
        saved_md5 = md5(fp.read()).hexdigest()

    with tempfile.TemporaryDirectory() as tdir:
        # Export dependencies to a temporary location and compute MD5 checksum
        current_environment_file_path = Path(tdir) / "environment.yaml"
        subprocess.run(
            ["conda", "env", "export", "--file", current_environment_file_path],
        )
        with current_environment_file_path.open("rb") as fp:
            current_md5 = md5(fp.read()).hexdigest()

    if saved_md5 != current_md5:
        raise ValueError(
            f"Saved environment file at {saved_environment_file_path} "
            "differs from the current conda environment. This might be "
            "caused by:\n"
            "1. You have installed or upgraded packages "
            f"without updating {saved_environment_file_path}.\n"
            "In this case, run `conda env export --file "
            f"{saved_environment_file_path}` to proceed.\n"
            "2. You have pulled, rolled back, or checked out a "
            "branch with different "
            "packages installed to your current environment.\n"
            "In this case, run `conda env update --file "
            f"{saved_environment_file_path}` to proceed."
        )

    print(
        "Your environment is consistent with your "
        f"environment file at {saved_environment_file_path}"
    )
