import datetime
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, List
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from trurl.prototyping import new_notebook, new_project, prototyping


@contextmanager
def mock_date(year: int, month: int, day: int) -> Generator[None, None, None]:
    """Context manager to mock datetime.date.today() for consistent testing."""
    with patch("trurl.prototyping.datetime") as mock_datetime:
        mock_datetime.date.today.return_value = datetime.date(year, month, day)
        yield


class TestNewProject:
    """Tests for the new_project command."""

    def test_new_project_success_valid_name(self, tmp_path: Path) -> None:
        """Test successful project creation with valid name."""
        runner = CliRunner()
        project_name = "test_project"

        with mock_date(2025, 7, 19):
            result = runner.invoke(new_project, [str(tmp_path), project_name])

            assert result.exit_code == 0

            # Check directory structure
            expected_dir = tmp_path / "2025-07_test_project"
            assert expected_dir.exists()
            assert expected_dir.is_dir()
            assert (expected_dir / "figures").exists()
            assert (expected_dir / "figures").is_dir()
            assert (expected_dir / "data").exists()
            assert (expected_dir / "data").is_dir()

            # Check output message
            assert f"New project generated here: {expected_dir}" in result.output

    def test_new_project_success_with_hyphens_and_underscores(
        self, tmp_path: Path
    ) -> None:
        """Test project creation with valid characters (hyphens and underscores)."""
        runner = CliRunner()
        project_name = "test-project_123"

        with mock_date(2025, 12, 31):
            result = runner.invoke(new_project, [str(tmp_path), project_name])

            assert result.exit_code == 0
            expected_dir = tmp_path / "2025-12_test-project_123"
            assert expected_dir.exists()

    def test_new_project_success_numeric_name(self, tmp_path: Path) -> None:
        """Test project creation with numeric name."""
        runner = CliRunner()
        project_name = "123456"

        with mock_date(2025, 1, 1):
            result = runner.invoke(new_project, [str(tmp_path), project_name])

            assert result.exit_code == 0
            expected_dir = tmp_path / "2025-01_123456"
            assert expected_dir.exists()

    def test_new_project_invalid_name_with_spaces(self, tmp_path: Path) -> None:
        """Test project creation fails with spaces in name."""
        runner = CliRunner()
        project_name = "test project"

        result = runner.invoke(new_project, [str(tmp_path), project_name])

        assert result.exit_code == 1
        assert (
            "Project names must only contain alphanumeric characters, '_' and '-'."
            in str(result.exception)
        )

    @pytest.mark.parametrize(
        "invalid_name",
        [
            "test@project",
            "test.project",
            "test/project",
            "test\\project",
            "test!project",
        ],
    )
    def test_new_project_invalid_name_with_special_chars(
        self, tmp_path: Path, invalid_name: str
    ) -> None:
        """Test project creation fails with special characters."""
        runner = CliRunner()

        result = runner.invoke(new_project, [str(tmp_path), invalid_name])
        assert result.exit_code == 1
        assert (
            "Project names must only contain alphanumeric characters, '_' and '-'."
            in str(result.exception)
        )

    def test_new_project_empty_name(self, tmp_path: Path) -> None:
        """Test project creation fails with empty name."""
        runner = CliRunner()
        project_name = ""

        result = runner.invoke(new_project, [str(tmp_path), project_name])

        assert result.exit_code == 1
        assert (
            "Project names must only contain alphanumeric characters, '_' and '-'."
            in str(result.exception)
        )

    def test_new_project_directory_already_exists(self, tmp_path: Path) -> None:
        """Test behavior when project directory already exists."""
        runner = CliRunner()
        project_name = "existing_project"

        with mock_date(2025, 7, 19):
            # Create the directory first
            existing_dir = tmp_path / "2025-07_existing_project"
            existing_dir.mkdir()

            result = runner.invoke(new_project, [str(tmp_path), project_name])

            # Should fail because directory already exists
            assert result.exit_code == 1
            assert isinstance(result.exception, FileExistsError)


class TestNewNotebook:
    """Tests for the new_notebook command."""

    def test_new_notebook_success_valid_name(self, tmp_path: Path) -> None:
        """Test successful notebook creation with valid name."""
        runner = CliRunner()

        # Create project structure first
        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        (project_dir / "figures").mkdir()
        (project_dir / "data").mkdir()

        notebook_name = "test_notebook"

        result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

        assert result.exit_code == 0

        # Check notebook file creation
        notebook_path = project_dir / "test_notebook.ipynb"
        assert notebook_path.exists()
        assert notebook_path.is_file()

        # Check corresponding directories
        assert (project_dir / "figures" / "test_notebook").exists()
        assert (project_dir / "figures" / "test_notebook").is_dir()
        assert (project_dir / "data" / "test_notebook").exists()
        assert (project_dir / "data" / "test_notebook").is_dir()

        # Check output message
        assert (
            f"New notebook generated here: {notebook_path.absolute()}" in result.output
        )

    def test_new_notebook_success_with_hyphens_and_underscores(
        self, tmp_path: Path
    ) -> None:
        """Test notebook creation with valid characters."""
        runner = CliRunner()

        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        (project_dir / "figures").mkdir()
        (project_dir / "data").mkdir()

        notebook_name = "test-notebook_123"

        result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

        assert result.exit_code == 0
        assert (project_dir / "test-notebook_123.ipynb").exists()
        assert (project_dir / "figures" / "test-notebook_123").exists()
        assert (project_dir / "data" / "test-notebook_123").exists()

    def test_new_notebook_invalid_name_with_spaces(self, tmp_path: Path) -> None:
        """Test notebook creation fails with spaces in name."""
        runner = CliRunner()

        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        (project_dir / "figures").mkdir()
        (project_dir / "data").mkdir()

        notebook_name = "test notebook"

        result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

        assert result.exit_code == 1
        assert (
            "Notebook names must only contain alphanumeric characters, '_' and '-'."
            in str(result.exception)
        )

    @pytest.mark.parametrize(
        "invalid_name",
        ["test@notebook", "test.notebook", "test/notebook", "test!notebook"],
    )
    def test_new_notebook_invalid_name_with_special_chars(
        self, tmp_path: Path, invalid_name: str
    ) -> None:
        """Test notebook creation fails with special characters."""
        runner = CliRunner()

        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        (project_dir / "figures").mkdir()
        (project_dir / "data").mkdir()

        result = runner.invoke(new_notebook, [str(project_dir), invalid_name])
        assert result.exit_code == 1
        assert (
            "Notebook names must only contain alphanumeric characters, '_' and '-'."
            in str(result.exception)
        )

    def test_new_notebook_already_exists(self, tmp_path: Path) -> None:
        """Test notebook creation fails when file already exists."""
        runner = CliRunner()

        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        (project_dir / "figures").mkdir()
        (project_dir / "data").mkdir()

        notebook_name = "existing_notebook"

        # Create the notebook file first
        existing_notebook = project_dir / "existing_notebook.ipynb"
        existing_notebook.touch()

        result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

        assert result.exit_code == 1
        assert isinstance(result.exception, FileExistsError)
        assert f"Notebook: {existing_notebook.absolute()} already exists." in str(
            result.exception
        )

    def test_new_notebook_nonexistent_project_dir(self, tmp_path: Path) -> None:
        """Test notebook creation fails when project directory doesn't exist."""
        runner = CliRunner()

        nonexistent_dir = tmp_path / "nonexistent_project"
        notebook_name = "test_notebook"

        result = runner.invoke(new_notebook, [str(nonexistent_dir), notebook_name])

        assert result.exit_code == 1
        assert isinstance(result.exception, FileNotFoundError)
        assert f"Project directory does not exist: {nonexistent_dir}" in str(
            result.exception
        )

    def test_new_notebook_missing_figures_dir_only(self, tmp_path: Path) -> None:
        """Test notebook creation when only figures directory is missing."""
        runner = CliRunner()

        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        # Create data directory but not figures
        (project_dir / "data").mkdir()

        notebook_name = "test_notebook"

        result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

        assert result.exit_code == 1
        assert isinstance(result.exception, FileNotFoundError)
        assert "Project figures directory does not exist" in str(result.exception)
        assert (
            "Make sure you're running this command in a valid project directory"
            in str(result.exception)
        )

    def test_new_notebook_missing_data_dir_only(self, tmp_path: Path) -> None:
        """Test notebook creation when only data directory is missing."""
        runner = CliRunner()

        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        # Create figures directory but not data
        (project_dir / "figures").mkdir()

        notebook_name = "test_notebook"

        result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

        assert result.exit_code == 1
        assert isinstance(result.exception, FileNotFoundError)
        assert "Project data directory does not exist" in str(result.exception)
        assert (
            "Make sure you're running this command in a valid project directory"
            in str(result.exception)
        )

    def test_new_notebook_missing_both_figures_and_data_dirs(
        self, tmp_path: Path
    ) -> None:
        """Test notebook creation when both figures and data directories are missing."""
        runner = CliRunner()

        project_dir = tmp_path / "test_project"
        project_dir.mkdir()
        # Don't create figures and data directories

        notebook_name = "test_notebook"

        result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

        assert result.exit_code == 1
        assert isinstance(result.exception, FileNotFoundError)
        assert "Project figures and data directories do not exist" in str(
            result.exception
        )
        assert (
            "Make sure you're running this command in a valid project directory"
            in str(result.exception)
        )


class TestPrototypingGroup:
    """Tests for the prototyping command group."""

    def test_prototyping_group_help(self) -> None:
        """Test that the prototyping group shows help correctly."""
        runner = CliRunner()
        result = runner.invoke(prototyping, ["--help"])

        assert result.exit_code == 0
        assert "Tools for prototyping in jupyter notebooks." in result.output
        assert "new-project" in result.output
        assert "new-notebook" in result.output

    def test_new_project_help(self) -> None:
        """Test new-project command help."""
        runner = CliRunner()
        result = runner.invoke(prototyping, ["new-project", "--help"])

        assert result.exit_code == 0

    def test_new_notebook_help(self) -> None:
        """Test new-notebook command help."""
        runner = CliRunner()
        result = runner.invoke(prototyping, ["new-notebook", "--help"])

        assert result.exit_code == 0


class TestCustomDirectoryConfiguration:
    """Tests for custom directory configurations using mocked DIRECTORIES variable."""

    @pytest.mark.parametrize(
        "directories",
        [
            ["figures", "data"],  # Default configuration
            ["plots", "datasets"],  # Alternative names
            ["figures", "data", "scripts"],  # Extended set
            ["output"],  # Minimal set
            ["charts", "raw_data", "processed_data", "models"],  # Complex configuration
        ],
    )
    def test_new_project_with_custom_directories(
        self, tmp_path: Path, directories: List[str]
    ) -> None:
        """Test project creation with different directory configurations."""
        runner = CliRunner()
        project_name = "test_project"

        with patch("trurl.prototyping.DIRECTORIES", directories):
            with mock_date(2025, 7, 19):
                result = runner.invoke(new_project, [str(tmp_path), project_name])

                assert result.exit_code == 0

                # Check that all configured directories were created
                expected_dir = tmp_path / "2025-07_test_project"
                assert expected_dir.exists()

                for dir_name in directories:
                    dir_path = expected_dir / dir_name
                    assert dir_path.exists(), f"Directory {dir_name} was not created"
                    assert dir_path.is_dir(), f"{dir_name} is not a directory"

    @pytest.mark.parametrize(
        "directories",
        [
            ["figures", "data"],  # Default configuration
            ["plots", "datasets"],  # Alternative names
            ["figures", "data", "scripts"],  # Extended set
            ["output"],  # Minimal set
        ],
    )
    def test_new_notebook_with_custom_directories(
        self, tmp_path: Path, directories: List[str]
    ) -> None:
        """Test notebook creation with different directory configurations."""
        runner = CliRunner()

        with patch("trurl.prototyping.DIRECTORIES", directories):
            # First create a project with the custom directories
            project_dir = tmp_path / "test_project"
            project_dir.mkdir()

            # Create all required directories
            for dir_name in directories:
                (project_dir / dir_name).mkdir()

            notebook_name = "test_notebook"

            result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

            assert result.exit_code == 0

            # Check notebook file creation
            notebook_path = project_dir / "test_notebook.ipynb"
            assert notebook_path.exists()

            # Check that notebook-specific directories were created in all configured directories
            for dir_name in directories:
                notebook_subdir = project_dir / dir_name / "test_notebook"
                assert (
                    notebook_subdir.exists()
                ), f"Notebook subdirectory in {dir_name} was not created"
                assert (
                    notebook_subdir.is_dir()
                ), f"Notebook subdirectory in {dir_name} is not a directory"

    def test_new_notebook_missing_custom_directories(self, tmp_path: Path) -> None:
        """Test notebook creation fails when custom directories are missing."""
        runner = CliRunner()
        custom_dirs = ["plots", "datasets", "models"]

        with patch("trurl.prototyping.DIRECTORIES", custom_dirs):
            project_dir = tmp_path / "test_project"
            project_dir.mkdir()
            # Don't create any of the required directories

            notebook_name = "test_notebook"

            result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

            assert result.exit_code == 1
            assert isinstance(result.exception, FileNotFoundError)
            # Should mention all missing directories
            error_msg = str(result.exception)
            assert "plots and datasets and models directories do not exist" in error_msg

    def test_new_notebook_partially_missing_custom_directories(
        self, tmp_path: Path
    ) -> None:
        """Test notebook creation fails when some custom directories are missing."""
        runner = CliRunner()
        custom_dirs = ["plots", "datasets", "models"]

        with patch("trurl.prototyping.DIRECTORIES", custom_dirs):
            project_dir = tmp_path / "test_project"
            project_dir.mkdir()
            # Create only some directories
            (project_dir / "plots").mkdir()
            (project_dir / "datasets").mkdir()
            # Don't create "models" directory

            notebook_name = "test_notebook"

            result = runner.invoke(new_notebook, [str(project_dir), notebook_name])

            assert result.exit_code == 1
            assert isinstance(result.exception, FileNotFoundError)
            # Should mention only the missing directory
            error_msg = str(result.exception)
            assert "Project models directory does not exist" in error_msg
            assert "plots" not in error_msg  # Should not mention existing directories
            assert "datasets" not in error_msg

    def test_empty_directories_configuration(self, tmp_path: Path) -> None:
        """Test behavior with empty DIRECTORIES configuration."""
        runner = CliRunner()

        with patch("trurl.prototyping.DIRECTORIES", []):
            with mock_date(2025, 7, 19):
                # Test project creation
                project_name = "empty_config_project"
                result1 = runner.invoke(new_project, [str(tmp_path), project_name])

                assert result1.exit_code == 0
                expected_dir = tmp_path / "2025-07_empty_config_project"
                assert expected_dir.exists()
                # No subdirectories should be created
                subdirs = [item for item in expected_dir.iterdir() if item.is_dir()]
                assert len(subdirs) == 0

                # Test notebook creation
                notebook_name = "test_notebook"
                result2 = runner.invoke(
                    new_notebook, [str(expected_dir), notebook_name]
                )

                assert result2.exit_code == 0
                # Notebook should be created successfully
                notebook_path = expected_dir / "test_notebook.ipynb"
                assert notebook_path.exists()


class TestIntegrationWorkflow:
    """Integration tests for typical workflows."""

    def test_complete_workflow(self, tmp_path: Path) -> None:
        """Test complete workflow: create project, then create notebook."""
        runner = CliRunner()

        with mock_date(2025, 7, 19):
            # Step 1: Create project
            project_name = "integration_test"
            result1 = runner.invoke(new_project, [str(tmp_path), project_name])
            assert result1.exit_code == 0

            project_dir = tmp_path / "2025-07_integration_test"
            assert project_dir.exists()

            # Step 2: Create notebook in the project
            notebook_name = "analysis_notebook"
            result2 = runner.invoke(new_notebook, [str(project_dir), notebook_name])
            assert result2.exit_code == 0

            # Verify complete structure
            assert (project_dir / "analysis_notebook.ipynb").exists()
            assert (project_dir / "figures" / "analysis_notebook").exists()
            assert (project_dir / "data" / "analysis_notebook").exists()

    def test_multiple_notebooks_in_project(self, tmp_path: Path) -> None:
        """Test creating multiple notebooks in the same project."""
        runner = CliRunner()

        with mock_date(2025, 7, 19):
            # Create project
            project_name = "multi_notebook_test"
            result1 = runner.invoke(new_project, [str(tmp_path), project_name])
            assert result1.exit_code == 0

            project_dir = tmp_path / "2025-07_multi_notebook_test"

            # Create multiple notebooks
            notebooks = ["notebook1", "notebook2", "analysis-final"]

            for notebook_name in notebooks:
                result = runner.invoke(new_notebook, [str(project_dir), notebook_name])
                assert result.exit_code == 0

                # Verify each notebook and its directories
                assert (project_dir / f"{notebook_name}.ipynb").exists()
                assert (project_dir / "figures" / notebook_name).exists()
                assert (project_dir / "data" / notebook_name).exists()

    def test_complete_workflow_with_custom_directories(self, tmp_path: Path) -> None:
        """Test complete workflow with custom directory configuration."""
        runner = CliRunner()
        custom_dirs = ["charts", "raw_data", "processed_data"]

        with patch("trurl.prototyping.DIRECTORIES", custom_dirs):
            with mock_date(2025, 7, 19):
                # Step 1: Create project
                project_name = "custom_integration_test"
                result1 = runner.invoke(new_project, [str(tmp_path), project_name])
                assert result1.exit_code == 0

                project_dir = tmp_path / "2025-07_custom_integration_test"
                assert project_dir.exists()

                # Verify custom directories were created
                for dir_name in custom_dirs:
                    assert (project_dir / dir_name).exists()

                # Step 2: Create notebook in the project
                notebook_name = "analysis_notebook"
                result2 = runner.invoke(new_notebook, [str(project_dir), notebook_name])
                assert result2.exit_code == 0

                # Verify complete structure with custom directories
                assert (project_dir / "analysis_notebook.ipynb").exists()
                for dir_name in custom_dirs:
                    assert (project_dir / dir_name / "analysis_notebook").exists()
