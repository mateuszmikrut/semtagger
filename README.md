# Semantic Versionning GIT Tagger

A pretty trivial python script to easely manage git tags with semantic versioning (semver.org)  

## Features

- ✅ Check if directory is a git workspace
- ✅ Warn if not on main/master branch
- ✅ Optional pull from remote before tagging
- ✅ Get latest semantic version tag
- ✅ Increment major, minor, or patch version
- ✅ Support for various version formats (v1.0.0, 1.0.0, 1.0.0-rc1)
- ✅ Create and optionally push tags to remote

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make the script executable (optional):
```bash
chmod +x git_tagger.py
```

## Usage

```bash
python git_tagger.py [options]
```

### Options

- `-p, --patch` - Increment patch version (x.x.PATCH)
- `-m, --minor` - Increment minor version (x.MINOR.0)
- `-M, --major` - Increment major version (MAJOR.0.0)
- `-u, --push` - Push the new tag to remote repository
- `--pull` - Pull from remote before creating tag
- `-v, --verbose` - Increase verbosity (use -v, -vv, or -vvv for more detail)
- `--dry-run` - Show what would be done without actually creating or pushing tags

### Examples

```bash
# Increment patch version (1.0.0 -> 1.0.1)
python git_tagger.py -p

# Increment minor version (1.0.0 -> 1.1.0)
python git_tagger.py -m

# Increment major version (1.0.0 -> 2.0.0)
python git_tagger.py -M

# Increment patch and push to remote
python git_tagger.py -p -u
# Pull before tagging and push
python git_tagger.py -p --pull -u

# With verbose output (INFO level)
python git_tagger.py -p -v
# With debug output (DEBUG level)
python git_tagger.py -p -vvv

# Dry run to preview changes without making them
python git_tagger.py -p --dry-run

# Dry run with push flag to see what would happen
python git_tagger.py -p -u --dry-run
```hon git_tagger.py -p -vvv
```hon git_tagger.py -p --pull -u
```

## Supported Version Formats

The script supports semantic versioning with the following formats:
- `v1.0.0` (with 'v' prefix)
- `1.0.0` (without prefix)
- `1.0.0-rc1` (with prerelease label)

When incrementing versions, prerelease labels are automatically removed.

