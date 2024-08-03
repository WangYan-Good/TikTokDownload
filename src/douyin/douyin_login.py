## <<Base>>
import os
from pathlib import Path
import sys

## <<Extension>>

## <<Third-part>>
from login import Login

class DouyinLogin(Login):

  def __init__(self, path: Path = None):
    super().__init__(path)

  # def