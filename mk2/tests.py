from database import delete_name, get_all_entries, insert_name
from engine import generate_name
from test_db import cleanup_test_db, setup_test_db
from test_helpers import (
  format_debug_pool,
  get_combined_double_pool,
  get_matching_pool,
  is_valid_format_any_result,
  get_any_format_pool,
  get_matching_pool_with_flags,
)


def run_tests():
  print("\n========================================")
  print(" 🧪 RUNNING AUTOMATED TEST SUITE        ")
  print("========================================")

  db = setup_test_db()
  passed = 0
  failed = 0

  def assert_test(
      condition, test_name, expected=None, actual=None, debug_pool=None
  ):
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

    if debug_pool is not None:
      print(f"     🔍 [Debug Pool Sample]: {format_debug_pool(debug_pool)}")

  # --- TEST 1: ADD TEST (Insertion check) ---
  initial_count = len(get_all_entries(db))
  insert_name("TestName", "first_name", "female", "human", "any", db_path=db)
  new_count = len(get_all_entries(db))
  assert_test(
    new_count == initial_count + 1, "Database correctly adds a new entry"
  )

  # --- TEST 2: DELETE TEST (Deletion check) ---
  entries = get_all_entries(db)
  target_id = entries[-1][0]
  deleted = delete_name(target_id, db_path=db)
  assert_test(deleted, "Database successfully deletes an entry by ID")

  # --- TEST 3: Generate first name with subspecies match ---
  cat, gender, slots = (
    "first_name",
    "female",
    [{"species": "insect", "sub_species": "spider"}],
  )
  generated_name = generate_name(cat, gender, slots, db_path=db)
  valid_pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
    generated_name in valid_pool,
    "Generate common first name for female insect spider",
    expected=f"One of {valid_pool}",
    actual=generated_name,
    debug_pool=valid_pool,
  )

  # --- TEST 4: Generate second name with subspecies match ---
  cat, gender, slots = (
    "second_name",
    "neutral",
    [{"species": "insect", "sub_species": "spider"}],
  )
  generated_second_name = generate_name(cat, gender, slots, db_path=db)
  valid_pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
    generated_second_name in valid_pool,
    "Generate common second name for neutral insect spider",
    expected=f"One of {valid_pool}",
    actual=generated_second_name,
    debug_pool=valid_pool,
  )

  # --- TEST 5: Generate full name with subspecies match ---
  cat, gender, slots = (
    "full_name",
    "female",
    [{"species": "insect", "sub_species": "mantis"}],
  )
  generated_full_name = generate_name(cat, gender, slots, db_path=db)
  valid_pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
    generated_full_name in valid_pool,
    "Generate common full name for female insect mantis",
    expected=f"One of {valid_pool}",
    actual=generated_full_name,
    debug_pool=valid_pool,
  )

  # ==========================================
  # NEW WILDCARD & GENDER TESTS
  # ==========================================
  wildcard_slot = [{"species": "any", "sub_species": "any"}]

  # Test 6: Generate any first name
  cat, gender, slots = "first_name", "any", wildcard_slot
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
    res in pool,
    "Generate any first name",
    expected=f"One of {pool}",
    actual=res,
    debug_pool=pool,
  )

  # Test 7: Generate any second name
  cat, gender, slots = "second_name", "any", wildcard_slot
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
    res in pool,
    "Generate any second name",
    expected=f"One of {pool}",
    actual=res,
    debug_pool=pool,
  )

  # Test 8: Generate any full name
  cat, gender, slots = "full_name", "any", wildcard_slot
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
    res in pool,
    "Generate any full name",
    expected=f"One of {pool}",
    actual=res,
    debug_pool=pool,
  )

  # Test 9: Generate any single name
  cat, gender, slots = "single_mode", "any", wildcard_slot
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, "first_name", gender, slots) + get_matching_pool(
    db, "second_name", gender, slots
  )
  assert_test(
    res in pool,
    "Generate any single name",
    expected=f"One of {pool}",
    actual=res,
    debug_pool=pool,
  )

  # Test 10: Generate any double name (Now showing fulls + first+second combinations!)
  cat, gender, slots = "double_mode", "any", wildcard_slot
  res = generate_name(cat, gender, slots, db_path=db)
  double_pool = get_combined_double_pool(db, gender, slots)
  assert_test(
    is_valid_format_any_result(db, gender, slots, res),
    "Generate any double name",
    expected="A valid double name combination",
    actual=res,
    debug_pool=double_pool,
  )

  # Test 11: Generate any format name (format = 'any')
  cat, gender, slots = "any", "any", wildcard_slot
  res = generate_name(cat, gender, slots, db_path=db)
  any_format_pool = get_any_format_pool(db, gender, slots)
  assert_test(
    is_valid_format_any_result(db, gender, slots, res),
    "Generate any format name (randomized mode)",
    expected="Any valid name format",
    actual=res,
    debug_pool=any_format_pool,
  )

  # Test 12: Generate any male name
  cat, gender, slots = "any", "male", wildcard_slot
  res = generate_name(cat, gender, slots, db_path=db)
  male_pool = get_matching_pool(db, "any", "male", slots)
  assert_test(
    is_valid_format_any_result(db, "male", slots, res),
    "Generate any male name",
    expected="A valid male-compatible name",
    actual=res,
    debug_pool=male_pool,
  )

  # Test 13: Generate any female name
  cat, gender, slots = "any", "female", wildcard_slot
  res = generate_name(cat, gender, slots, db_path=db)
  female_pool = get_matching_pool(db, "any", "female", slots)
  assert_test(
    is_valid_format_any_result(db, "female", slots, res),
    "Generate any female name",
    expected="A valid female-compatible name",
    actual=res,
    debug_pool=female_pool,
  )

  # Test 14: Generate any neutral name (universal mode)
  cat, gender, slots = "any", "neutral", wildcard_slot
  res = generate_name(cat, gender, slots, db_path=db)
  neutral_pool = get_matching_pool(db, "any", "neutral", slots)
  assert_test(
    is_valid_format_any_result(db, "neutral", slots, res),
    "Generate any neutral name (universal mode)",
    expected="Any valid name from the DB",
    actual=res,
    debug_pool=neutral_pool,
  )

  # ==========================================
  # NEW ELF & NEGATIVE TAXONOMY TESTS
  # ==========================================

  # Test 15: Generate any species name (species = 'any'), format single_mode
  cat, gender, slots = "single_mode", "any", [{"species": "any", "sub_species": "any"}]
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, "first_name", gender, slots) + get_matching_pool(db, "second_name", gender, slots)
  assert_test(res in pool, "Generate any species name (species='any')", expected=f"One of {pool}", actual=res, debug_pool=pool)

  # Test 16: Generate any subspecies name (subspecies = 'any') given a specific species, format single_mode (insects)
  cat, gender, slots = "single_mode", "any", [{"species": "insect", "sub_species": "any"}]
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, "first_name", gender, slots) + get_matching_pool(db, "second_name", gender, slots)
  assert_test(res in pool, "Generate any subspecies name for insect species", expected=f"One of {pool}", actual=res, debug_pool=pool)

  # Test 17: Generate specific species name, format single mode for elfs
  cat, gender, slots = "single_mode", "any", [{"species": "elf", "sub_species": "elf"}]
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, "first_name", gender, slots) + get_matching_pool(db, "second_name", gender, slots)
  assert_test(res in pool, "Generate specific species name single mode for elfs", expected=f"One of {pool}", actual=res, debug_pool=pool)

  # Test 18: Generate name given a specific species but a subspecies of another species (should return no match)
  cat, gender, slots = "single_mode", "any", [{"species": "elf", "sub_species": "spider"}]
  res = generate_name(cat, gender, slots, db_path=db)
  assert_test(res.startswith("⚠️"), "Mismatch taxonomy returns no match warning", expected="Warning starting with ⚠️", actual=res, debug_pool=get_matching_pool(db, cat, gender, slots))

  # Test 19: Generate name given a specific species with non-existent/mismatched subspecies
  cat, gender, slots = "single_mode", "any", [{"species": "elf", "sub_species": "nonexistent"}]
  res = generate_name(cat, gender, slots, db_path=db)
  assert_test(res.startswith("⚠️"), "Invalid subspecies returns no match warning", expected="Warning starting with ⚠️", actual=res, debug_pool=get_matching_pool(db, cat, gender, slots))

  # Test 20: Generate name given a specific species with subspecies with the same name as the species (elfs)
  cat, gender, slots = "first_name", "female", [{"species": "elf", "sub_species": "elf"}]
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, cat, gender, slots)
  assert_test(res in pool, "Generate female elf with elf subspecies first name (elf/elf match)", expected=f"One of {pool}", actual=res, debug_pool=pool)

# Test 21: Generate species-generic insect name (sub_species='any' matching broad category)
  cat, gender, slots = "single_mode", "any", [{"species": "insect", "sub_species": "any"}]
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
      res in pool, 
      "Generate species-generic insect name (sub_species='any')", 
      expected=f"One of {pool}", 
      actual=res, 
      debug_pool=pool
  )

# Test 21-b: Generate species-generic insect name (sub_species='insect' matching broad category)
  cat, gender, slots = "single_mode", "any", [{"species": "insect", "sub_species": "insect"}]
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, cat, gender, slots)
  assert_test(
      res in pool, 
      "Generate species-generic insect name (sub_species='insect')", 
      expected=f"One of {pool}", 
      actual=res, 
      debug_pool=pool
  )


# Test 22: Generate No Match Scenario (impossible filter combination)
  res = generate_name("first_name", "male", [{"species": "beastkin", "sub_species": "rabbit"}], db_path=db)
  assert_test(res.startswith("⚠️"), "No match scenario returns warning", expected="Warning starting with ⚠️", actual=res, debug_pool=get_matching_pool(db, "first_name", "male", [{"species": "beastkin", "sub_species": "rabbit"}]))

# Test 23: Generate Invalid Format Scenario (invalid format type)
  res = generate_name("invalid_format_type", "any", wildcard_slot, db_path=db)
  assert_test(
      res.startswith("⚠️"), 
      "Invalid format type returns warning", 
      expected="Warning starting with ⚠️", 
      actual=res,
      debug_pool=get_matching_pool(db, "invalid_format_type", "any", wildcard_slot)
  )

# --- CHECKBOX TIER TEST: Mantis with Global + Sub-species only (No Species-Generic) ---
  cat, gender, slots = "any", "any", [{"species": "insect", "sub_species": "mantis"}]
  
  # With allow_species_generic=False, "Beto" or "Besouro" (insect/insect) should be excluded, 
  # while "Louva Deusa" (insect/mantis) and "Anny" (any/any) should be allowed.
  res = generate_name(
      cat, gender, slots, 
      allow_global=True, 
      allow_species_generic=False, 
      allow_subspecies_specific=True, 
      db_path=db
  )
  
  # Compute expected pool with these exact flags
  allowed_pool = get_matching_pool_with_flags(
      db, cat, gender, slots, 
      allow_global=True, allow_species_generic=False, allow_subspecies_specific=True
  )
  
  assert_test(
      is_valid_format_any_result(db, gender, slots, res),
      "Mantis generation with Species-Generic disabled",
      expected="A valid name excluding broad insect-generic names",
      actual=res,
      debug_pool=allowed_pool
  )

  print("\n----------------------------------------")
  print(f"📊 Test Results: {passed} Passed, {failed} Failed.")
  print("========================================\n")

  cleanup_test_db()


if __name__ == "__main__":
  run_tests()