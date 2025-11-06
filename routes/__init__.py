"""
Módulo de rotas da aplicação.
"""
from flask import Blueprint
from .api_routes import api_bp
from .web_routes import web_bp

__all__ = ['api_bp', 'web_bp']
