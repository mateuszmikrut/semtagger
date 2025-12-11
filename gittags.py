"""
Git tag management module
"""

import logging
import sys
from pathlib import Path
from typing import Optional

try:
  import git
except ImportError:
  print("Error: GitPython library is required. Install it with: pip install gitpython")
  sys.exit(1)

from semver import SemanticVersion

logger = logging.getLogger(__name__)


def check_git_workspace(repo_path: str = ".") -> Optional[git.Repo]:
  """Check if current directory is a git workspace and return repo"""
  try:
    repo = git.Repo(Path(repo_path).resolve(), search_parent_directories=True)
    logger.debug(f"Found git repository at {repo.working_dir}")
    return repo
  except git.InvalidGitRepositoryError:
    logger.error(f"'{repo_path}' is not a git repository")
    return None
  except git.GitCommandError as e:
    logger.error(f"Git command failed: {e}")
    return None


def check_main_branch(repo: git.Repo) -> bool:
  """Check if currently on main or master branch"""
  try:
    current_branch = repo.active_branch.name
    if current_branch not in ['main', 'master']:
      logger.warning(f"You are on branch '{current_branch}', not on main/master")
      return False
    logger.debug(f"On {current_branch} branch")
    return True
  except TypeError:
    logger.warning("HEAD is detached, not on any branch")
    return False


def pull_from_remote(repo: git.Repo) -> bool:
  """Pull latest changes from remote"""
  try:
    origin = repo.remote('origin')
    logger.info(f"Pulling from remote '{origin.name}'...")
    origin.pull()
    logger.info("Successfully pulled latest changes")
    return True
  except git.GitCommandError as e:
    logger.error(f"Error pulling from remote: {e}")
    return False
  except ValueError:
    logger.warning("No remote named 'origin' found")
    return False


def get_latest_tag(repo: git.Repo) -> Optional[str]:
  """Get the latest semantic version tag"""
  try:
    tags = repo.tags
    if not tags:
      logger.info("No tags found in repository")
      return None
    
    logger.debug(f"Found {len(tags)} total tags")
    
    # Filter and sort semantic version tags
    semantic_tags = []
    for tag in tags:
      try:
        version = SemanticVersion(tag.name)
        semantic_tags.append((tag.name, version))
        logger.debug(f"Valid semantic version tag: {tag.name}")
      except ValueError:
        # Skip non-semantic version tags
        logger.debug(f"Skipping non-semantic tag: {tag.name}")
        continue
    
    if not semantic_tags:
      logger.info("No semantic version tags found")
      return None
    
    # Sort by major, minor, patch (ignoring prerelease for sorting)
    semantic_tags.sort(
      key=lambda x: (x[1].major, x[1].minor, x[1].patch),
      reverse=True
    )
    
    latest_tag = semantic_tags[0][0]
    logger.info(f"Latest tag: {latest_tag}")
    return latest_tag
    
  except Exception as e:
    logger.error(f"Error getting tags: {e}")
    return None


def create_and_push_tag(repo: git.Repo, new_tag: str, push: bool = False) -> bool:
  """Create a new tag and optionally push it"""
  try:
    # Create the tag
    logger.info(f"Creating tag: {new_tag}")
    repo.create_tag(new_tag, message=f"Release {new_tag}")
    logger.info(f"Successfully created tag: {new_tag}")
    
    # Push if requested
    if push:
      logger.info(f"Pushing tag '{new_tag}' to remote...")
      origin = repo.remote('origin')
      origin.push(new_tag)
      logger.info(f"Successfully pushed tag: {new_tag}")
    else:
      logger.debug("Skipping push (not requested)")
    
    return True
    
  except git.GitCommandError as e:
    logger.error(f"Error creating/pushing tag: {e}")
    return False
  except ValueError as e:
    logger.error(f"Error: {e}")
    return False
