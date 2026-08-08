from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class UserProfile:
    experience_level: str
    languages: List[str]
    interests: List[str]
    goal: str
    available_hours_per_day: float
    learning_style: str = "building"


@dataclass
class Repository:
    name: str
    full_name: str
    url: str
    description: str
    language: str
    stars: int
    forks: int
    open_issues: int
    topics: List[str] = field(default_factory=list)

    has_readme: bool = False
    has_license: bool = False
    has_contributing: bool = False

    size_kb: int = 0
    updated_at: str = ""

    languages: Dict[str, int] = field(default_factory=dict)


@dataclass
class RepositoryEvaluation:
    repository: Repository

    documentation: float
    activity: float
    setup: float
    contribution: float
    architecture: float
    learning_value: float
    goal_alignment: float
    technology_match: float

    overall_score: float
    reasons: List[str] = field(default_factory=list)


@dataclass
class Recommendation:
    repository: Repository
    match_percentage: float
    reasons: List[str]
    concerns: List[str]