"""
Instancia compartida de slowapi. Se importa en main.py para registrarla en
la app y en los routers que necesiten @limiter.limit(...).
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
