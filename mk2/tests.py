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
  test_counter = 0  # QoL: Automatic test number counter

  def assert_test(
      condition, test_name, expected=None, actual=None, debug_pool=None
  ):
    nonlocal passed, failed, test_counter
    test_counter += 1
    formatted_name = f"Test {test_counter}: {test_name}"
    
    if condition:
      print(f"  ✅ PASS: {formatted_name}")
      passed += 1
    else:
      print(f"  ❌ FAIL: {formatted_name}")
      if expected is not None and actual is not None:
        print(f"     🔸 Expected: {expected}")
        print(f"     🔸 Got:      {actual}")
      failed += 1

    if debug_pool is not None:
      print(f"     🔍 [Debug Pool Sample]: {format_debug_pool(debug_pool)}")

  wildcard_slot = [{"species": "any", "sub_species": "any"}]

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

  # --- TEST 3: Generate first name with subspecies only ---
  cat, gender, slots = "first_name", "female", [{"species": "insect", "sub_species": "spider"}]
  res = generate_name(
    cat, gender, slots, 
    allow_global=False, 
    allow_species_generic=False, 
    allow_subspecies_specific=True, 
    db_path=db
  )
  pool = get_matching_pool_with_flags(
    db, cat, gender, slots, 
    allow_global=False, allow_species_generic=False, allow_subspecies_specific=True
  )
  assert_test(res in pool, "Generate first name spider subspecies only", expected=f"One of {pool}", actual=res, debug_pool=pool)

# --- TEST 4: Generate second name with subspecies only ---
  cat, gender, slots = "second_name", "neutral", [{"species": "insect", "sub_species": "spider"}]
  res = generate_name(
    cat, gender, slots, 
    allow_global=False, 
    allow_species_generic=False, 
    allow_subspecies_specific=True, 
    db_path=db
  )
  pool = get_matching_pool_with_flags(
    db, cat, gender, slots, 
    allow_global=False, allow_species_generic=False, allow_subspecies_specific=True
  )
  assert_test(res in pool, "Generate second name spider subspecies only", expected=f"One of {pool}", actual=res, debug_pool=pool)

# --- TEST 5: Generate full name with subspecies only ---
  cat, gender, slots = "full_name", "female", [{"species": "insect", "sub_species": "mantis"}]
  res = generate_name(
    cat, gender, slots, 
    allow_global=False, 
    allow_species_generic=False, 
    allow_subspecies_specific=True, 
    db_path=db
  )
  pool = get_matching_pool_with_flags(
    db, cat, gender, slots, 
    allow_global=False, allow_species_generic=False, allow_subspecies_specific=True
  )
  assert_test(res in pool, "Generate full name mantis subspecies only", expected=f"One of {pool}", actual=res, debug_pool=pool)

  # --- TEST 6: Generate any first name ---
  cat, gender, slots = "first_name", "any", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots, 
    allow_global=True, 
    allow_species_generic=True, 
    allow_subspecies_specific=True, 
    db_path=db
  )
  pool = get_matching_pool_with_flags(
    db, cat, gender, slots, 
    allow_global=True, allow_species_generic=True, allow_subspecies_specific=True
  )
  assert_test(res in pool, "Generate any first name", expected=f"One of {pool}", actual=res, debug_pool=pool)

  # --- TEST 7: Generate any second name ---
  cat, gender, slots = "second_name", "any", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots, 
    allow_global=True, 
    allow_species_generic=True, 
    allow_subspecies_specific=True, 
    db_path=db
  )
  pool = get_matching_pool_with_flags(
    db, cat, gender, slots, 
    allow_global=True, allow_species_generic=True, allow_subspecies_specific=True
  )
  assert_test(res in pool, "Generate any second name", expected=f"One of {pool}", actual=res, debug_pool=pool)

  # --- TEST 8: Generate any full name ---
  cat, gender, slots = "full_name", "any", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots, 
    allow_global=True, 
    allow_species_generic=True, 
    allow_subspecies_specific=True, 
    db_path=db
  )
  pool = get_matching_pool_with_flags(
    db, cat, gender, slots, 
    allow_global=True, allow_species_generic=True, allow_subspecies_specific=True
  )
  assert_test(res in pool, "Generate any full name", expected=f"One of {pool}", actual=res, debug_pool=pool)

# --- TEST 9: Generate any single name ---
  cat, gender, slots = "single_mode", "any", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=True,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  pool = get_matching_pool_with_flags(
    db, "first_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True
  ) + get_matching_pool_with_flags(
    db, "second_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True
  )
  assert_test(
    res in pool,
    "Generate any single name",
    expected=f"One of {pool}",
    actual=res,
    debug_pool=pool,
  )

  # --- TEST 10: Generate any double name ---
  cat, gender, slots = "double_mode", "any", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=True,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  firsts = get_matching_pool_with_flags(db, "first_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  seconds = get_matching_pool_with_flags(db, "second_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  fulls = get_matching_pool_with_flags(db, "full_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  double_pool = fulls + [f"{f} {s}" for f in firsts for s in seconds]
  
  assert_test(
    is_valid_format_any_result(db, gender, slots, res),
    "Generate any double name",
    expected="A valid double name combination",
    actual=res,
    debug_pool=double_pool,
  )

  # --- TEST 11: Generate any format name (format = 'any') ---
  cat, gender, slots = "any", "any", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=True,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  firsts = get_matching_pool_with_flags(db, "first_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  seconds = get_matching_pool_with_flags(db, "second_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  fulls = get_matching_pool_with_flags(db, "full_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  any_format_pool = list(set(firsts + seconds + fulls + [f"{f} {s}" for f in firsts for s in seconds]))
  
  assert_test(
    is_valid_format_any_result(db, gender, slots, res),
    "Generate any format name (randomized mode)",
    expected="Any valid name format",
    actual=res,
    debug_pool=any_format_pool,
  )

# --- TEST 12: Generate any male name ---
  cat, gender, slots = "any", "male", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=True,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  firsts = get_matching_pool_with_flags(db, "first_name", "male", slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  seconds = get_matching_pool_with_flags(db, "second_name", "male", slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  fulls = get_matching_pool_with_flags(db, "full_name", "male", slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  male_pool = list(set(firsts + seconds + fulls + [f"{f} {s}" for f in firsts for s in seconds]))
  
  assert_test(
    is_valid_format_any_result(db, "male", slots, res),
    "Generate any male name",
    expected="A valid male-compatible name",
    actual=res,
    debug_pool=male_pool,
  )

  # --- TEST 13: Generate any female name ---
  cat, gender, slots = "any", "female", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=True,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  firsts = get_matching_pool_with_flags(db, "first_name", "female", slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  seconds = get_matching_pool_with_flags(db, "second_name", "female", slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  fulls = get_matching_pool_with_flags(db, "full_name", "female", slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  female_pool = list(set(firsts + seconds + fulls + [f"{f} {s}" for f in firsts for s in seconds]))
  
  assert_test(
    is_valid_format_any_result(db, "female", slots, res),
    "Generate any female name",
    expected="A valid female-compatible name",
    actual=res,
    debug_pool=female_pool,
  )

  # --- TEST 14: Generate any neutral name (universal mode) ---
  cat, gender, slots = "any", "neutral", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=True,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  firsts = get_matching_pool_with_flags(db, "first_name", "neutral", slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  seconds = get_matching_pool_with_flags(db, "second_name", "neutral", slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  fulls = get_matching_pool_with_flags(db, "full_name", "neutral", slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  neutral_pool = list(set(firsts + seconds + fulls + [f"{f} {s}" for f in firsts for s in seconds]))
  
  assert_test(
    is_valid_format_any_result(db, "neutral", slots, res),
    "Generate any neutral name (universal mode)",
    expected="Any valid name from the DB",
    actual=res,
    debug_pool=neutral_pool,
  )

# --- TEST 15: Generate any species single name (species = 'any'), format single_mode (excluding global) ---
  cat, gender, slots = "single_mode", "any", [{"species": "any", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=False,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  pool = (
    get_matching_pool_with_flags(db, "first_name", gender, slots, allow_global=False, allow_species_generic=True, allow_subspecies_specific=True) +
    get_matching_pool_with_flags(db, "second_name", gender, slots, allow_global=False, allow_species_generic=True, allow_subspecies_specific=True)
  )
  assert_test(
    res in pool,
    "Generate any species single name (species='any', no global)",
    expected=f"One of {pool}",
    actual=res,
    debug_pool=pool,
  )

  # --- TEST 16: Generate any subspecies single name (subspecies = 'any') given insect species (no global) ---
  cat, gender, slots = "single_mode", "any", [{"species": "insect", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=False,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  pool = (
    get_matching_pool_with_flags(db, "first_name", gender, slots, allow_global=False, allow_species_generic=True, allow_subspecies_specific=True) +
    get_matching_pool_with_flags(db, "second_name", gender, slots, allow_global=False, allow_species_generic=True, allow_subspecies_specific=True)
  )
  assert_test(
    res in pool,
    "Generate any subspecies single name for insect species (no global)",
    expected=f"One of {pool}",
    actual=res,
    debug_pool=pool,
  )

  # --- TEST 17: Generate any subspecies single name (subspecies = 'any') given insect species (with global) ---
  cat, gender, slots = "single_mode", "any", [{"species": "insect", "sub_species": "any"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=True,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  pool = (
      get_matching_pool_with_flags(db, "first_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True) +
      get_matching_pool_with_flags(db, "second_name", gender, slots, allow_global=True, allow_species_generic=True, allow_subspecies_specific=True)
  )
  assert_test(
      res in pool,
      "Generate any subspecies single name for insect species (with global)",
      expected=f"One of {pool}",
      actual=res,
      debug_pool=pool,
  )

# --- TEST 18: Generate specific species name, format single mode for elfs ---
  cat, gender, slots = "single_mode", "any", [{"species": "elf", "sub_species": "elf"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=False,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  pool = (
    get_matching_pool_with_flags(db, "first_name", gender, slots, allow_global=False, allow_species_generic=True, allow_subspecies_specific=True) +
    get_matching_pool_with_flags(db, "second_name", gender, slots, allow_global=False, allow_species_generic=True, allow_subspecies_specific=True)
  )
  assert_test(
    res in pool,
    "Generate specific species name single mode for elfs",
    expected=f"One of {pool}",
    actual=res,
    debug_pool=pool,
  )

  # ==========================================
  # CHECKBOX PERMUTATION TESTS FOR ELFS (8 Combinations)
  # ==========================================
  elf_slots = [{"species": "elf", "sub_species": "elf"}]

  permutations = [
    (True, True, True, "All Checkboxes ON"),
    (True, True, False, "Global=T, SpeciesGen=T, SubSpec=F"),
    (True, False, True, "Global=T, SpeciesGen=F, SubSpec=T"),
    (True, False, False, "Global=T, SpeciesGen=F, SubSpec=F (Only Global)"),
    (False, True, True, "Global=F, SpeciesGen=T, SubSpec=T"),
    (False, True, False, "Global=F, SpeciesGen=T, SubSpec=F"),
    (False, False, True, "Global=F, SpeciesGen=F, SubSpec=T"),
    (False, False, False, "All Checkboxes OFF (Expected: No Match)"),
  ]

  for g_flag, sg_flag, ss_flag, label in permutations:
    res = generate_name("single_mode", "any", elf_slots, allow_global=g_flag, allow_species_generic=sg_flag, allow_subspecies_specific=ss_flag, db_path=db)
    expected_pool = (
      get_matching_pool_with_flags(db, "first_name", "any", elf_slots, allow_global=g_flag, allow_species_generic=sg_flag, allow_subspecies_specific=ss_flag) +
      get_matching_pool_with_flags(db, "second_name", "any", elf_slots, allow_global=g_flag, allow_species_generic=sg_flag, allow_subspecies_specific=ss_flag)
    )
    
    if expected_pool:
      assert_test(
        res in expected_pool,
        f"Elf Checkbox Permutation -> {label}",
        expected=f"One of {expected_pool}",
        actual=res,
        debug_pool=expected_pool
      )
    else:
      assert_test(
        res.startswith("⚠️"),
        f"Elf Checkbox Permutation -> {label}",
        expected="Warning starting with ⚠️",
        actual=res,
        debug_pool=expected_pool
      )

  # --- TEST 27: Generate name given a specific species but a subspecies of another species (should return no match) ---
  cat, gender, slots = "single_mode", "any", [{"species": "elf", "sub_species": "spider"}]
  res = generate_name(
    cat, gender, slots,
    allow_global=False,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=db
  )
  assert_test(
    res.startswith("⚠️"),
    "Mismatch taxonomy returns no match warning",
    expected="Warning starting with ⚠️",
    actual=res,
    debug_pool=get_matching_pool_with_flags(db, cat, gender, slots, allow_global=False, allow_species_generic=True, allow_subspecies_specific=True)
  )

  # Test 20: Generate name given a specific species with non-existent/mismatched subspecies
  cat, gender, slots = "single_mode", "any", [{"species": "elf", "sub_species": "nonexistent"}]
  res = generate_name(cat, gender, slots, db_path=db)
  assert_test(res.startswith("⚠️"), "Invalid subspecies returns no match warning", expected="Warning starting with ⚠️", actual=res, debug_pool=get_matching_pool(db, cat, gender, slots))

  # Test 21: Generate name given a specific species with subspecies with the same name as the species (elfs)
  cat, gender, slots = "first_name", "female", [{"species": "elf", "sub_species": "elf"}]
  res = generate_name(cat, gender, slots, db_path=db)
  pool = get_matching_pool(db, cat, gender, slots)
  assert_test(res in pool, "Generate female elf with elf subspecies first name (elf/elf match)", expected=f"One of {pool}", actual=res, debug_pool=pool)

# Test 22: Generate species-generic insect name (sub_species='any' matching broad category)
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

# Test 23: Generate species-generic insect name (sub_species='insect' matching broad category)
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