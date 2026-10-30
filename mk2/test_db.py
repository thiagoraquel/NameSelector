import os
from database import init_db, insert_name

TEST_DB_FILE = "test_names.db"


def setup_test_db():
  """Sets up an isolated test database file, wiping any previous test runs."""
  if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

  init_db(TEST_DB_FILE)

  # Insert precise test fixtures (including the new entries)
  insert_name("Aranya", "first_name", "female", "insect", "spider", db_path=TEST_DB_FILE)
  insert_name("Spider", "second_name", "neutral", "insect", "spider", db_path=TEST_DB_FILE)
  insert_name("Louva Deusa", "full_name", "female", "insect", "mantis", db_path=TEST_DB_FILE)
  insert_name("Ferin", "first_name", "female", "beastkin", "wolf", db_path=TEST_DB_FILE)
  insert_name("Lobato", "second_name", "neutral", "beastkin", "wolf", db_path=TEST_DB_FILE)
  insert_name("Hopper Coelho", "full_name", "male", "beastkin", "rabbit", db_path=TEST_DB_FILE)

  return TEST_DB_FILE


def cleanup_test_db():
  """Wipes the test database file after tests finish."""
  if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)