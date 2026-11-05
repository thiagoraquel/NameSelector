from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class NameRecord:
    """Pure data model for a name entry stored in the application.

    This class represents a single curated name and all metadata associated with it,
    without depending on SQLite, file I/O, or SQL logic.
    """

    name: str
    category: str
    gender: str
    species: str
    sub_species: str
    id: Optional[int] = None

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.category = self.category.strip()
        self.gender = self.gender.strip().lower()
        self.species = self.species.strip()
        self.sub_species = self.sub_species.strip()

        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.category:
            raise ValueError("category cannot be empty")
        if not self.gender:
            raise ValueError("gender cannot be empty")
        if not self.species:
            raise ValueError("species cannot be empty")
        if not self.sub_species:
            raise ValueError("sub_species cannot be empty")