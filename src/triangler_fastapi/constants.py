from enum import Enum


class SampleNames(str, Enum):
    """Sample names for beer tasting."""

    A = "Sample A"
    B = "Sample B"
    C = "Sample C"


class ExperienceLevels(str, Enum):
    """Experience levels for beer drinkers."""

    NON_BEER_DRINKER = "Non Beer Drinker"
    GENERAL_BEER_DRINKER = "General Beer Drinker"
    CRAFT_BEER_ENTHUSIAST = "Craft Enthusiast"
    HOMEBREWER = "Homebrewer"
    BJCP_TRAINING = "BJCP (training)"
    BJCP_RECOGNIZED_OR_HIGHER = "BJCP (Recognized or higher)"


def get_experience_level_description(level_id: int) -> str:
    """Get the experience level description from the level id."""
    for x in ExperienceLevels:
        if x.name == level_id:
            return x.value
    raise ValueError("Unknown experience level")


def get_experience_level_id(level_description: str) -> str:
    """Get the experience level id from the level description."""
    for x in ExperienceLevels:
        if x.value == level_description:
            return x.name
    return ExperienceLevels.NON_BEER_DRINKER.name
