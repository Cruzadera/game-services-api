from github import Github
import os
from collections import defaultdict

# Autenticación
token = os.environ.get("MY_GITHUB_PAT") or os.environ.get("GITHUB_TOKEN")
repo_name = os.environ.get("GITHUB_REPOSITORY")
g = Github(token)
repo = g.get_repo(repo_name)

# Obtener PRs fusionados en develop y main
merged_prs = []
seen_prs = set()

for branch in ["main", "develop"]:
    for pr in repo.get_pulls(state='closed', base=branch):
        if pr.is_merged() and pr.number not in seen_prs:
            merged_prs.append(pr)
            seen_prs.add(pr.number)

# Ordenar por fecha de merge
merged_prs.sort(key=lambda pr: pr.merged_at, reverse=True)

# Agrupar por tipo conventional (feat, fix, chore, etc.)
sections = defaultdict(list)

for pr in merged_prs:
    title = pr.title
    branch = pr.head.ref
    branch_filename = branch.replace("/", "-")
    comic_path = f"comics/{branch_filename}.png"

    if ":" in title:
        commit_type, message = title.split(":", 1)
        commit_type = commit_type.strip().lower()
        message = message.strip()
    else:
        commit_type = "otros"
        message = title

    merged_date = pr.merged_at.strftime("%-d %b %Y")
    entry = f"- **PR #{pr.number}**: {message} _({merged_date})_"

    if os.path.exists(comic_path):
        entry += f"\n  ![Cómic]({comic_path})"

    sections[commit_type].append(entry)

# Construir el contenido del CHANGELOG
changelog_content = "# 📝 CHANGELOG\n\n"

emoji_map = {
    "feat": "✨ Features",
    "fix": "🐛 Fixes",
    "chore": "🧹 Chores",
    "refactor": "🔧 Refactors",
    "test": "🧪 Tests",
    "otros": "📌 Others"
}

for commit_type, entries in sections.items():
    title = emoji_map.get(commit_type, commit_type.capitalize())
    changelog_content += f"## {title}\n\n"
    changelog_content += "\n".join(entries) + "\n\n"

# Guardar el archivo
with open("CHANGELOG.md", "w", encoding="utf-8") as f:
    f.write(changelog_content)