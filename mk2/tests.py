from database import delete_name, get_all_entries, insert_name
from engine import generate_name
from test_db import cleanup_test_db, setup_test_db
from test_helpers import format_debug_pool, get_matching_pool


def run_tests():
  print("\n========================================")
  print(" 🧪 RUNNING AUTOMATED TEST SUITE        ")
  print("========================================")

  db = setup_test_db()
  passed = 0
  failed = 0

  def assert_test(condition, test_name, expected=None, actual=None, debug_pool=None):
    nonlocal passed, failed
    if debug_pool is not None:
      print(f"     🔍 [Debug Pool Sample]: {format_debug_pool(debug_pool)}")

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

  # --- TEST 3: Generate first name with subspecies match ---
  cat, gender, slots = "first_name", "female", [{"species": "insect", "sub_species": "spider"}]
  generated_name = generate_name(cat, gender, slots, db_path=db)
  valid_pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
      generated_name in valid_pool, 
      "Generate common first name for female insect spider",
      expected=f"One of {valid_pool}",
      actual=generated_name,
      debug_pool=valid_pool
  )

  # --- TEST 4: Generate second name with subspecies match ---
  cat, gender, slots = "second_name", "neutral", [{"species": "insect", "sub_species": "spider"}]
  generated_second_name = generate_name(cat, gender, slots, db_path=db)
  valid_pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
      generated_second_name in valid_pool, 
      "Generate common second name for neutral insect spider",
      expected=f"One of {valid_pool}",
      actual=generated_second_name,
      debug_pool=valid_pool
  )

  # --- TEST 5: Generate full name with subspecies match ---
  cat, gender, slots = "full_name", "female", [{"species": "insect", "sub_species": "mantis"}]
  generated_full_name = generate_name(cat, gender, slots, db_path=db)
  valid_pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
      generated_full_name in valid_pool, 
      "Generate common full name for female insect mantis",
      expected=f"One of {valid_pool}",
      actual=generated_full_name,
      debug_pool=valid_pool
  )

  print("\n----------------------------------------")
  print(f"📊 Test Results: {passed} Passed, {failed} Failed.")
  print("========================================\n")

  cleanup_test_db()


if __name__ == "__main__":
  run_tests()