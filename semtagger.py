#!/usr/bin/env python3
"""
Semtagger - A tool for managing semantic version tags in git repositories
"""

import argparse
import logging
import sys
from gitstuff import 
from semver import SemanticVersion

logger = logging.getLogger(__name__)

def main():
  """Main function for semtagger"""
  ########################
  ### Argument Parsing ###
  ########################
  parser = argparse.ArgumentParser(
    description='Semtagger - Manage semantic version tags in git repositories',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  %(prog)s -p        # Increment patch version (1.0.0 -> 1.0.1)
  %(prog)s -m        # Increment minor version (1.0.0 -> 1.1.0)
  %(prog)s -M        # Increment major version (1.0.0 -> 2.0.0)
  %(prog)s -p -l rc1 # Increment patch and add label (1.0.0 -> 1.0.1-rc1)
  %(prog)s -p -u     # Increment patch and push to remote
  %(prog)s -p -vvv   # Increment patch with debug logging
        """
  )
  parser.add_argument('-v', '--verbose', action='count', default=0, help='Verbosity (-v for INFO, -vv for DEBUG)')
  parser.add_argument('-f', '--force', action='store_true', default=False, help='Force the operation even if not on main/master branch')
  parser.add_argument('-b', '--by', action='store', type=int, default=1, help='Increment by a specific number')
  
  version_group = parser.add_mutually_exclusive_group(required=True)
  version_group.add_argument('-p', '--patch', action='store_true', help='Increment patch version (x.x.PATCH)')
  version_group.add_argument('-m', '--minor', action='store_true', help='Increment minor version (x.MINOR.0)')
  version_group.add_argument('-M', '--major', action='store_true', help='Increment major version (MAJOR.0.0)')
  
  parser.add_argument('-l', '--label', type=str, default=None, help='Add label to the version (e.g., -l rc1 creates 1.0.0-rc1)')
  parser.add_argument('-u', '--push', action='store_true', help='Push the new tag to remote repository', default=False)
  args = parser.parse_args()
  
  ### Logging based on verbosity ###
  if args.verbose == 0:
    log_level = logging.WARNING
  elif args.verbose == 1:
    log_level = logging.INFO
  else:
    log_level = logging.DEBUG
  
  logging.basicConfig(
    level=log_level,
    format='%(message)s' # Keep it simple (no timestamps, severity etc.)
  )
  
  ##################
  ### Main Logic ###
  ##################
  logger.debug(f"Arguments: {args}")
  
  ### Check if this is a git workspace ###
  repo = git_workspace()
  if repo is None:
    logger.error("Not a git repository. Exiting.")
    sys.exit(1)
  
  ## Check if on main/master branch (warning only)
  if not gittags.check_main_branch(repo):
    logger.warning("You are not on the main/master branch.")
    if not args.force:
      logger.error("Use -f to force the operation on non-main/master branches.")
      sys.exit(2)
  
  ## Get latest tag
  latest_tag = gittags.get_latest_tag(repo)
  
  if latest_tag is None:
    # No tags found, start with 0.0.0
    logger.debug("No semantic version tags found. Starting with 0.0.0")
    current_version = SemanticVersion("0.0.0")
  else:
    try:
      current_version = SemanticVersion(latest_tag)
    except ValueError as e:
      logger.error(f"Error parsing latest tag: {e}")
      sys.exit(1)
  
  ### Increment version ###
  if args.major:
    logger.debug("Incrementing major version")
    current_version.increment_major(by=args.by)
  elif args.minor:
    logger.debug("Incrementing minor version")
    current_version.increment_minor(by=args.by)
  elif args.patch:
    logger.debug("Incrementing patch version")
    current_version.increment_patch(by=args.by)
  
  ### Label ###
  if args.label:
    logger.debug(f"Adding label: {args.label}")
    current_version.set_label(args.label)
  
  new_tag = str(current_version)
  logger.info(f"New version: {new_tag}")
  
  # Always print the new tag - could use critial for this
  print(f"{new_tag}")
  
  ### Create tag and optionally push ###
  if not gittags.create_and_push_tag(repo, new_tag, push=args.push):
    sys.exit(1)
  
  logger.info("Done!")


if __name__ == "__main__":
  main()
