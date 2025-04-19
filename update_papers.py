# update_papers.py
import feedparser

ARXIV_CATEGORIES = {
    "AI": "cs.AI",
    "Healthcare": "cs.CY",
    "ML": "cs.LG"
}

def fetch_arxiv(category, max_results=3):
    feed = feedparser.parse(f"http://export.arxiv.org/api/query?search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}")
    entries = []
    for entry in feed.entries:
        paper_id = entry.id.split('/abs/')[-1]
        pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
        paper = {
            "title": entry.title.strip(),
            "url": entry.link,
            "pdf": pdf_url,
        }
        entries.append(paper)
    return entries

def build_markdown():
    lines = ["### 🌐 Latest Research on Cutting-Edge Tech in CS & AI (🇺🇸 USA & 🇨🇳 China)\n"]
    for field, cat in ARXIV_CATEGORIES.items():
        lines.append(f"**{field}**")
        papers = fetch_arxiv(cat)
        for p in papers:
            lines.append(f"- [{p['title']}]({p['url']}) [📄 PDF]({p['pdf']})")
        lines.append("")
    return "\n".join(lines)

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    start = content.find("<!--START-RESEARCH-->")
    end = content.find("<!--END-RESEARCH-->")
    if start != -1 and end != -1:
        new_content = content[:start+21] + "\n" + build_markdown() + "\n" + content[end:]
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)

if __name__ == "__main__":
    update_readme()
