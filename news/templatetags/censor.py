from django import template
import re

register = template.Library()

# Список нежелательных слов или фраз для цензуры
censored_words = ['нежелательное_слово_1', 'нежелательное_слово_2', ]


@register.filter
def censor(value):
    for word in censored_words:
        # Заменяем нежелательное слово или фразу на звёздочки
        value = re.sub(rf'\b{re.escape(word)}\b', '*' *
                       len(word), value, flags=re.IGNORECASE)
    return value
