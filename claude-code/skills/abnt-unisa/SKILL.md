---
name: abnt-unisa
description: Formata automaticamente documentos acadêmicos e resenhas no padrão oficial UNISA / ABNT (NBR 14724, NBR 6023, NBR 10520) com folha A4, Arial 12pt, margens 3cm (superior/esquerda) e 2cm (inferior/direita), recuo de 1,25cm na 1ª linha, entrelinhas 1,5, texto justificado, cabeçalho institucional UNISA padronizado, citações diretas/indiretas e referências em espaço simples. Gera automaticamente PDF de alta fidelidade e DOCX editável. Use sempre que o usuário pedir formatação ABNT/UNISA, gerar PDF de resenha/trabalho, formatar cabeçalho acadêmico, rodar /format-doc ou converter Markdown para PDF/Word acadêmico.
---

# abnt-unisa — Formatação Acadêmica UNISA / ABNT & Compilação PDF/DOCX

Esta skill automatiza a estruturação, estilização e compilação de resenhas e trabalhos acadêmicos no padrão institucional **UNISA / ABNT**, garantindo conformidade visual com os modelos oficiais.

---

## 1. Especificações Oficiais UNISA / ABNT

| Elemento | Regra / Valor | Implementação CSS / Layout |
| :--- | :--- | :--- |
| **Papel & Orientação** | A4 (210 x 297 mm), retrato | `@page { size: A4 portrait; }` |
| **Margem Superior** | **3,0 cm** | `margin-top: 3cm;` |
| **Margem Esquerda** | **3,0 cm** | `margin-left: 3cm;` |
| **Margem Inferior** | **2,0 cm** | `margin-bottom: 2cm;` |
| **Margem Direita** | **2,0 cm** | `margin-right: 2cm;` |
| **Tipografia** | Arial (ou Times New Roman), corpo **12 pt** | `font-family: Arial, sans-serif; font-size: 12pt;` |
| **Espaçamento Entrelinhas** | **1,5** no corpo do texto | `line-height: 1.5;` |
| **Alinhamento do Texto** | **Justificado** | `text-align: justify;` |
| **Recuo de 1ª Linha** | **1,25 cm** nos parágrafos normais | `text-indent: 1.25cm;` |
| **Títulos de Seções** | Negrito, caixa alta, alinhados à esquerda, **sem recuo** | `font-weight: bold; text-indent: 0; break-after: avoid;` |
| **Citação Direta Curta** | Entre aspas, no corpo do texto, com autor, ano e página | Inline com `""` |
| **Citação Direta Longa (> 3 linhas)** | Recuo de 4,0 cm à esquerda, entrelinhas simples (1,0), sem aspas, fonte menor (10 pt) | `margin-left: 4cm; font-size: 10pt; line-height: 1.0;` |
| **Citação Indireta** | No corpo do texto, sem aspas, com indicação de autor/ano | Parágrafo normal |
| **Referências (NBR 6023)** | Espaçamento simples (1,0), alinhadas à esquerda | `text-align: left; text-indent: 0; line-height: 1.0;` |
| **Controle de Paginação** | Evitar linhas órfãs/viúvas e quebra de títulos | `orphans: 3; widows: 3; break-after: avoid;` |

---

## 2. Padrão Visual do Cabeçalho UNISA

O cabeçalho segue rigorosamente a seguinte distribuição de blocos e alinhamentos:

```text
               UNIVERSIDADE SANTO AMARO - UNISA
          CURSO DE PSICOLOGIA - TEORIAS DA PERSONALIDADE
          [Centralizados, Negrito, Caixa Alta, 12pt]

Nome: Nome do Aluno 1 - RA: 1234567
Nome: Nome do Aluno 2 - RA: 7654321
Turma: 4A
[Alinhados à Esquerda, 12pt, "Nome:", "RA:", "Turma:" em Negrito]

                   Profa. Nome da Professora
                   [Centralizado, Normal, 12pt]

 RESENHA 1 – O que é personalidade e o que caracteriza uma teoria da
                           personalidade?
                   [Centralizado, Negrito, 12pt]
```

---

## 3. Comandos Disponíveis

### Slash Command (Claude Code / Cursor)
```bash
/format-doc <arquivo.md>
```

### CLI Terminal
```bash
# Formata o documento gerando HTML, PDF e DOCX automaticamente:
format-doc documento.md
# ou
abnt-unisa documento.md
```
