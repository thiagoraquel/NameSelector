# 🏷️ Projeto: Selecionador Procedural de Nomes (Worldbuilding)

## 📖 Introdução
Este projeto consiste em um **sistema selecionador e misturador (mix-and-match)** de nomes próprios curados manualmente, voltado para exercícios de worldbuilding (criação de universos ficcionais, espécies, raças e localidades). 

O sistema foca em **preservar 100% a integridade estética da curadoria humana**, utilizando um banco de dados estruturado com metadados para combinar nomes de forma inteligente, respeitando critérios de gênero, formatação estrutural, hierarquia biológica/cultural e hibridismo.

---

## ⚙️ Arquitetura Geral do Sistema
1. **Camada de Dados:** O núcleo do projeto. Armazena os nomes curados associados a metadados rigorosos (gênero, categoria de nome e vínculos taxonômicos).
2. **Camada de Decisão:** Recebe os parâmetros de entrada desejados pelo usuário (ex: tipo de indivíduo, espécie(s), sub-espécie(s), gênero, formato desejado).
3. **Camada de Algoritmo:** Realiza a seleção probabilística dentro do escopo filtrado, cruzando as regras de taxonomia e hibridismo.

---

## 📐 Regras de Definição e Estrutura de Dados

### 1. Categorias de Nomes (Formato de Armazenamento)
O banco de dados armazena os nomes estritamente em três categorias principais:
* **Primeiro Nome:** Uma entrada de palavra única.
* **Segundo Nome:** Uma entrada de palavra única (sobrenome ou cognome).
* **Nome Completo:** Uma entrada atômica e única (uma linha) contendo **obrigatoriamente duas palavras**. Ele é tratado como um bloco verídico por si só, evitando decomposições automáticas que inflariam os bancos de primeiro/segundo nome.

### 2. Regras de Geração (Saída do Seletor)
Com base na decisão do sistema:
* **Nomes de uma palavra:** Podem ser gerados **apenas** utilizando opções da categoria *Primeiro Nome*.
* **Nomes de duas palavras:** O seletor escolhe entre duas vias:
  1. A combinação de `Primeiro Nome` + `Segundo Nome`.
  2. A seleção direta de um `Nome Completo` atômico pré-cadastrado.

### 3. Gêneros
Cada entrada de nome é vinculada a um gênero específico, extensível conforme o worldbuilding evolui:
* Masculino
* Feminino
* Hermafrodita
* Neutro (indeterminado / unissex)

---

## 🧬 Hierarquia Taxonômica, Escopo e Cardinalidade

Cada nome cadastrado no banco possui obrigatoriamente **uma ou duas Espécies (macro)** e **uma ou duas Sub-espécies** associadas. Isso permite modelar desde nomes simples até títulos heróicos ou nomes completos exclusivos de híbridos específicos (ex: um nome com 1 espécie e 2 sub-espécies como *gafanhoto + muriçoca*, ou 2 espécies e 2 sub-espécies como *raposa + borboleta*).

### O Curinga `any`:
* **Sub-espécie como `"any"`:** Qualquer sub-espécie pertencente àquela espécie macro pode utilizar o nome.
* **Espécie como `"any"`:** O nome é universal, podendo ser utilizado por **literalmente qualquer indivíduo**, inclusive em contextos híbridos.

---

## 🔄 Regras de Validação e Atribuição Cruzada

Um nome pode ser atribuído a um indivíduo desde que os componentes taxonômicos do nome **contenham** as sub-espécies/espécies correspondentes ao indivíduo. 

* **Regra de Acesso Amplo:** Um híbrido (ex: *Louva-deus + Aranha*) pode utilizar legitimamente:
  1. Nomes genéricos (`any`).
  2. Nomes pertencentes exclusivamente à sub-espécie *Louva-deus*.
  3. Nomes pertencentes exclusivamente à sub-espécie *Aranha*.
  4. Nomes exclusivos da fusão híbrida *Louva-deus + Aranha*.

---

## ⚗️ Lógica de Seleção: Indivíduos Comuns vs. Híbridos (Incluindo Híbridos Puros)

A Camada de Decisão lida com diferentes perfis de input para a geração:

1. **Indivíduo Comum:** O usuário configura o seletor com apenas uma slot de Espécie/Sub-espécie. O algoritmo buscará nomes compatíveis apenas com aquele escopo único e com os genéricos (`any`).
2. **Indivíduo Híbrido (Misto ou Puro):** O usuário configura o seletor fornecendo **duas slots** de Espécie/Sub-espécie.
   * **Híbridos Mistos (Espécies diferentes):** Ex: *Aranha + Formiga*. O sistema pode buscar nomes exclusivos dessa combinação exata, ou puxar partes independentes de cada uma das metades parentais.
   * **Híbridos Puros (Mesma sub-espécie duplicada):** Ex: *Aranha + Aranha*. Representa indivíduos raros com poderes únicos. Na camada de dados, eles não exigem uma estrutura separada: o seletor processará as duas slots como sendo de Aranha, buscando nomes daquela sub-espécie ou genéricos. Caso uma combinação pura não faça sentido na lore (ex: *Humano + Humano*), o sistema simplesmente degrada a seleção para o comportamento de um indivíduo comum de um gene só."# NameSelector" 
