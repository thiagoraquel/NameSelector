import random
from database import DEFAULT_DB_FILE, get_connection


def generate_name(
    format_type,
    gender,
    user_slots,
    allow_global=True,
    allow_species_generic=True,
    allow_subspecies_specific=True,
    db_path=DEFAULT_DB_FILE,
):
  conn = get_connection(db_path)
  cursor = conn.cursor()

  gender_condition = (
      f"(gender = '{gender}' OR gender = 'neutral' OR gender = 'any')"
  )
  query = f"SELECT id, name, category, species, sub_species FROM names WHERE {gender_condition}"
  cursor.execute(query)
  all_entries = cursor.fetchall()
  conn.close()

  valid_entries = []

  for entry_id, name, category, db_species, db_subs in all_entries:
    db_species_list = [s.strip() for s in db_species.split(",")]
    db_subs_list = [s.strip() for s in db_subs.split(",")]

    # Classify entry into inheritance tiers based on user slots
    is_global = "any" in db_species_list and "any" in db_subs_list

    is_species_generic = False
    if not is_global and "any" in db_subs_list:
      for ds in db_species_list:
        if ds == "any" or any(
            slot["species"] == ds or slot["species"] == "any"
            for slot in user_slots
        ):
          is_species_generic = True
          break

    is_subspecies_specific = False
    if not is_global and not is_species_generic:
      if matches_taxonomy(db_species_list, db_subs_list, user_slots):
        is_subspecies_specific = True

    # Apply user checkbox tier filters
    if is_global and not allow_global:
      continue
    if is_species_generic and not allow_species_generic:
      continue
    if is_subspecies_specific and not allow_subspecies_specific:
      continue

    if is_global or is_species_generic or is_subspecies_specific:
      if is_global or is_species_generic or matches_taxonomy(
          db_species_list, db_subs_list, user_slots
      ):
        valid_entries.append({"name": name, "category": category})

  # --- SELECTION LOGIC BASED ON THE 5 FORMAT TYPES ---
  if format_type == "first_name":
    pool = [e for e in valid_entries if e["category"] == "first_name"]
    if not pool:
      return "⚠️ No matching First Name found for these criteria."
    return random.choice(pool)["name"]

  elif format_type == "second_name":
    pool = [e for e in valid_entries if e["category"] == "second_name"]
    if not pool:
      return "⚠️ No matching Second Name found for these criteria."
    return random.choice(pool)["name"]

  elif format_type == "full_name":
    pool = [e for e in valid_entries if e["category"] == "full_name"]
    if not pool:
      return "⚠️ No matching Full Name found for these criteria."
    return random.choice(pool)["name"]

  elif format_type == "single_mode":
    pool = [
        e
        for e in valid_entries
        if e["category"] in ["first_name", "second_name"]
    ]
    if not pool:
      return "⚠️ No matching single names found for these criteria."
    return random.choice(pool)["name"]

  elif format_type == "double_mode":
    first_pool = [e for e in valid_entries if e["category"] == "first_name"]
    second_pool = [e for e in valid_entries if e["category"] == "second_name"]
    full_pool = [e for e in valid_entries if e["category"] == "full_name"]

    choices = []
    if first_pool and second_pool:
      choices.append("combination")
    if full_pool:
      choices.append("full_atomic")

    if not choices:
      return "⚠️ No matching double name format found for these criteria."

    chosen_path = random.choice(choices)
    if chosen_path == "combination":
      f = random.choice(first_pool)["name"]
      s = random.choice(second_pool)["name"]
      return f"{f} {s}"
    else:
      return random.choice(full_pool)["name"]

  return "⚠️ Invalid format type selected."


def matches_taxonomy(db_species_list, db_subs_list, user_slots):
  for ds in db_species_list:
    if ds == "any":
      continue
    matched = any(
        slot["species"] == ds or slot["species"] == "any" for slot in user_slots
    )
    if not matched:
      return False

  for dss in db_subs_list:
    if dss == "any":
      continue
    matched = any(
        slot["sub_species"] == dss or slot["sub_species"] == "any"
        for slot in user_slots
    )
    if not matched:
      return False

  return True