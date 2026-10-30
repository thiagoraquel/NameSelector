import random
from database import DEFAULT_DB_FILE, get_connection


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


def generate_name(format_type, gender, user_slots):
  return generate_name_with_db(format_type, gender, user_slots, DEFAULT_DB_FILE)


def generate_name_with_db(format_type, gender, user_slots, db_path):
  conn = get_connection(db_path)
  cursor = conn.cursor()

  gender_condition = f"(gender = '{gender}' OR gender = 'neutral' OR gender = 'any')"
  query = f"SELECT name, category, species, sub_species FROM names WHERE {gender_condition}"
  cursor.execute(query)
  all_entries = cursor.fetchall()
  conn.close()

  valid_entries = []
  for name, category, db_species, db_subs in all_entries:
    db_species_list = [s.strip() for s in db_species.split(",")]
    db_subs_list = [s.strip() for s in db_subs.split(",")]

    if matches_taxonomy(db_species_list, db_subs_list, user_slots):
      valid_entries.append({"name": name, "category": category})

  if format_type == "single":
    pool = [e for e in valid_entries if e["category"] == "first_name"]
    if not pool:
      return "⚠️ No matching single name found for these criteria."
    return random.choice(pool)["name"]

  elif format_type == "double":
    first_pool = [e for e in valid_entries if e["category"] == "first_name"]
    second_pool = [e for e in valid_entries if e["category"] == "second_name"]
    full_pool = [e for e in valid_entries if e["category"] == "full_name"]

    choices = []
    if first_pool and second_pool:
      choices.append("combination")
    if full_pool:
      choices.append("full_atomic")

    if not choices:
      return "⚠️ No matching double name found for these criteria."

    chosen_path = random.choice(choices)
    if chosen_path == "combination":
      f = random.choice(first_pool)["name"]
      s = random.choice(second_pool)["name"]
      return f"{f} {s}"
    else:
      return random.choice(full_pool)["name"]