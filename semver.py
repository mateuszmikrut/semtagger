"""
Semantic versioning module for parsing and incrementing version strings
"""

import logging
import re

logger = logging.getLogger(__name__)


class SemanticVersion:
  """Handle semantic versioning parsing and increment operations"""
  
  def __init__(self, version_string: str):
    self.original = version_string
    self.prefix = ""
    self.major = 0
    self.minor = 0
    self.patch = 0
    self.prerelease = ""
  def _parse(self, version_string: str):
    """Parse semantic version string"""
    # Remove 'v' prefix if present
    if version_string.startswith('v'):
      self.prefix = 'v'
      version_string = version_string[1:]
    
    # Pattern to match semantic versioning: major.minor.patch[-prerelease]
    pattern = r'^(\d+)\.(\d+)\.(\d+)(?:-(.+))?$'
    match = re.match(pattern, version_string)
    
    if not match:
      raise ValueError(f"Invalid semantic version format: {self.original}")
    
    self.major = int(match.group(1))
    self.minor = int(match.group(2))
    self.patch = int(match.group(3))
    self.prerelease = match.group(4) or ""
    
    logger.debug(f"Parsed version: {self.major}.{self.minor}.{self.patch}" +
                 (f"-{self.prerelease}" if self.prerelease else ""))
    self.minor = int(match.group(2))
    self.patch = int(match.group(3))
    self.prerelease = match.group(4) or ""
  
  def increment_major(self) -> 'SemanticVersion':
    """Increment major version and reset minor and patch"""
    self.major += 1
    self.minor = 0
    self.patch = 0
    self.prerelease = ""
    return self
  
  def increment_minor(self) -> 'SemanticVersion':
    """Increment minor version and reset patch"""
    self.minor += 1
    self.patch = 0
    self.prerelease = ""
    return self
  
  def increment_patch(self) -> 'SemanticVersion':
    """Increment patch version"""
    self.patch += 1
    self.prerelease = ""
    return self
  
  def set_label(self, label: str) -> 'SemanticVersion':
    """Set a label/prerelease identifier"""
    self.prerelease = label
    return self
  
  def __str__(self) -> str:
    """Return formatted version string"""
    version = f"{self.prefix}{self.major}.{self.minor}.{self.patch}"
    if self.prerelease:
      version += f"-{self.prerelease}"
    return version
  
  def __repr__(self) -> str:
    """Return representation of version"""
    return f"SemanticVersion('{str(self)}')"
