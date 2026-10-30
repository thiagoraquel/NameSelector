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

  # Test 8: Generate common name with no species matches
  generated_no_match = generate_name_with_db("single", "male", [{"species": "void", "sub_species": "any"}], db_path=db)
  assert_test(generated_no_match is None, "Generate common name with no species matches")

  # Test 9: Generate common name with no species matches and no subspecies matches
  generated_no_match = generate_name_with_db("single", "male", [{"species": "void", "sub_species": "void"}], db_path=db)
  assert_test(generated_no_match is None, "Generate common name with no species matches and no subspecies matches")


  #insert_name("Beto", "first_name", "male", "insect", "rhino beetle", db_path=TEST_DB_FILE)
  #insert_name("Besouro", "second_name", "neutral", "insect", "any", db_path=TEST_DB_FILE)