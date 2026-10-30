import tkinter as tk
from tkinter import messagebox, ttk
from database import (
    delete_name,
    get_all_entries,
    get_metadata_lists,
    get_sub_species_for_species,
    init_db,
    insert_name,
)
from engine import generate_name


class WorldbuildingGUI:

  def __init__(self, root):
    self.root = root
    self.root.title("🏷️ Worldbuilding Name Selector (GUI)")
    self.root.geometry("700x740")
    self.root.minsize(650, 680)

    init_db()

    self.notebook = ttk.Notebook(root)
    self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

    self.tab_generate = ttk.Frame(self.notebook)
    self.tab_add = ttk.Frame(self.notebook)
    self.tab_view = ttk.Frame(self.notebook)

    self.notebook.add(self.tab_generate, text="✨ Generate Name")
    self.notebook.add(self.tab_add, text="➕ Add Name")
    self.notebook.add(self.tab_view, text="📚 View & Delete Database")

    self.build_generate_tab()
    self.build_add_tab()
    self.build_view_tab()

  # ==========================================
  # TAB 1: GENERATE NAME
  # ==========================================
  def build_generate_tab(self):
    frame = ttk.LabelFrame(
        self.tab_generate, text=" Generation Constraints ", padding=15
    )
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    # 1. Format / Category Selection
    # 1. Format / Category Selection (Added "any" option)
    ttk.Label(frame, text="Name Format / Mode:").grid(
        row=0, column=0, sticky="w", pady=5
    )
    self.gen_category = ttk.Combobox(
        frame,
        values=[
            "any",
            "single_mode",
            "double_mode",
            "first_name",
            "second_name",
            "full_name",
        ],
        state="readonly",
    )
    self.gen_category.grid(row=0, column=1, sticky="ew", pady=5)
    self.gen_category.set("any")

    # 2. Gender Selection
    ttk.Label(frame, text="Gender Target:").grid(
        row=1, column=0, sticky="w", pady=5
    )
    genders, species_list, _ = get_metadata_lists()
    self.gen_gender = ttk.Combobox(frame, values=genders, state="readonly")
    self.gen_gender.grid(row=1, column=1, sticky="ew", pady=5)
    if genders:
      self.gen_gender.set(genders[0])

    # 3. Individual Type (Common vs Hybrid)
    ttk.Label(frame, text="Individual Type:").grid(
        row=2, column=0, sticky="w", pady=5
    )
    self.ind_type_var = tk.StringVar(value="common")

    type_frame = ttk.Frame(frame)
    type_frame.grid(row=2, column=1, sticky="w", pady=5)
    ttk.Radiobutton(
        type_frame,
        text="Common (1 Slot)",
        variable=self.ind_type_var,
        value="common",
        command=self.toggle_hybrid_slots,
    ).pack(side="left", padx=5)
    ttk.Radiobutton(
        type_frame,
        text="Hybrid (2 Slots)",
        variable=self.ind_type_var,
        value="hybrid",
        command=self.toggle_hybrid_slots,
    ).pack(side="left", padx=5)

    # 4. Taxonomic Slots Container
    self.slots_frame = ttk.LabelFrame(
        frame, text=" Taxonomic Slots ", padding=10
    )
    self.slots_frame.grid(
        row=3, column=0, columnspan=2, sticky="ew", pady=10
    )

    ttk.Label(self.slots_frame, text="Slot 1 - Species:").grid(
        row=0, column=0, sticky="w", padx=5, pady=2
    )
    self.slot1_species = ttk.Combobox(
        self.slots_frame, values=species_list, state="readonly"
    )
    self.slot1_species.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
    self.slot1_species.bind(
        "<<ComboboxSelected>>", lambda e: self.on_species_selected(1)
    )

    ttk.Label(self.slots_frame, text="Slot 1 - Sub-species:").grid(
        row=1, column=0, sticky="w", padx=5, pady=2
    )
    self.slot1_sub = ttk.Combobox(
        self.slots_frame, values=[], state="readonly"
    )
    self.slot1_sub.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

    self.slot2_label_sp = ttk.Label(self.slots_frame, text="Slot 2 - Species:")
    self.slot2_species = ttk.Combobox(
        self.slots_frame, values=species_list, state="readonly"
    )
    self.slot2_species.bind(
        "<<ComboboxSelected>>", lambda e: self.on_species_selected(2)
    )

    self.slot2_label_sub = ttk.Label(
        self.slots_frame, text="Slot 2 - Sub-species:"
    )
    self.slot2_sub = ttk.Combobox(
        self.slots_frame, values=[], state="readonly"
    )

    # 5. Inheritance Tier Checkboxes
    filter_frame = ttk.LabelFrame(
        frame, text=" Name Inclusion Checkboxes (Tiers) ", padding=10
    )
    filter_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

    self.chk_global_var = tk.BooleanVar(value=True)
    self.chk_species_gen_var = tk.BooleanVar(value=True)
    self.chk_subspecies_spec_var = tk.BooleanVar(value=True)

    ttk.Checkbutton(
        filter_frame,
        text="Allow Global Universal Names (e.g., 'any/any')",
        variable=self.chk_global_var,
    ).pack(anchor="w", pady=2)
    ttk.Checkbutton(
        filter_frame,
        text="Allow Species-Generic Names (e.g., Species macro-wide)",
        variable=self.chk_species_gen_var,
    ).pack(anchor="w", pady=2)
    ttk.Checkbutton(
        filter_frame,
        text="Allow Sub-Species Specific Names",
        variable=self.chk_subspecies_spec_var,
    ).pack(anchor="w", pady=2)

    # Generate Button
    gen_btn = ttk.Button(
        frame, text="✨ Generate Name", command=self.on_generate_click
    )
    gen_btn.grid(row=5, column=0, columnspan=2, sticky="ew", pady=15)

    # Result Display Box
    ttk.Label(frame, text="Result:").grid(row=6, column=0, sticky="w", pady=5)
    self.result_display = tk.Text(
        frame, height=3, font=("Arial", 12, "bold"), wrap="word"
    )
    self.result_display.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5)
    self.result_display.config(state="disabled")

    frame.columnconfigure(1, weight=1)
    self.slots_frame.columnconfigure(1, weight=1)

  def on_species_selected(self, slot_num):
    """Dynamically updates the sub-species combobox when a species is chosen."""
    if slot_num == 1:
      selected_species = self.slot1_species.get().strip().lower()
      sub_box = self.slot1_sub
    else:
      selected_species = self.slot2_species.get().strip().lower()
      sub_box = self.slot2_sub

    if not selected_species:
      return

    # Fetch sub-species available for this specific species
    valid_subs = get_sub_species_for_species(selected_species)
    sub_box.config(values=valid_subs)

    # Clear current selection and auto-select first available if any
    sub_box.set("")
    if valid_subs:
      sub_box.set(valid_subs[0])

  def toggle_hybrid_slots(self):
    if self.ind_type_var.get() == "hybrid":
      self.slot2_label_sp.grid(row=2, column=0, sticky="w", padx=5, pady=2)
      self.slot2_species.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
      self.slot2_label_sub.grid(row=3, column=0, sticky="w", padx=5, pady=2)
      self.slot2_sub.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
    else:
      self.slot2_label_sp.grid_remove()
      self.slot2_species.grid_remove()
      self.slot2_label_sub.grid_remove()
      self.slot2_sub.grid_remove()

  def on_generate_click(self):
    format_type = self.gen_category.get()
    gender = self.gen_gender.get()
    ind_type = self.ind_type_var.get()

    user_slots = []
    sp1 = self.slot1_species.get().strip().lower()
    sub1 = self.slot1_sub.get().strip().lower()

    if not sp1 or not sub1:
      messagebox.showerror(
          "Error", "Slot 1 must have both Species and Sub-species filled!"
      )
      return

    user_slots.append({"species": sp1, "sub_species": sub1})

    if ind_type == "hybrid":
      sp2 = self.slot2_species.get().strip().lower()
      sub2 = self.slot2_sub.get().strip().lower()
      if not sp2 or not sub2:
        messagebox.showerror(
            "Error",
            "Hybrid mode selected: Slot 2 must also have Species and"
            " Sub-species filled!",
        )
        return
      user_slots.append({"species": sp2, "sub_species": sub2})

    allow_global = self.chk_global_var.get()
    allow_species_gen = self.chk_species_gen_var.get()
    allow_subspecies_spec = self.chk_subspecies_spec_var.get()

    res = generate_name(
        format_type,
        gender,
        user_slots,
        allow_global=allow_global,
        allow_species_generic=allow_species_gen,
        allow_subspecies_specific=allow_subspecies_spec,
    )

    self.result_display.config(state="normal")
    self.result_display.delete("1.0", tk.END)
    self.result_display.insert(tk.END, res)
    self.result_display.config(state="disabled")

  # ==========================================
  # TAB 2: ADD NAME
  # ==========================================
  def build_add_tab(self):
    frame = ttk.LabelFrame(
        self.tab_add, text=" Add New Curated Name ", padding=15
    )
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
    self.add_name_entry = ttk.Entry(frame)
    self.add_name_entry.grid(row=0, column=1, sticky="ew", pady=5)

    ttk.Label(frame, text="Category:").grid(row=1, column=0, sticky="w", pady=5)
    self.add_category = ttk.Combobox(
        frame,
        values=["first_name", "second_name", "full_name"],
        state="readonly",
    )
    self.add_category.grid(row=1, column=1, sticky="ew", pady=5)
    self.add_category.set("first_name")

    ttk.Label(frame, text="Gender:").grid(row=2, column=0, sticky="w", pady=5)
    genders, _, _ = get_metadata_lists()
    self.add_gender = ttk.Combobox(frame, values=genders, state="readonly")
    self.add_gender.grid(row=2, column=1, sticky="ew", pady=5)
    if genders:
      self.add_gender.set(genders[0])

    ttk.Label(frame, text="Species (e.g. insect or elf):").grid(
        row=3, column=0, sticky="w", pady=5
    )
    self.add_species = ttk.Entry(frame)
    self.add_species.grid(row=3, column=1, sticky="ew", pady=5)
    self.add_species.insert(0, "insect")

    ttk.Label(
        frame, text="Sub-species (e.g. mantis or elf for self-matching):"
    ).grid(row=4, column=0, sticky="w", pady=5)
    self.add_sub = ttk.Entry(frame)
    self.add_sub.grid(row=4, column=1, sticky="ew", pady=5)
    self.add_sub.insert(0, "any")

    add_btn = ttk.Button(
        frame, text="💾 Save Name to Database", command=self.on_add_click
    )
    add_btn.grid(row=5, column=0, columnspan=2, sticky="ew", pady=20)

    frame.columnconfigure(1, weight=1)

  def on_add_click(self):
    name = self.add_name_entry.get().strip()
    category = self.add_category.get().strip()
    gender = self.add_gender.get().strip()
    species = self.add_species.get().strip().lower()
    sub_species = self.add_sub.get().strip().lower()

    if not name or not species or not sub_species:
      messagebox.showerror(
          "Error", "Please fill in all fields before saving!"
      )
      return

    insert_name(name, category, gender, species, sub_species)
    messagebox.showinfo("Success", f"Successfully added '{name}' to database!")
    self.add_name_entry.delete(0, tk.END)
    self.refresh_view_table()

  # ==========================================
  # TAB 3: VIEW & DELETE DATABASE
  # ==========================================
  def build_view_tab(self):
    frame = ttk.LabelFrame(
        self.tab_view, text=" Database Records Management ", padding=15
    )
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    columns = ("Row", "Name", "Category", "Gender", "Species", "Sub-species")
    self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

    self.tree.heading("Row", text="#")
    self.tree.column("Row", width=50, anchor="center")

    for col in columns[1:]:
      self.tree.heading(col, text=col)
      self.tree.column(col, width=100, anchor="w")

    scrollbar = ttk.Scrollbar(
        frame, orient="vertical", command=self.tree.yview
    )
    self.tree.configure(yscrollcommand=scrollbar.set)

    self.tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    btn_frame = ttk.Frame(self.tab_view)
    btn_frame.pack(fill="x", pady=10)

    refresh_btn = ttk.Button(
        btn_frame, text="🔄 Refresh Table", command=self.refresh_view_table
    )
    refresh_btn.pack(side="left", padx=5)

    delete_btn = ttk.Button(
        btn_frame, text="🗑️ Delete Selected Name", command=self.on_delete_click
    )
    delete_btn.pack(side="right", padx=5)

    self.refresh_view_table()

  def refresh_view_table(self):
    for item in self.tree.get_children():
      self.tree.delete(item)

    rows = get_all_entries()
    for index, row in enumerate(rows, 1):
      db_id = row[0]
      self.tree.insert(
          "",
          tk.END,
          values=(index, row[1], row[2], row[3], row[4], row[5]),
          tags=(str(db_id),),
      )

  def on_delete_click(self):
    selected_item = self.tree.selection()
    if not selected_item:
      messagebox.showwarning(
          "Selection Warning", "Please select a row in the table to delete."
      )
      return

    item_tags = self.tree.item(selected_item, "tag")
    if not item_tags:
      return

    db_id = int(item_tags[0])
    name_values = self.tree.item(selected_item, "values")
    name_text = name_values[1]

    confirm = messagebox.askyesno(
        "Confirm Deletion", f"Are you sure you want to delete '{name_text}'?"
    )
    if confirm:
      delete_name(db_id)
      messagebox.showinfo("Deleted", f"Successfully deleted '{name_text}'.")
      self.refresh_view_table()


if __name__ == "__main__":
  root = tk.Tk()
  app = WorldbuildingGUI(root)
  root.mainloop()