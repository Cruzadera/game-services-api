from github import Github
import os

# Usa MY_GITHUB_PAT si existe, sino usa GITHUB_TOKEN
token = os.environ.get("MY_GITHUB_PAT") or os.environ.get("GITHUB_TOKEN")
repo_name = os.environ.get("GITHUB_REPOSITORY")
g = Github(token)
repo = g.get_repo(repo_name)

# Obtener PR cerradas con fusión que tengan como base main y develop
merged_prs = []
# Primero, los PRs fusionados hacia main
for pr in repo.get_pulls(state='closed', base='main'):
    if pr.is_merged():
        merged_prs.append(pr)

# Luego, los PRs fusionados hacia develop
for pr in repo.get_pulls(state='closed', base='develop'):
    if pr.is_merged():
        merged_prs.append(pr)

# Además, puedes buscar merges de ramas feature en develop (PRs cuyo base es develop)
for pr in repo.get_pulls(state='closed', base='develop'):
    if pr.is_merged() and 'feature' in pr.head.ref:
        merged_prs.append(pr)

# Ordenar las PR fusionadas por fecha de fusión (más recientes primero)
merged_prs = sorted(merged_prs, key=lambda pr: pr.merged_at, reverse=True)

changelog_content = "# CHANGELOG\n\n"

for pr in merged_prs:
    branch = pr.head.ref
    # Reemplaza "/" por "-" para formar el nombre del archivo
    branch_filename = branch.replace("/", "-")
    changelog_content += f"## PR #{pr.number}: {pr.title}\n"
    comic_path = f"comics/{branch_filename}.png"
    if os.path.exists(comic_path):
        changelog_content += f"![Cómic {branch}]({comic_path})\n\n"
    else:
        changelog_content += f"*No se encontró cómic para la rama {branch}*\n\n"

with open("CHANGELOG.md", "w", encoding="utf-8") as f:
    f.write(changelog_content)