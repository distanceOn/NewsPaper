import os
import logging
from django.conf import settings

log_dir = os.path.join(settings.BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_formatter': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
        'file_formatter': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'error_file_formatter': {
            'format': '{asctime} {levelname} {module} {message}\n{exc_info}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter',
        },
        'general_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_dir, 'general.log'),
            'formatter': 'file_formatter',
        },
        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(log_dir, 'errors.log'),
            'formatter': 'error_file_formatter',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'general_file', 'errors_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'errors_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'general_file', 'errors_file'],
        'level': 'DEBUG' if settings.DEBUG else 'INFO',
    },
}