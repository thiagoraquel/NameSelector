from database import delete_name, get_all_entries, get_metadata_lists, insert_name
from engine import generate_name
from tests import run_tests


def prompt_choice(prompt_text, options):
  print(prompt_text)
  for idx, opt in enumerate(options, 1):
    print(f"  {idx}. {opt.capitalize()}")
  while True:
    try:
      choice = int(input("Select option number: ").strip())
      if 1 <= choice <= len(options):
        return options[choice - 1]
    except ValueError:
      pass
    print("❌ Invalid input. Please enter a valid number from the list.")


def add_name_cli():
  print("\n--- Add a New Name ---")
  name = input("Enter name: ").strip()

  categories = ["first_name", "second_name", "full_name"]
  category = prompt_choice("Select Category:", categories)

  genders, _, _ = get_metadata_lists()
  gender_options = list(dict.fromkeys(genders + ["neutral", "any"]))
  gender = prompt_choice("Select Gender:", gender_options)

  species = input(
      "Enter Species (comma-separated if multiple, e.g. insect or"
      " insect,spider. Type 'any'): "
  ).strip().lower()
  sub_species = input(
      "Enter Sub-species (comma-separated if multiple, e.g. mantis or"
      " spider,ant. Type 'any'): "
  ).strip().lower()

  insert_name(name, category, gender, species, sub_species)
  print(f"✅ Successfully added '{name}' to the database!")


def delete_name_cli():
  print("\n--- Delete a Name ---")
  rows = get_all_entries()
  if not rows:
    print("Database is empty. Nothing to delete.")
    return

  view_all_entries_cli()
  try:
    name_id = int(
        input("Enter the ID of the name you want to delete (or 0 to cancel): ")
        .strip()
    )
    if name_id == 0:
      return
    success = delete_name(name_id)
    if success:
      print(f"🗑️ Successfully deleted entry with ID {name_id}.")
    else:
      print(f"❌ No entry found with ID {name_id}.")
  except ValueError:
    print("❌ Invalid ID format. Please enter a number.")


def view_all_entries_cli():
  print("\n--- 📚 All Database Entries ---")
  rows = get_all_entries()
  if not rows:
    print("Database is empty.")
    return

  print(
      f"{'ID':<4} | {'Name':<20} | {'Category':<12} | {'Gender':<8} |"
      f" {'Species':<15} | {'Sub-species':<15}"
  )
  print("-" * 85)
  for r in rows:
    print(
        f"{r[0]:<4} | {r[1]:<20} | {r[2]:<12} | {r[3]:<8} | {r[4]:<15} |"
        f" {r[5]:<15}"
    )
  print("-" * 85)


def generate_cli():
  print("\n--- Generate a Name ---")
  formats = ["single", "double"]
  format_type = prompt_choice("Select Format:", formats)

  genders, _, _ = get_metadata_lists()
  gender = prompt_choice("Select Gender Target:", genders + ["any"])

  ind_types = ["common", "hybrid"]
  ind_type = prompt_choice("Select Individual Type:", ind_types)

  user_slots = []
  if ind_type == "hybrid":
    print("\nConfiguring Hybrid (2 slots):")
    for i in range(1, 3):
      sp = input(f"  Slot {i} Species: ").strip().lower()
      sub_sp = input(f"  Slot {i} Sub-species: ").strip().lower()
      user_slots.append({"species": sp, "sub_species": sub_sp})
  else:
    sp = input("Species: ").strip().lower()
    sub_sp = input("Sub-species: ").strip().lower()
    user_slots.append({"species": sp, "sub_species": sub_sp})

  result = generate_name(format_type, gender, user_slots)
  print(f"\n✨ Generated Name: **{result}**\n")