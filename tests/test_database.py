import pytest

from app.database import Database

def test_database():
    db = Database()
    assert db.get_connection() is not None