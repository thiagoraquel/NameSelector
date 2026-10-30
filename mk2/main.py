from cli import (
    add_name_cli,
    delete_name_cli,
    generate_cli,
    view_all_entries_cli,
)
from database import get_metadata_lists, init_db
from tests import run_tests


def main():
  init_db()
  while True:
    print("========================================")
    print(" 🏷️  WORLDBUILDING NAME TOOL (Modular)  ")
    print("========================================")
    print("1. Generate Name")
    print("2. Add New Name")
    print("3. Delete a Name")
    print("4. View All Database Entries")
    print("5. View Metadata Stats")
    print("6. Run Automated Test Suite")
    print("7. Exit")

    choice = input("Select an option (1-7): ").strip()

    if choice == "1":
      generate_cli()
    elif choice == "2":
      add_name_cli()
    elif choice == "3":
      delete_name_cli()
    elif choice == "4":
      view_all_entries_cli()
    elif choice == "5":
      genders, species, subs = get_metadata_lists()
      print(f"\n📊 **Current DB Metadata Index**:")
      print(f"  • Known Genders: {genders}")
      print(f"  • Known Species: {species}")
      print(f"  • Known Sub-species: {subs}\n")
    elif choice == "6":
      run_tests()
    elif choice == "7":
      print("Exiting. Keep building worlds!")
      break
    else:
      print("❌ Invalid option. Try again.")


if __name__ == "__main__":
  main()