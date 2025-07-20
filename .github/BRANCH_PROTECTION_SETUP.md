# Branch Protection Setup

To ensure that PRs cannot be merged when pre-commit checks fail, you need to set up branch protection rules in your GitHub repository.

## Steps to Enable Branch Protection:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Branches**
3. Click **Add rule** or edit an existing rule for your main branch
4. Configure the following settings:

### Required Settings:
- ✅ **Require status checks to pass before merging**
- ✅ **Require branches to be up to date before merging**
- ✅ Under "Status checks that are required", search for and select:
  - `pre-commit` (this is the job name from our workflow)

### Recommended Additional Settings:
- ✅ **Require pull request reviews before merging**
- ✅ **Dismiss stale pull request approvals when new commits are pushed**
- ✅ **Require review from code owners** (if you have a CODEOWNERS file)
- ✅ **Restrict pushes that create files that exceed 100 MB**
- ✅ **Require linear history** (optional, prevents merge commits)

## What This Achieves:

Once configured, this setup will:
- Run all pre-commit hooks (Black, Ruff, mypy, isort, etc.) on every PR
- Prevent merging if any hook fails
- Show clear feedback about which checks failed
- Require fixes before the PR can be merged
- Maintain code quality standards automatically

## Local Development:

Developers should install pre-commit locally to catch issues before pushing:

```bash
# Install pre-commit hooks locally
poetry run pre-commit install

# Run hooks manually on all files
poetry run pre-commit run --all-files

# Run hooks on staged files only
poetry run pre-commit run
```

This ensures a smooth development workflow where issues are caught early.
