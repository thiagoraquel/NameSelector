# 🏷️ Project: Procedural Name Selector (Worldbuilding)

## 📖 Introduction
This project consists of a **mix-and-match name selection system** using manually curated names for worldbuilding exercises (creating fictional universes, species, races, and locations). 

The system focuses on **preserving 100% of the human curation's aesthetic integrity** by using a structured database with rich metadata to combine names intelligently. It respects criteria such as gender, structural formatting, biological/cultural hierarchy, and hybridization.

---

## ⚙️ General System Architecture
1. **Data Layer:** The core of the project. Stores curated names associated with strict metadata (gender, name category, and etc).
2. **Decision Layer:** Receives input parameters specified by the user (e.g., individual type, species, sub-species, gender, desired format, checkboxes).
3. **Algorithm Layer:** Performs probabilistic selection within the filtered scope, cross-referencing taxonomy and hybridization rules.

---

### 1. 📐 Data Layer
The database strictly stores names in this exact way:

#### Format:
**First Name:** A single-word entry.
**Second Name:** A single-word entry (surname or cognomen).
**Compound Name:** An atomic, single-line entry containing **strictly two or three words**. It is treated as a complete block on its own.

#### Gender:
**Male:** A masculine entry.
**Female:** A feminine entry.
**Neutral:** A neutral entry.

#### Species:
At least one species and at most two. There is no "Single Species" or "Double Species" category, it comes as a list of either a single species or two.
**Species:** ["bug"].

##### Special case:
**Any:** There may be names with the "any" tag on species. That is a specific case where the species and subspecies will also be "any".

#### Subspecies:
At least one subspecies and at most two. There is no "Single Subspecies" or "Double Subspecies" category, it comes as a list of either a single subspecies or two.
**Subspecies:** ["mantis"].

##### Special cases:
**Any:** There may be names with the "any" tag on subspecies. That is a specific case where the species and subspecies will also be "any".
**Species And Subspecies Identical:** There may be names where the subspecies tag is the exact same as the species. These are generic names. An species:bug, subspecies:bug name is a generic name usable by all bug subspecies. However elfs don't have subspecies, so an species:elf, subspecies:elf name is only usable by elfs, being simoultaneously general for all elfs and specific for only elfs.

### 2. 🧬 Selection Rules For Generation With Interface

#### Format

**First Name:** Generates a first name.
**Second Name:** Generates a second name.
**Compound Name:** Generates a compound name.
**Atomic Name:** Generates either a first name or a second name.
**Single Name:** Generates either a first name, a second name or a compound name.
**Paired Name:** Generates a first name + second name.
**Full Name:** Generates either a first name + second name or a compound name.
**Any Name:** Generates either a first name, a second name, a compound name, or a first name + second name.
**Random:** Generates a name with one of the formats above chosen at random.

#### Gender

**Male:** Generates a male name.
**Female:** Generates a female name.
**Neutral:** Generates a neutral name.
**Mal&Neutral:** Generates a male or neutral name.
**Femal&Neutral:** Generates a female or neutral name.

#### Species
There is no fixed number of species, and more may be added, but there is a special case.
**Any:** There may be names with the "any" tag on species. That is a specific case where the species and subspecies will also be "any". Such names are universal names used by any species. These universal names may not be included in generation via it's respective checkbox on the interface.

#### Subspecies
Every species may have at least one subspecies specific to them.

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