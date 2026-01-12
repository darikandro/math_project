from modules.problems.models import Tasks
from utils.translation_utils import translate


def difficulty_key(value):
    if 1 <= value <= 4:
        return "easy"
    if 5 <= value <= 7:
        return "medium"
    else:
        return "hard"
    