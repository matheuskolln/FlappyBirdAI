from abc import ABC
from typing import Tuple


class IBase(ABC):
    x: Tuple[int, int]
    y: int
