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

  # Neutral and Any act as universal/asexual categories returning all names
  if gender.lower() in ["any", "neutral"]:
    gender_condition = "1=1"
  else:
    gender_condition = (
        f"(gender = '{gender}' OR gender = 'neutral' OR gender = 'any')"
    )

  query = f"SELECT id, name, category, gender, species, sub_species FROM names WHERE {gender_condition}"
  cursor.execute(query)
  all_entries = cursor.fetchall()
  conn.close()

  valid_entries = []

  for entry_id, name, category, entry_gender, db_species, db_subs in all_entries:
    db_species_list = [s.strip() for s in db_species.split(",")]
    db_subs_list = [s.strip() for s in db_subs.split(",")]

    is_global = "any" in db_species_list and "any" in db_subs_list

    is_species_generic = False
    if not is_global:
      for ds in db_species_list:
        if (ds in db_subs_list and ds != "any") or ("any" in db_subs_list and ds != "any"):
          for slot in user_slots:
            if slot["species"] == ds or slot["species"] == "any":
              # Sub-species must be "any" or match the species macro-family
              if slot["sub_species"] == "any" or slot["sub_species"] == ds:
                is_species_generic = True
                break
        if is_species_generic:
          break

    is_subspecies_specific = False
    if not is_global and not is_species_generic:
      if matches_taxonomy(db_species_list, db_subs_list, user_slots):
        is_subspecies_specific = True

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

  first_pool = [e for e in valid_entries if e["category"] == "first_name"]
  second_pool = [e for e in valid_entries if e["category"] == "second_name"]
  full_pool = [e for e in valid_entries if e["category"] == "full_name"]

  # If format is "any", randomly choose among formats that have matching names
  if format_type == "any":
    available_modes = []
    if first_pool:
      available_modes.append("first_name")
    if second_pool:
      available_modes.append("second_name")
    if full_pool:
      available_modes.append("full_name")
    if first_pool or second_pool:
      available_modes.append("single_mode")
    if (first_pool and second_pool) or full_pool:
      available_modes.append("double_mode")

    if not available_modes:
      return "⚠️ No matching names found for these criteria."
    format_type = random.choice(available_modes)

  # --- SELECTION LOGIC ---
  if format_type == "first_name":
    if not first_pool:
      return "⚠️ No matching First Name found for these criteria."
    return random.choice(first_pool)["name"]

  elif format_type == "second_name":
    if not second_pool:
      return "⚠️ No matching Second Name found for these criteria."
    return random.choice(second_pool)["name"]

  elif format_type == "full_name":
    if not full_pool:
      return "⚠️ No matching Full Name found for these criteria."
    return random.choice(full_pool)["name"]

  elif format_type == "single_mode":
    single_pool = first_pool + second_pool
    if not single_pool:
      return "⚠️ No matching single names found for these criteria."
    return random.choice(single_pool)["name"]

  elif format_type == "double_mode":
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