import os
from database import delete_name, get_all_entries, init_db, insert_name
from engine import generate_name_with_db

TEST_DB_FILE = "test_names.db"


def setup_test_db():
  """Sets up an isolated test database file, wiping any previous test runs."""
  if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)

  init_db(TEST_DB_FILE)

  # Insert precise test fixtures
  insert_name("Legolas", "first_name", "male", "elf", "any", db_path=TEST_DB_FILE)
  insert_name("Boran", "first_name", "male", "insect", "mantis", db_path=TEST_DB_FILE)
  insert_name("UniversalHero", "first_name", "neutral", "any", "any", db_path=TEST_DB_FILE)

  return TEST_DB_FILE


def run_tests():
  print("\n========================================")
  print(" 🧪 RUNNING AUTOMATED TEST SUITE        ")
  print("========================================")

  db = setup_test_db()
  passed = 0
  failed = 0

  def assert_test(condition, test_name, expected=None, actual=None):
    nonlocal passed, failed
    if condition:
      print(f"  ✅ PASS: {test_name}")
      passed += 1
    else:
      print(f"  ❌ FAIL: {test_name}")
      if expected is not None and actual is not None:
        print(f"     🔸 Expected: {expected}")
        print(f"     🔸 Got:      {actual}")
      failed += 1

  # --- TEST 1: ADD TEST (Insertion check) ---
  initial_count = len(get_all_entries(db))
  insert_name("TestName", "first_name", "female", "human", "any", db_path=db)
  new_count = len(get_all_entries(db))
  assert_test(new_count == initial_count + 1, "Database correctly adds a new entry")

  # --- TEST 2: DELETE TEST (Deletion check) ---
  entries = get_all_entries(db)
  target_id = entries[-1][0]
  deleted = delete_name(target_id, db_path=db)
  assert_test(deleted, "Database successfully deletes an entry by ID")

  # --- TEST 3: RETRIEVE / POSITIVE TEST ---
  # Elves can match "Legolas" or universal names like "UniversalHero" due to 'any'
  elf_slot = [{"species": "elf", "sub_species": "any"}]
  result = generate_name_with_db("single", "male", elf_slot, db_path=db)
  valid_expected = ["Legolas", "UniversalHero"]
  assert_test(
      result in valid_expected,
      "Correctly retrieves a valid Elf-compatible name",
      expected=f"One of {valid_expected}",
      actual=result
  )

  # --- TEST 4: NEGATIVE TEST (Species isolation) ---
  # Asking strictly for an insect sub-species should NOT return an elf-exclusive name like "Legolas"
  insect_slot = [{"species": "insect", "sub_species": "mantis"}]
  result_insect = generate_name_with_db("single", "male", insect_slot, db_path=db)
  # UniversalHero has 'any' so it could appear, but "Legolas" (species: elf) must NEVER appear here.
  assert_test(
      result_insect != "Legolas",
      "Negative Test: Elf-exclusive names do not leak into strict Insect requests",
      expected="Anything except 'Legolas'",
      actual=result_insect
  )

  # --- TEST 5: UNIVERSAL WILDCARD TEST (`any`) ---
  universal_slot = [{"species": "dwarf", "sub_species": "any"}]
  result_univ = generate_name_with_db("single", "neutral", universal_slot, db_path=db)
  assert_test(
      result_univ == "UniversalHero",
      "Universal wildcard (any/any) matches unknown species requests",
      expected="UniversalHero",
      actual=result_univ
  )

  print("\n----------------------------------------")
  print(f"📊 Test Results: {passed} Passed, {failed} Failed.")
  print("========================================\n")

  if os.path.exists(TEST_DB_FILE):
    os.remove(TEST_DB_FILE)


if __name__ == "__main__":
  run_tests()