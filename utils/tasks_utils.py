from transliterate import translit

from modules.problems.models import Tasks
from utils.translation_utils import translate


def difficulty_key(value):
    if 1 <= value <= 4:
        return "easy"
    if 5 <= value <= 7:
        return "medium"
    else:
        return "hard"
    

def auto_slug(text):

    slug = translit(text.lower().replace(' ', '_'), 'ru', reversed=True)

    i = 1
    while Tasks.query.filter_by(title=slug).first():
        slug = f"{slug}_{i}"
        i += 1

    return slug
    