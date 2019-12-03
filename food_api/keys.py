#!/usr/bin/env python3
"""
This file will store some secret
information like keys and configuration info
"""
import os

EDAMAM_FOOD_DATABASE_API_KEY = os.getenv('EDAMAM_FOOD_DATABASE_API_KEY', 'Get your Own API Key!!!')
MYFRIDGE_APP_ID = os.getenv('MYFRIDGE_APP_ID', 'Get Your Own App Id')
