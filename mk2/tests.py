import sqlite3
from database import delete_name, get_all_entries, init_db, insert_name
from engine import generate_name_with_db


def setup_test_db():
  """Sets up an isolated in-memory SQLite database with controlled test data."""
  test_db = ":memory:"
  init_db(test_db)

  # Insert precise test fixtures
  insert_name(
      "Legolas", "first_name", "male", "elf", "any", db_path=test_db
  )  # Elf
  insert_name(
      "Boran", "first_name", "male", "insect", "mantis", db_path=test_db
  )  # Insect
  insert_name(
      "UniversalHero",
      "first_name",
      "neutral",
      "any",
      "any",
      db_path=test_db,
  )  # Universal

  return test_db


def run_tests():
  print("\n========================================")
  print(" 🧪 RUNNING AUTOMATED TEST SUITE        ")
  print("========================================")

  db = setup_test_db()
  passed = 0
  failed = 0

  def assert_test(condition, test_name):
    nonlocal passed, failed
    if condition:
      print(f"  ✅ PASS: {test_name}")
      passed += 1
    else:
      print(f"  ❌ FAIL: {test_name}")
      failed += 1

  # --- TEST 1: ADD TEST (Insertion check) ---
  initial_count = len(get_all_entries(db))
  insert_name(
      "TestName", "first_name", "female", "human", "any", db_path=db
  )
  new_count = len(get_all_entries(db))
  assert_test(
      new_count == initial_count + 1, "Database correctly adds a new entry"
  )

  # --- TEST 2: DELETE TEST (Deletion check) ---
  entries = get_all_entries(db)
  target_id = entries[-1][0]  # get ID of the last inserted test name
  deleted = delete_name(target_id, db_path=db)
  assert_test(deleted, "Database successfully deletes an entry by ID")

  # --- TEST 3: RETRIEVE / POSITIVE TEST ---
  # Asking for an elf name should find 'Legolas'
  elf_slot = [{"species": "elf", "sub_species": "any"}]
  result = generate_name_with_db("single", "male", elf_slot, db_path=db)
  assert_test(
      result == "Legolas",
      "Correctly retrieves a valid Elf name for an Elf request",
  )

  # --- TEST 4: NEGATIVE TEST (Species isolation) ---
  # Asking for an insect should NOT return an elf name (Legolas)
  insect_slot = [{"species": "insect", "sub_species": "mantis"}]
  # Run multiple times or check result logic
  result_insect = generate_name_with_db(
      "single", "male", insect_slot, db_path=db
  )
  assert_test(
      result_insect != "Legolas",
      "Negative Test: Elf names do not leak into Insect-only requests",
  )

  # --- TEST 5: UNIVERSAL WILDCARD TEST (`any`) ---
  # Universal names should appear for both elves and insects
  universal_slot = [{"species": "dwarf", "sub_species": "any"}]
  result_univ = generate_name_with_db("single", "neutral", universal_slot, db_path=db)
  assert_test(
      result_univ == "UniversalHero",
      "Universal wildcard (any/any) matches unknown species requests",
  )

  print("\n----------------------------------------")
  print(f"📊 Test Results: {passed} Passed, {failed} Failed.")
  print("========================================\n")


if __name__ == "__main__":
  run_tests()