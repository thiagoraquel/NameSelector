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

  pool = []
  for name, cat, g, sp, sub in rows:
    if cat != category:
      continue
    gender_match = (g == gender or g == "neutral" or g == "any" or gender == "any")
    if not gender_match:
      continue
    
    db_sp_list = [s.strip() for s in sp.split(",")]
    db_sub_list = [s.strip() for s in sub.split(",")]
    if matches_taxonomy(db_sp_list, db_sub_list, user_slots):
      pool.append(name)
      
  return pool


def format_debug_pool(pool):
  """Returns a randomized sample of up to 10 matching names for deep test debugging."""
  sample_pool = list(pool)
  random.shuffle(sample_pool)
  capped = sample_pool[:10]
  return f"{capped} (Total matching entries found: {len(pool)})"