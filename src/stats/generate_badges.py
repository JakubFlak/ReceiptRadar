import json
from pathlib import Path

data = json.loads(Path("data/stats/project_stats.json").read_text())

badges = {
    "receipts": ("receipts", data["receipts"], "blue"),
    "products": ("products", data["products"], "green"),
    "stores": ("stores", data["stores"], "purple"),
    "data_freshness": ("data_freshness", data["data_freshness"].replace("-", "."), "orange"),
}

readme_path = Path("README.md")
readme = readme_path.read_text()

badge_lines = []
for key, (label, value, color) in badges.items():
    url = f"https://img.shields.io/badge/{label}-{value}-{color}"
    badge_lines.append(f"![{key}]({url})")

badge_block = "\n".join(badge_lines)

start = "<!-- BADGES_START -->"
end = "<!-- BADGES_END -->"

old_block = readme[
    readme.index(start):readme.index(end) + len(end)
]

new_block = (
    f"{start}\n"
    f"{badge_block}\n"
    f"{end}"
)

new_readme = readme.replace(old_block, new_block)

readme_path.write_text(new_readme)