"""
Just Facebook MCP Server

A Model Context Protocol (MCP) server for automating and managing
interactions on a Facebook Page using the Facebook Graph API.
"""

__version__ = "0.1.0"

from .server import main

__all__ = ["main", "__version__"]
