"""Neo4j driver singleton — process boyunca tek driver instance.

Neden singleton: her call'da yeni driver açmak connection pool'u boşa harcar.
Anthropic SDK / SQLAlchemy engine ile aynı pattern.
"""
from neo4j import GraphDatabase, Driver
from . import config

_driver: Driver | None = None

def get_driver() -> Driver:
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            config.NEO4J_URI,
            auth=(config.NEO4J_USER, config.NEO4J_PASSWORD),
        )
    return _driver

def close_driver():
    """Test / shutdown için."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None