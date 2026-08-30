#!/usr/bin/env python3
"""
format_abnt.py - Motor de formatação acadêmica UNISA / ABNT
Converte arquivos Markdown (.md) ou texto bruto em:
  - HTML estilizado com regras @page milimétricas
  - PDF vetorial via Chromium/Chrome headless
  - DOCX editável via LibreOffice headless

Normas atendidas:
  - Formato UNISA/ABNT: A4; Arial 12; margens 3 cm (superior/esquerda) e 2 cm (inferior/direita);
  - Texto justificado; recuo de 1,25 cm na 1ª linha; espaçamento 1,5 entre linhas;
  - Cabeçalho institucional UNISA com blocos e alinhamentos conforme gabarito oficial;
  - Citações diretas curtas (entre aspas), diretas longas (>3 linhas, recuo 4cm, espaço simples, fonte 10pt) e indiretas;
  - Referências alinhadas à esquerda em espaçamento simples (NBR 6023).
"""

import sys
import os
import re
import argparse
import subprocess
from pathlib import Path


def parse_markdown_to_academic_html(md_text: str, font_family: str = "Arial") -> str:
    lines = md_text.strip().splitlines()
    
    header_institution = []
    student_lines = []
    turma_line = None
    docente_line = None
    doc_title = None
    
    body_elements = []
    in_references = False
    
    css = f"""
    @page {{
      size: A4 portrait;
      margin-top: 3cm;
      margin-left: 3cm;
      margin-bottom: 2cm;
      margin-right: 2cm;
    }}

    * {{
      box-sizing: border-box;
    }}

    html, body {{
      font-family: {font_family}, "Helvetica Neue", Helvetica, sans-serif;
      font-size: 12pt;
      line-height: 1.5;
      color: #000000;
      background-color: #ffffff;
      margin: 0;
      padding: 0;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }}

    /* Cabeçalho UNISA / ABNT */
    .header-unisa {{
      text-align: center;
      margin-bottom: 1.5rem;
    }}

    .header-unisa .inst-line {{
      font-size: 12pt;
      font-weight: bold;
      text-transform: uppercase;
      margin: 0;
      line-height: 1.5;
    }}

    /* Bloco de Alunas(os) e Turma (Alinhado à Esquerda) */
    .student-block {{
      text-align: left;
      margin-top: 1.5rem;
      margin-bottom: 1.5rem;
      font-size: 12pt;
      line-height: 1.5;
    }}

    .student-block p {{
      margin: 0;
      text-indent: 0;
      text-align: left;
      line-height: 1.5;
    }}

    /* Docente (Centralizado) */
    .docente-block {{
      text-align: center;
      margin-top: 1.5rem;
      margin-bottom: 1.5rem;
      font-size: 12pt;
      line-height: 1.5;
    }}

    .docente-block p {{
      margin: 0;
      text-indent: 0;
      text-align: center;
    }}

    /* Título do Trabalho / Resenha (Centralizado, Negrito) */
    .doc-title {{
      font-size: 12pt;
      font-weight: bold;
      text-align: center;
      margin-top: 1.5rem;
      margin-bottom: 1.5rem;
      line-height: 1.5;
      page-break-after: avoid;
      break-after: avoid;
    }}

    /* Seções e Títulos */
    .section-title {{
      font-size: 12pt;
      font-weight: bold;
      text-transform: uppercase;
      margin-top: 1.5rem;
      margin-bottom: 0.5rem;
      text-align: left;
      text-indent: 0;
      line-height: 1.5;
      page-break-after: avoid;
      break-after: avoid;
    }}

    /* Parágrafos de texto corrido */
    p.paragraph {{
      text-align: justify;
      text-indent: 1.25cm;
      line-height: 1.5;
      margin-top: 0;
      margin-bottom: 0.6rem;
      orphans: 3;
      widows: 3;
      hyphens: auto;
      -webkit-hyphens: auto;
    }}

    /* Citações longas (> 3 linhas, recuo 4cm, espaço simples, fonte 10pt) */
    blockquote.long-quote {{
      margin-left: 4.0cm;
      margin-right: 0;
      margin-top: 0.8rem;
      margin-bottom: 0.8rem;
      font-size: 10pt;
      line-height: 1.0;
      text-align: justify;
      text-indent: 0;
    }}

    /* Referências (Espaço simples, alinhadas à esquerda) */
    .reference-section {{
      margin-top: 2rem;
      page-break-inside: avoid;
      break-inside: avoid;
    }}

    .reference-title {{
      font-size: 12pt;
      font-weight: bold;
      text-transform: uppercase;
      margin-bottom: 0.8rem;
      text-align: left;
      text-indent: 0;
      line-height: 1.5;
      page-break-after: avoid;
      break-after: avoid;
    }}

    .reference-entry {{
      font-size: 12pt;
      line-height: 1.0;
      text-align: left;
      text-indent: 0;
      margin-bottom: 0.8rem;
    }}
    """

    def inline_md(t: str) -> str:
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
        t = re.sub(r'_(.+?)_', r'<em>\1</em>', t)
        return t

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Instituição e Curso (# UNIVERSIDADE... / ## CURSO...)
        if line.startswith('# ') and ('UNIVERSIDADE' in line.upper() or 'FACULDADE' in line.upper() or 'INSTITUTO' in line.upper() or not header_institution):
            inst_text = line.lstrip('#').strip()
            header_institution.append(f'<div class="inst-line">{inst_text}</div>')
            i += 1
            continue

        if line.startswith('## ') and ('CURSO' in line.upper() or (len(header_institution) == 1 and not doc_title and not student_lines)):
            if 'CURSO' in line.upper():
                course_text = line.lstrip('#').strip()
                header_institution.append(f'<div class="inst-line">{course_text}</div>')
                i += 1
                continue

        # Identificação de Alunas/Autores
        if re.search(r'^(?:\*\*)?(?:Alun[ao]s?|Nome):\s*', line, re.IGNORECASE):
            clean = re.sub(r'^\*\*(Alun[ao]s?|Nome):\s*\*\*', '', line, flags=re.IGNORECASE).strip()
            clean = re.sub(r'^(Alun[ao]s?|Nome):\s*', '', clean, flags=re.IGNORECASE).strip()
            
            parts = re.split(r'\s*[•|;]\s*', clean)
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                m_ra = re.search(r'^(.*?)(?:\s*[-–—]?\s*|\s*\(?)(?:\*\*)?RA:?(?:\*\*)?\s*([0-9A-Za-z]+)\)?$', part, re.IGNORECASE)
                if m_ra:
                    s_name = re.sub(r'[*_]', '', m_ra.group(1)).strip().rstrip('-–— ')
                    s_ra = m_ra.group(2).strip()
                    student_lines.append(f'<p><strong>Nome:</strong> {s_name} - <strong>RA:</strong> {s_ra}</p>')
                else:
                    s_name = re.sub(r'[*_]', '', part).strip()
                    student_lines.append(f'<p><strong>Nome:</strong> {s_name}</p>')
            i += 1
            continue

        # Turma e Docente na mesma linha
        if re.search(r'Turma:', line, re.IGNORECASE) and (re.search(r'Docente:', line, re.IGNORECASE) or re.search(r'Prof', line, re.IGNORECASE)):
            parts = re.split(r'\s*[|]\s*', line)
            for p in parts:
                p = p.strip()
                if re.search(r'Turma:', p, re.IGNORECASE):
                    t_val = re.sub(r'^\*\*Turma:\s*\*\*', '', p, flags=re.IGNORECASE)
                    t_val = re.sub(r'^\*\*Turma:\*\*', '', t_val, flags=re.IGNORECASE)
                    t_val = re.sub(r'^Turma:\s*', '', t_val, flags=re.IGNORECASE).strip()
                    t_val = re.sub(r'[*_]', '', t_val).strip()
                    turma_line = f'<p><strong>Turma:</strong> {t_val}</p>'
                elif re.search(r'Docente:', p, re.IGNORECASE) or re.search(r'Prof', p, re.IGNORECASE):
                    d_val = re.sub(r'^\*\*Docente:\s*\*\*', '', p, flags=re.IGNORECASE)
                    d_val = re.sub(r'^\*\*Docente:\*\*', '', d_val, flags=re.IGNORECASE)
                    d_val = re.sub(r'^Docente:\s*', '', d_val, flags=re.IGNORECASE).strip()
                    d_val = re.sub(r'[*_]', '', d_val).strip()
                    docente_line = f'<div class="docente-block"><p>{d_val}</p></div>'
            i += 1
            continue

        # Turma isolada
        if re.search(r'^(?:\*\*)?Turma:\s*', line, re.IGNORECASE):
            t_val = re.sub(r'^\*\*Turma:\s*\*\*', '', line, flags=re.IGNORECASE)
            t_val = re.sub(r'^\*\*Turma:\*\*', '', t_val, flags=re.IGNORECASE)
            t_val = re.sub(r'^Turma:\s*', '', t_val, flags=re.IGNORECASE).strip()
            t_val = re.sub(r'[*_]', '', t_val).strip()
            turma_line = f'<p><strong>Turma:</strong> {t_val}</p>'
            i += 1
            continue

        # Docente / Professora isolada
        if re.search(r'^(?:\*\*)?Docente:\s*', line, re.IGNORECASE) or re.match(r'^(?:Prof[a-z]?\.?|Professor[a]?)\s+', line, re.IGNORECASE):
            d_val = re.sub(r'^\*\*Docente:\s*\*\*', '', line, flags=re.IGNORECASE)
            d_val = re.sub(r'^\*\*Docente:\*\*', '', d_val, flags=re.IGNORECASE)
            d_val = re.sub(r'^Docente:\s*', '', d_val, flags=re.IGNORECASE).strip()
            d_val = re.sub(r'[*_]', '', d_val).strip()
            docente_line = f'<div class="docente-block"><p>{d_val}</p></div>'
            i += 1
            continue

        # Título da Resenha / Trabalho (## RESENHA... or # RESENHA...)
        if (line.startswith('## ') or line.startswith('# ')) and not doc_title and not re.match(r'^#+\s*\d+\.', line):
            doc_title = line.lstrip('#').strip()
            i += 1
            continue

        # Referências (NBR 6023)
        if re.match(r'^\*?\*?REFER[ÊE]NCIAS?\*?\*?$', line, re.IGNORECASE) or line.startswith('## REFER'):
            in_references = True
            ref_title = re.sub(r'[*#]', '', line).strip().upper()
            body_elements.append(f'<div class="reference-section"><div class="reference-title">{ref_title}</div>')
            i += 1
            continue

        # Títulos de Seção (Ex: 1. INTRODUÇÃO)
        section_match = re.match(r'^(?:##\s*)?(\d+\.\s+[^#\n]+)$', line)
        if section_match:
            sec_text = inline_md(section_match.group(1).strip())
            if in_references:
                body_elements.append('</div>')
                in_references = False
            body_elements.append(f'<div class="section-title">{sec_text}</div>')
            i += 1
            continue

        # Citação Longa (> 3 linhas: > texto)
        if line.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip().lstrip('>').strip())
                i += 1
            quote_text = inline_md(" ".join(quote_lines))
            body_elements.append(f'<blockquote class="long-quote">{quote_text}</blockquote>')
            continue

        # Entrada de Referência
        if in_references:
            body_elements.append(f'<p class="reference-entry">{inline_md(line)}</p>')
            i += 1
            continue

        # Parágrafo Corrido Justificado
        para_lines = [line]
        i += 1
        while (i < len(lines) and 
               lines[i].strip() != '' and 
               not lines[i].strip().startswith('#') and 
               not re.match(r'^\d+\.', lines[i].strip()) and 
               not re.match(r'^(?:\*\*)?(?:Alun|Nome|Turma|Docente|Prof|Orientador|Data|REFER)', lines[i].strip(), re.IGNORECASE) and 
               not lines[i].strip().startswith('>')):
            para_lines.append(lines[i].strip())
            i += 1

        para_text = inline_md(" ".join(para_lines))
        body_elements.append(f'<p class="paragraph">{para_text}</p>')

    if in_references:
        body_elements.append('</div>')

    # Montagem do cabeçalho UNISA / ABNT
    header_html = f'<div class="header-unisa">{"".join(header_institution)}</div>' if header_institution else ''
    
    student_content = "".join(student_lines)
    if turma_line:
        student_content += turma_line
    student_block_html = f'<div class="student-block">{student_content}</div>' if student_content else ''
    
    docente_html = docente_line if docente_line else ''
    title_html = f'<div class="doc-title">{doc_title}</div>' if doc_title else ''

    full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>{doc_title or 'Documento UNISA - ABNT'}</title>
  <style>
{css}
  </style>
</head>
<body>
  {header_html}
  {student_block_html}
  {docente_html}
  {title_html}
  {"".join(body_elements)}
</body>
</html>
"""
    return full_html


def build_documents(input_path: str, output_prefix: str = None, font: str = "Arial", format_target: str = "all"):
    path = Path(input_path)
    if not path.exists():
        print(f"Erro: Arquivo '{input_path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    prefix = output_prefix or path.stem
    out_dir = path.parent.resolve()

    md_content = path.read_text(encoding="utf-8")
    html_content = parse_markdown_to_academic_html(md_content, font_family=font)

    html_file = out_dir / f"{prefix}.html"
    pdf_file = out_dir / f"{prefix}.pdf"
    docx_file = out_dir / f"{prefix}.docx"

    html_file.write_text(html_content, encoding="utf-8")
    print(f"✅ HTML gerado: {html_file}")

    if format_target in ("all", "pdf"):
        # Compilação PDF com Chrome headless
        try:
            chrome_bin = None
            for candidate in ("google-chrome-stable", "google-chrome", "chromium", "chromium-browser"):
                if subprocess.run(["which", candidate], capture_output=True).returncode == 0:
                    chrome_bin = candidate
                    break
            
            if chrome_bin:
                cmd_pdf = [
                    chrome_bin,
                    "--headless=new",
                    "--disable-gpu",
                    "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_file.name}",
                    html_file.name
                ]
                subprocess.run(cmd_pdf, cwd=out_dir, capture_output=True, text=True, check=True)
                print(f"✅ PDF compilado: {pdf_file}")
            else:
                print("⚠️ Google Chrome / Chromium não encontrado no PATH para compilação PDF.", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Erro ao compilar PDF via Chrome: {e}", file=sys.stderr)

    if format_target in ("all", "docx"):
        # Compilação DOCX com LibreOffice
        try:
            soffice_bin = None
            for candidate in ("soffice", "libreoffice"):
                if subprocess.run(["which", candidate], capture_output=True).returncode == 0:
                    soffice_bin = candidate
                    break
            
            if soffice_bin:
                cmd_docx = [
                    soffice_bin,
                    "--headless",
                    '--convert-to', 'docx:MS Word 2007 XML',
                    html_file.name,
                    "--outdir", str(out_dir)
                ]
                subprocess.run(cmd_docx, cwd=out_dir, capture_output=True, text=True, check=True)
                print(f"✅ DOCX compilado: {docx_file}")
            else:
                print("⚠️ LibreOffice (soffice) não encontrado no PATH para conversão DOCX.", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ Erro ao converter para DOCX via LibreOffice: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Formatar Markdown para o padrão UNISA / ABNT (gera HTML, PDF e DOCX)"
    )
    parser.add_argument("input_file", help="Caminho do arquivo Markdown (.md)")
    parser.add_argument("-o", "--output", help="Prefixo customizado do arquivo de saída")
    parser.add_argument(
        "--font",
        default="Arial",
        choices=["Arial", "Times New Roman"],
        help="Família da fonte (padrão: Arial)",
    )
    parser.add_argument(
        "--target",
        default="all",
        choices=["all", "pdf", "docx", "html"],
        help="Formatos de saída a gerar (padrão: all)",
    )
    args = parser.parse_args()

    build_documents(args.input_file, output_prefix=args.output, font=args.font, format_target=args.target)


if __name__ == "__main__":
    main()
