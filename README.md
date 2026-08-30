# ABNT UNISA Plugin & CLI

Formatação acadêmica automatizada no padrão oficial **UNISA / ABNT** com suporte nativo a múltiplos assistentes de IA (**Claude Code**, **Cursor**, **Antigravity**, **Oh My Pi**, **OpenCode**) e linha de comando (**CLI**).

Converte arquivos Markdown (`.md`) diretamente para **PDF vetorial de alta precisão**, **Word (DOCX) editável** e **HTML de impressão**.

---

## 🎯 Especificações Atendidas

* **Formato de Folha:** A4 (210 x 297 mm), orientação retrato.
* **Margens Físicas:**
  * **Superior:** 3,0 cm
  * **Esquerda:** 3,0 cm
  * **Inferior:** 2,0 cm
  * **Direita:** 2,0 cm
* **Tipografia:** Arial (ou Times New Roman), corpo **12 pt**.
* **Espaçamento Entrelinhas:** **1,5** no corpo do texto.
* **Parágrafos:** Justificados (`text-align: justify`) com recuo de 1ª linha de **1,25 cm**.
* **Cabeçalho UNISA Padronizado:**
  * Instituição e Curso centralizados em negrito e caixa alta.
  * Bloco de alunas(os) e turma alinhado à esquerda (`Nome: ... - RA: ...`).
  * Docente centralizado em texto normal.
  * Título da resenha/trabalho centralizado em negrito.
* **Citações:**
  * Direta curta no próprio texto entre aspas.
  * Direta longa (> 3 linhas) com recuo de **4,0 cm** à esquerda, entrelinhas **simples (1,0)**, sem aspas e com fonte menor (**10 pt**).
  * Indireta sem aspas.
* **Referências (NBR 6023):** Alinhadas à margem esquerda com espaçamento **simples (1,0)**.

---

## 🚀 Instalação Rápida

### 1. Clonar o repositório
```bash
git clone git@github.com:renanbs/abnt-unisa.git ~/src/abnt-unisa
cd ~/src/abnt-unisa
```

### 2. Instalar os comandos CLI no terminal
```bash
make install-cli
```
Isso disponibiliza os comandos `format-doc`, `abnt-unisa` e `format-abnt` no seu `~/.local/bin`.

---

## 💻 Uso via Linha de Comando (CLI)

```bash
# Formata o documento e compila HTML, PDF e DOCX automaticamente:
format-doc meu_trabalho.md

# Usando o comando com nome do plugin:
abnt-unisa meu_trabalho.md

# Usando fonte Times New Roman:
format-doc meu_trabalho.md --font "Times New Roman"

# Gerando apenas PDF:
format-doc meu_trabalho.md --target pdf
```

---

## 🤖 Integração com Assistentes de IA

### Claude Code
* **Slash Command:** `/format-doc <arquivo.md>`
* **Skill Automática:** Ativada automaticamente sempre que você pedir para formatar um documento em ABNT/UNISA.

### Cursor / Cursor CLI
* Regra global `.cursor/rules/abnt-unisa.mdc` inclusa.
* Reconhece o comando `/format-doc` e executa via terminal.

### Antigravity & Oh My Pi
* Skills prontas em `antigravity/` e `omp/` para execução autônoma do fluxo de formatação.

---

## 📁 Estrutura do Arquivo Markdown de Entrada

```markdown
# UNIVERSIDADE SANTO AMARO - UNISA
## CURSO DE PSICOLOGIA - TEORIAS DA PERSONALIDADE

**Nome:** Nome da Aluna 1 - **RA:** 1234567
**Nome:** Nome da Aluna 2 - **RA:** 7654321
**Turma:** 4A

Profa. Nome da Professora

## RESENHA 1 – TÍTULO DO TRABALHO OU RESENHA ACADÊMICA

1. **INTRODUÇÃO**

Texto da introdução justificado com recuo de 1,25 cm...

2. **SÍNTESE DA OBRA**

Texto do desenvolvimento...

> Citação direta longa com mais de três linhas sem aspas, recuo de 4 cm à esquerda e fonte 10 pt.

3. **ANÁLISE CRÍTICA**

Texto da análise crítica...

4. **CONCLUSÃO**

Texto da conclusão...

**REFERÊNCIAS**

SOBRENOME, Nome. **Título da Obra em Negrito**: subtítulo sem negrito. Edição. Local: Editora, Ano.
```

---

## 🛠️ Requisitos de Sistema
* **Python 3.8+**
* **Google Chrome / Chromium:** Para compilação PDF com fidelidade vetorial `@page` (`--headless=new`).
* **LibreOffice (`soffice`):** Para conversão de `.html` para `.docx`.

Verifique seus requisitos rodando:
```bash
make check-deps
```

---

## 📄 Licença
Distribuído sob a licença [MIT](LICENSE).
