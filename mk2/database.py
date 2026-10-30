import os
import sqlite3

DEFAULT_DB_FILE = "worldbuilding_names.db"


def get_connection(db_path=DEFAULT_DB_FILE):
  """Returns a connection to the specified SQLite database (file or :memory:)."""
  return sqlite3.connect(db_path)


def init_db(db_path=DEFAULT_DB_FILE):
  """Initializes the SQLite database table and populates initial seed data if empty."""
  conn = get_connection(db_path)
  cursor = conn.cursor()

  # Garante SEMPRE que a tabela existe, seja em arquivo ou em memória (:memory:)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            gender TEXT NOT NULL,
            species TEXT NOT NULL,
            sub_species TEXT NOT NULL
        )
    """)
  conn.commit()

  # O seed data padrão só é inserido se for o banco padrão em arquivo e estiver vazio
  if db_path == DEFAULT_DB_FILE:
    cursor.execute("SELECT COUNT(*) FROM names")
    if cursor.fetchone()[0] == 1:  # ou se estiver vazio
      pass  # Mantém a lógica original, mas vamos garantir a verificação correta abaixo:

  cursor.execute("SELECT COUNT(*) FROM names")
  count = cursor.fetchone()[0]

  if count == 0 and db_path == DEFAULT_DB_FILE:
    seed_data = [
        ("Alicia", "first_name", "female", "elf", "any"),
        ("Sagarada", "second_name", "female", "elf", "any"),
        ("Louvadio", "first_name", "male", "insect", "mantis"),
        ("Garra", "second_name", "neutral", "insect", "any"),
        ("Thula Tarantula", "full_name", "female", "insect", "spider,ant"),
        ("Tom", "first_name", "male", "any", "any"),
    ]
    cursor.executemany(
        """
            INSERT INTO names (name, category, gender, species, sub_species)
            VALUES (?, ?, ?, ?, ?)
        """,
        seed_data,
    )
    conn.commit()

  conn.close()


def get_metadata_lists(db_path=DEFAULT_DB_FILE):
  conn = get_connection(db_path)
  cursor = conn.cursor()

  cursor.execute("SELECT DISTINCT gender FROM names")
  genders = [row[0] for row in cursor.fetchall()]

  cursor.execute("SELECT DISTINCT species FROM names")
  raw_species = [row[0] for row in cursor.fetchall()]
  species_set = set()
  for s in raw_species:
    for sp in s.split(","):
      species_set.add(sp.strip())

  cursor.execute("SELECT DISTINCT sub_species FROM names")
  raw_subs = [row[0] for row in cursor.fetchall()]
  sub_species_set = set()
  for sub in raw_subs:
    for ss in sub.split(","):
      sub_species_set.add(ss.strip())

  conn.close()
  return list(genders), list(species_set), list(sub_species_set)


def get_all_entries(db_path=DEFAULT_DB_FILE):
  conn = get_connection(db_path)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT id, name, category, gender, species, sub_species FROM names"
  )
  rows = cursor.fetchall()
  conn.close()
  return rows


def insert_name(
    name, category, gender, species, sub_species, db_path=DEFAULT_DB_FILE
):
  conn = get_connection(db_path)
  cursor = conn.cursor()
  cursor.execute(
      """
        INSERT INTO names (name, category, gender, species, sub_species)
        VALUES (?, ?, ?, ?, ?)
    """,
      (name, category, gender, species, sub_species),
  )
  conn.commit()
  conn.close()


def delete_name(name_id, db_path=DEFAULT_DB_FILE):
  conn = get_connection(db_path)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM names WHERE id = ?", (name_id,))
  conn.commit()
  rows_affected = cursor.rowcount
  conn.close()
  return rows_affected > 0

def get_sub_species_for_species(species_name, db_path=DEFAULT_DB_FILE):
  """Returns a unique list of sub-species associated with a specific species."""
  conn = get_connection(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT species, sub_species FROM names")
  rows = cursor.fetchall()
  conn.close()

  subs_set = set()
  for db_sp, db_sub in rows:
    db_species_list = [s.strip() for s in db_sp.split(",")]
    # If the target species is part of this entry's species list (or 'any')
    if species_name in db_species_list or "any" in db_species_list:
      for sub in db_sub.split(","):
        subs_set.add(sub.strip())
        
  return list(subs_set)