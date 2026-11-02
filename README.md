# 🏷️ Project: Procedural Name Selector (Worldbuilding)

## 📖 Introduction
This project consists of a **mix-and-match name selection system** using manually curated names for worldbuilding exercises (creating fictional universes, species, races, and locations). 

The system focuses on **preserving 100% of the human curation's aesthetic integrity** by using a structured database with simple metadata to combine names intelligently. It respects criteria such as gender, structural formatting, biological/cultural hierarchy, and hybridization.

---

## ⚙️ General System Architecture
1. **Data Layer:** The core of the project. Stores curated names associated with strict metadata (gender, name category, and etc).
2. **Decision Layer:** Receives input parameters specified by the user (e.g., individual type, species, sub-species, gender, desired format, checkboxes).
3. **Algorithm Layer:** Currently this code does not need or has implemented an algorithm layer, given the restrictions will be validated, the selected name will be randomized from all pools it can draw from.

---

### 1. 📐 Data Layer
The database strictly stores names in this exact way:

#### Name:
The name data that will be used for name selection.

#### Format:
**First Name:** A single-word entry.
**Second Name:** A single-word entry (surname or cognomen).
**Compound Name:** An atomic, single-line entry containing **strictly two or three words separated by spaces**. It is treated as a complete block on its own.

#### Gender:
**Male:** A masculine entry.
**Female:** A feminine entry.
**Neutral:** A neutral entry (for assexual/unissex/hermaphrodite names).

#### Species:
Each entry has one species.
**Species:** ["bug"].

##### Special case:
**Any:** There may be names with the "any" tag on species. That is a specific case where the species and subspecies will also be "any".

#### Subspecies:
Each entry has one subspecies.
**Subspecies:** ["mantis"].

##### Special cases:
**Any:** There may be names with the "any" tag on subspecies. That is a specific case where the species and subspecies will also be "any".
**Species And Subspecies Identical:** There may be names where the subspecies tag is the exact same as the species. These are generic names for that species, usable by any subspecies of that species. For example, subspecies:"bug".
**Otherwise:** Subspecies will be different from "any" and it's species name.

### 2. 🧬 Selection Rules For Generation With Interface

In order for a name to be selected, all parameters must be chosen and be valid via the GUI.

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
By default starts blank.
**Specific Species:** Generation will only choose names from that species. Only existing species in the database will be shown. If a species is chosen, by default it sets subspecies to the same name as species if it exists, otherwise, sets subspecies to "any".
**Any:** Generation will choose names from any species. By default sets subspecies to "any" if chosen.

#### Subspecies
By default starts blank.
**Specific Subspecies:** Generation will only choose names from that subspecies. Only existing subspecies of the selected species in the database will be shown.
**Same As Species:** Generation will only choose generic names usable by any subspecies from that species, and no names from specific subspecies.
**Any:** Generation will choose names from any subspecies of that species, including generic names (unless marked off on checkboxes). 

#### Checkboxes
At least one of the three checkboxes below must be selected for selection, and the system does not allow for all three to be toggled off simultaneously. There is no guarantee that a name may be generated with only one checkbox on or even three (although with three on, a universal name will always be generated).

**Include Universal Names:** Generation will include or exclude universal names. Universal names are names usable by any species. They are the entries with both species:"any" and subspecies:"any". Entries with "any" will always come with it on species and subspecies and it's the only case where "any" appears in whatever way, meaning it always comes coupled on species and subspecies.

**Include Species Generic Names:** Generation will include or exclude species generic names. Species generic names are names usable by any subspecies of the selected species. They are entries where species and subspecies have the same name, like `species:"bug"` and `subspecies:"bug"`. 
> *Base Case for Single-Tier Races (like Elfs):* Races without subspecies are stored as `species:"elf"` and `subspecies:"elf"`, meaning their names fall under this tier. This checkbox acts as the master switch for that species' base names: if marked off, no base names are selected from that species, independent of the subspecies checkbox.

**Include Subspecies Specific Names:** Generation will include or exclude subspecies specific names. Subspecies specific names are entries where species and subspecies differ in name, like `species:"bug"` and `subspecies:"mantis"`, targeting exclusive sub-group variations.

#### Individual Mode
User must choose between one of two modes for name generation.

**Standard:** One species and subspecies must be selected. Generation will select as normal.
**Hybrid:** Two species and subspecies must be selected. Generation will simply unite the pool of both species/subspecies generated. If either of the two species is set to "any", put all species and subspecies to "any". If an option other than "any" is selected, put the rest to blank so user may select what he wants and isn't locked into "any" forever. 
If both species and subspecies for the two slots are the same, generation will work as if it's a standard name. The case is called within worldbuilding as "pure hybrid".
Otherwise, the most common case of all, where the species/subspecies differ is called "mixed hybrid".