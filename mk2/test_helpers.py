import random
import sqlite3
from engine import matches_taxonomy


def get_matching_pool(db_path, category, gender, user_slots):
  """Dynamically computes all valid names in the DB that match the given criteria."""
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT name, category, gender, species, sub_species FROM names")
  rows = cursor.fetchall()
  conn.close()

  # Map engine modes or wildcards to valid DB categories
  if category == "single_mode":
    target_categories = ["first_name", "second_name"]
  elif category == "any":
    target_categories = ["first_name", "second_name", "full_name"]
  else:
    target_categories = [category]

  pool = []
  for name, cat, g, sp, sub in rows:
    if cat not in target_categories:
      continue
    
    gender_match = (
        gender.lower() in ["any", "neutral"] or
        g.lower() in ["any", "neutral"] or
        g.lower() == gender.lower()
    )
    if not gender_match:
      continue
    
    db_sp_list = [s.strip() for s in sp.split(",")]
    db_sub_list = [s.strip() for s in sub.split(",")]
    if matches_taxonomy(db_sp_list, db_sub_list, user_slots):
      pool.append(name)
      
  return pool


def get_combined_double_pool(db_path, gender, user_slots):
  """Computes all valid double-name options (Full names + First+Second combinations)."""
  fulls = get_matching_pool(db_path, "full_name", gender, user_slots)
  firsts = get_matching_pool(db_path, "first_name", gender, user_slots)
  seconds = get_matching_pool(db_path, "second_name", gender, user_slots)
  
  combinations = [f"{f} {s}" for f in firsts for s in seconds]
  return fulls + combinations


def is_valid_format_any_result(db_path, gender, user_slots, result_name):
  """Validates that a result from format='any' is a legal single, full, or combined name."""
  firsts = get_matching_pool(db_path, "first_name", gender, user_slots)
  seconds = get_matching_pool(db_path, "second_name", gender, user_slots)
  fulls = get_matching_pool(db_path, "full_name", gender, user_slots)

  if result_name in firsts or result_name in seconds or result_name in fulls:
    return True

  parts = result_name.split(" ", 1)
  if len(parts) == 2:
    if parts[0] in firsts and parts[1] in seconds:
      return True

  return False


def format_debug_pool(pool):
  """Returns a randomized sample of up to 10 matching names for deep test debugging."""
  sample_pool = list(pool)
  random.shuffle(sample_pool)
  capped = sample_pool[:10]
  return f"{capped} (Total matching entries found: {len(pool)})"

def get_any_format_pool(db_path, gender, user_slots):
  """Computes every possible unique output (single names + double names + combinations) for format='any'."""
  firsts = get_matching_pool(db_path, "first_name", gender, user_slots)
  seconds = get_matching_pool(db_path, "second_name", gender, user_slots)
  fulls = get_matching_pool(db_path, "full_name", gender, user_slots)
  combinations = [f"{f} {s}" for f in firsts for s in seconds]
  
  # Return unique set of all possible generation outcomes
  return list(set(firsts + seconds + fulls + combinations))

def get_matching_pool_with_flags(
    db_path,
    category,
    gender,
    user_slots,
    allow_global=True,
    allow_species_generic=True,
    allow_subspecies_specific=True,
):
  """Computes valid names respecting individual checkbox inclusion flags (tiers)."""
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT name, category, gender, species, sub_species FROM names")
  rows = cursor.fetchall()
  conn.close()

  if category == "single_mode":
    target_categories = ["first_name", "second_name"]
  elif category == "any":
    target_categories = ["first_name", "second_name", "full_name"]
  else:
    target_categories = [category]

  pool = []
  for name, cat, g, sp, sub in rows:
    if cat not in target_categories:
      continue

    gender_match = (
        gender.lower() in ["any", "neutral"]
        or g.lower() in ["any", "neutral"]
        or g.lower() == gender.lower()
    )
    if not gender_match:
      continue

    db_species_list = [s.strip() for s in sp.split(",")]
    db_subs_list = [s.strip() for s in sub.split(",")]

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
      pool.append(name)

  return pool