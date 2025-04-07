import sys
import os
import re

REQUIRED_FIELDS = ['title', 'author', 'journal', 'year']


def extract_doi_from_url(url):
    match = re.search(r'10\.\d{4,9}/[^\s"\'<>]+', url)
    return match.group(0).lower() if match else url.strip().lower()


def normalize_identifier(raw):
    if 'doi.org' in raw.lower():
        return extract_doi_from_url(raw)
    return raw.strip().lower()


def extract_bib_field(entry, field):
    brace_pattern = re.compile(rf'{field}\s*=\s*\{{(.*?)\}}', re.IGNORECASE | re.DOTALL)
    quote_pattern = re.compile(rf'{field}\s*=\s*"([^"]+)"', re.IGNORECASE)
    brace_match = brace_pattern.search(entry)
    if brace_match:
        return brace_match.group(1).strip()
    quote_match = quote_pattern.search(entry)
    if quote_match:
        return quote_match.group(1).strip()
    return None


def has_university_author(author_field):
    if not author_field:
        return False
    return re.search(r'\b(university|college)\b', author_field, re.IGNORECASE) is not None


def parse_bibtex_entry(raw_entry):
    entry_type_match = re.match(r'(\w+)\s*{', raw_entry)
    entry_type = entry_type_match.group(1).lower() if entry_type_match else None

    fields = {
        "type": entry_type,
        "title": extract_bib_field(raw_entry, 'title'),
        "author": extract_bib_field(raw_entry, 'author'),
        "journal": extract_bib_field(raw_entry, 'journal') or extract_bib_field(raw_entry, 'booktitle'),
        "year": extract_bib_field(raw_entry, 'year'),
        "doi": extract_bib_field(raw_entry, 'doi'),
        "url": extract_bib_field(raw_entry, 'url')
    }

    identifiers = set()
    if fields["doi"]:
        identifiers.add(extract_doi_from_url(fields["doi"]))
    if fields["url"]:
        identifiers.add(normalize_identifier(fields["url"]))

    return fields, identifiers


def run_check(bib_path, txt_path):
    result_lines = []

    # Load links
    with open(txt_path, "r", encoding="utf-8") as f:
        file_links = {extract_doi_from_url(line.strip()) for line in f if line.strip()}

    # Load BibTeX
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()
    entries = content.split('@')[1:]
    zotero_entries = [parse_bibtex_entry(e) for e in entries]

    # Compare
    missing = file_links.copy()
    extra = []
    incomplete = []

    for fields, ids in zotero_entries:
        if ids & file_links:
            missing -= ids
        else:
            extra.append((fields, ids))

        missing_fields = [f for f in REQUIRED_FIELDS if not fields.get(f)]
        if has_university_author(fields.get("author")):
            missing_fields.append("suspect_author")

        if missing_fields:
            incomplete.append((fields, missing_fields))

    result_lines.append("==== MISSING LINKS (in file, not in Zotero) ====")
    for link in sorted(missing):
        result_lines.append(link)

    result_lines.append("\n==== EXTRA ENTRIES (in Zotero, not in file) ====")
    for fields, ids in extra:
        title = fields.get("title", "Untitled")
        result_lines.append(f"{title} | {', '.join(sorted(ids))}")

    result_lines.append("\n==== INCOMPLETE METADATA ====")
    for fields, missing_fields in incomplete:
        title = fields.get("title", "Untitled")
        result_lines.append(f"{title} | Missing: {', '.join(missing_fields)}")

    # Print to terminal
    for line in result_lines:
        print(line)

    # Save to single file
    output_file = os.path.join(os.path.dirname(bib_path), "zotero_check_result.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for line in result_lines:
            f.write(line + "\n")

    input("\nCheck the results file created at the path of your BibTeX file.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python zotero_checker_core.py <bibfile> <linkfile>")
    else:
        run_check(sys.argv[1], sys.argv[2])
