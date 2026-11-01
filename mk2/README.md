# 🏷️ Project: Procedural Name Selector (Worldbuilding)

## 📖 Introduction
This project consists of a **mix-and-match name selection system** using manually curated names for worldbuilding exercises (creating fictional universes, species, races, and locations). 

The system focuses on **preserving 100% of the human curation's aesthetic integrity** by using a structured database with rich metadata to combine names intelligently. It respects criteria such as gender, structural formatting, biological/cultural hierarchy, and hybridization.

---

## ⚙️ General System Architecture
1. **Data Layer:** The core of the project. Stores curated names associated with strict metadata (gender, name category, and taxonomic linkages).
2. **Decision Layer:** Receives input parameters specified by the user (e.g., individual type, species, sub-species, gender, desired format).
3. **Algorithm Layer:** Performs probabilistic selection within the filtered scope, cross-referencing taxonomy and hybridization rules.

---

## 📐 Rules of Definition and Data Structure

### 1. Name Categories (Storage Format)
The database strictly stores names across three main categories:
* **First Name:** A single-word entry.
* **Second Name:** A single-word entry (surname or cognomen).
* **Full Name:** An atomic, single-line entry containing **strictly two words**. It is treated as a complete block on its own, avoiding automatic decomposition that would artificially inflate the first/second name pools.

### 2. Generation Rules (Selector Output)
Based on the system's decision:
* **One-word names:** Generated **exclusively** using options from the *First Name* category.
* **Two-word names:** The selector chooses between two paths:
  1. Combining a `First Name` + `Second Name`.
  2. Selecting a pre-registered, atomic `Full Name` directly.

### 3. Genders
Each name entry is linked to a specific gender, extensible as worldbuilding grows:
* Male
* Female
* Hermaphrodite
* Neutral (undetermined / unisex)

---

## 🧬 Taxonomic Hierarchy, Scope, and Cardinality

Each name registered in the database must be linked to **one or two Species (macro)** and **one or two Sub-species**. This allows modeling everything from simple names to heroic titles or full names exclusive to specific hybrids (e.g., a name with 1 species and 2 sub-species like *grasshopper + gnat*, or 2 species and 2 sub-species like *fox + butterfly*).

### The `any` Wildcard:
* **Sub-species as `"any"`:** Any sub-species belonging to that macro species can use the name.
* **Species as `"any"`:** The name is universal and can be used by **literally any individual**, including in hybrid contexts.

---

## 🔄 Validation Rules and Cross-Attribution

A name can be assigned to an individual as long as the taxonomic components of the name **contain** the sub-species/species corresponding to that individual.

* **Broad Access Rule:** A hybrid (e.g., *Praying Mantis + Spider*) can legitimately use:
  1. Generic names (`any`).
  2. Names belonging exclusively to the *Praying Mantis* sub-species.
  3. Names belonging exclusively to the *Spider* sub-species.
  4. Names exclusive to the hybrid fusion *Praying Mantis + Spider*.

---

## ⚗️ Selection Logic: Standard Individuals vs. Hybrids (Including Pure Hybrids)

The Decision Layer handles different input profiles for generation:

1. **Standard Individual:** The user configures the selector with a single Species/Sub-species slot. The algorithm searches for names compatible only with that single scope and generics (`any`).
2. **Hybrid Individual (Mixed or Pure):** The user configures the selector providing **two slots** for Species/Sub-species.
   * **Mixed Hybrids (Different species):** E.g., *Spider + Ant*. The system can search for names exclusive to that exact combination or draw independent parts from each parental half.
   * **Pure Hybrids (Same sub-species duplicated):** E.g., *Spider + Spider*. Represents rare individuals with unique powers. In the data layer, they do not require a separate structure: the selector processes both slots as Spider, drawing names from that sub-species or generics. If a pure combination makes no sense in lore (e.g., *Human + Human*), the system simply degrades selection to the behavior of a single-gene standard individual.