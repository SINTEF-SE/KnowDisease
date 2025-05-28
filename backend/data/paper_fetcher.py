import os
import time

from Bio import Entrez, Medline

from xml_fetcher import save_xml

SUBHEADINGS = [
    "etiology[sh]",
    "pathology[sh]",
    "genetics[sh]",
    "complications[sh]",
    "diagnosis[sh]",
    "therapy[sh]",
    "pathogenesis[sh]",
    "physiopathology[sh]"
]

def build_query(disease, *, require_full_text, pubtypes):
    if not disease or not disease.strip():
        raise ValueError("Disease parameter cannot be empty")
    
    parts = [f"{disease}[majr]"]
    parts.append("(" + " OR ".join(SUBHEADINGS) + ")")
    theory_terms = "(pathogenesis OR mechanism OR pathway OR model OR theory OR framework OR biomarker OR prognosis OR outcome)"
    parts.append(theory_terms)

    if pubtypes:
        pt_query = "(" + " OR ".join(f"{pt}[pt]" for pt in pubtypes) + ")"
        parts.append(pt_query)

    if require_full_text:
        parts.append("(free full text[Filter])")

    return " AND ".join(parts)

def entrez_search(query, max_results):
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="relevance")
    record = Entrez.read(handle)
    handle.close()
    return record.get("IdList", [])


def download_xmls(pmids, out_dir, delay=0.5):
    os.makedirs(out_dir, exist_ok=True)
    total_pmids = len(pmids)
    for idx, pmid in enumerate(pmids, 1):
        print(f"[{idx}/{total_pmids}] Downloading {pmid}...", end=" ")
        fname = os.path.join(out_dir, f"{pmid}_ascii_pmcoa.xml")
        if os.path.exists(fname):
            print("exists")
        else:
            res = save_xml(pmid, folder=out_dir, source="pmcoa")
            print("ok" if res == 1 else "fail")
        time.sleep(delay)


def fetch_disease_papers(
    disease,
    max_results,
    publication_types,
    require_full_text,
    out_dir,
    delay,
):

    query = build_query(disease, require_full_text=require_full_text, pubtypes=publication_types or [])
    print("[query]", query)

    pmids = entrez_search(query, max_results=max_results)
    print(f"[search] Retrieved {len(pmids)} PMIDs")

    if not pmids:
        return []

    download_xmls(pmids, out_dir, delay)
    return pmids

def main():
    disease = "Cystic Fibrosis"
    max_results = 10
    require_full_text = True
    publication_types = ["Review", "Systematic Review", "Meta-analysis", "Guideline"]
    out_dir = "./downloaded_papers"
    delay = 0.5
    
    email = os.environ.get("ENTREZ_EMAIL", "isak.w.midtvedt@gmail.com")
    
    if not email:
        print("ERROR: Please set Entrez email via ENTREZ_EMAIL env var.")
        return

    Entrez.email = email
    print(f"[Entrez] Email set to: {email}")

    pmids = fetch_disease_papers(
        disease,
        max_results=max_results,
        publication_types=publication_types,
        require_full_text=require_full_text,
        out_dir=out_dir,
        delay=delay,
    )
    print("[main] Done -", len(pmids), "PMIDs processed for", out_dir)


if __name__ == "__main__":
    main()