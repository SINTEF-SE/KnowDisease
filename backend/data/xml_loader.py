import os
import re
import xml.etree.ElementTree as ET

exclude_sections = {
    "REF", "REFERENCE", "REFERENCES", "BIBLIO", "ACK", "FIG", "TABLE", "SUPPL",
    "SUPPLEMENT", "AUTHOR_NOTES", "LICENSE", "GLOSSARY", "AUTH_CONT", "COMP_INT", "FRONT",
    "FIG_CAPTION", "TABLE_FOOTNOTE", "TABLE_CAPTION", "ACK_FUND", "ABBR", "FOOTNOTE",
    "CONCLUSION", "CONCLUSIONS"
}


def _infon(p, key):
    for inf in p.findall("infon"):
        if inf.get("key") == key:
            return (inf.text or "").strip()
    return ""

def load_xml(xml_path):
    if not os.path.exists(xml_path):
        return None
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError:
        return None
    document = root.find("document")
    if document is None:
        return None
        
    processed_text_parts = []

    for passage in document.findall("passage"):
        passage_type = _infon(passage, "type").upper()
        section_type = _infon(passage, "section_type").upper()
        if passage_type in exclude_sections or section_type in exclude_sections:
            continue
        text_element = (passage.findtext("text") or "").strip()
        if not text_element:
            continue
        if passage_type.startswith("TITLE"):
            level_match = re.search(r"TITLE[_\s]*([0-9]+)", _infon(passage, "type"), re.IGNORECASE)
            level = int(level_match.group(1)) if level_match else 1
            if level <= 2:
                header_prefix = "#" * level + " "
                processed_text_parts.append(header_prefix + text_element.upper())
            else:
                processed_text_parts.append(text_element.upper())
            continue
        if passage_type == "ABSTRACT":
            processed_text_parts.append("# ABSTRACT")
        processed_text_parts.append(text_element)

    if not processed_text_parts:
        return None
    out = "\n\n".join(processed_text_parts)
    return out

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("xml")
    ap.add_argument("--print-output", action="store_true", help="Print the loaded text to the console")
    args = ap.parse_args()
    txt = load_xml(args.xml)
    if txt and args.print_output:
        print(txt)