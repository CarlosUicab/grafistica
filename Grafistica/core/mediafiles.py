# -*- coding: utf-8 -*-
import os
from .json_reader import json_settings

settings = json_settings()

__PATH_MEDIA = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(__PATH_MEDIA, '../media/')
MEDIA_URL = '/media/'

