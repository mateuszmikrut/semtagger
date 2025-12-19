# Semantic Version GIT Tagger

A pretty trivial python script to easily manage git tags with semantic versioning (semver.org)  

## Usage

```bash
semtag [options]
```

### Options

<!-- OPTIONS:START -->
<!-- OPTIONS:END -->

### Examples

```bash
# Increment minor version (1.0.0 -> 1.1.0)
semtag -m

# Increment major version (1.0.0 -> 2.0.0)
semtag -M

# Increment patch version (1.0.0 -> 1.0.5)
semtag -p -b 5

# Increment patch and add label (1.0.0 -> 1.0.1-rc1), don't fetch and push new tag
semtag -n -u -p -l rc1
```

## Installation

Using pip  (preferred)
```bash
pip install semtag
```

From git
```bash
git clone https://github.com/mateuszmikrut/semtag.git
cd semtag
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python ./semtag.py
```

## Supported Version Formats

The script supports semantic versioning with the following formats:
- `v1.0.0` (with 'v' prefix)
- `1.0.0` (without prefix)
- `1.0.0-rc1` (with prerelease label)

When incrementing versions, prerelease labels are automatically removed.

