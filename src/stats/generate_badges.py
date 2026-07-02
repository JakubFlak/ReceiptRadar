import json
from pathlib import Path

data = json.loads(Path("data/stats/project_stats.json").read_text())

badges = {
    "receipts": ("receipts", data["receipts"], "blue"),
    "products": ("products", data["products"], "green"),
    "stores": ("stores", data["stores"], "purple"),
    "data_freshness": ("freshness", data["data_freshness"], "orange"),
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

new_readme = readme.split(start)[0] + \
              start + "\n" + \
              badge_block + "\n" + \
              end

readme_path.write_text(new_readme)