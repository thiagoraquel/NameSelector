import os
from database import init_db, insert_name

TEST_DB_FILE = "test_names.db"


def setup_test_db():
  """Sets up an isolated test database file, wiping any previous test runs."""
  if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

  init_db(TEST_DB_FILE)

  # Original fixtures
  insert_name("Aranya", "first_name", "female", "insect", "spider", db_path=TEST_DB_FILE)
  insert_name("Spider", "second_name", "neutral", "insect", "spider", db_path=TEST_DB_FILE)
  insert_name("Louva Deusa", "full_name", "female", "insect", "mantis", db_path=TEST_DB_FILE)
  insert_name("Rinoceronte", "second_name", "male", "insect", "rhino beetle", db_path=TEST_DB_FILE)
  insert_name("Ferin", "first_name", "female", "beastkin", "wolf", db_path=TEST_DB_FILE)
  insert_name("Lobato", "second_name", "neutral", "beastkin", "wolf", db_path=TEST_DB_FILE)
  insert_name("Hopper Coelho", "full_name", "male", "beastkin", "rabbit", db_path=TEST_DB_FILE)
  insert_name("Elfcel", "first_name", "female", "elf", "elf", db_path=TEST_DB_FILE)
  insert_name("Incelf", "second_name", "female", "elf", "elf", db_path=TEST_DB_FILE)
  insert_name("Zéfiro Luscofusco", "full_name", "male", "elf", "elf", db_path=TEST_DB_FILE)

  # New explicit tier entries
  insert_name("Beto", "first_name", "male", "insect", "insect", db_path=TEST_DB_FILE)
  insert_name("Besouro", "second_name", "neutral", "insect", "insect", db_path=TEST_DB_FILE)
  insert_name("Anny", "first_name", "neutral", "any", "any", db_path=TEST_DB_FILE)

  return TEST_DB_FILE


def cleanup_test_db():
  """Wipes the test database file after tests finish."""
  if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)