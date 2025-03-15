from github import Github
import os

# Obtener el token y la información del repositorio desde las variables de entorno de GitHub Actions
token = os.environ.get("GITHUB_TOKEN")
repo_name = os.environ.get("GITHUB_REPOSITORY")
g = Github(token)
repo = g.get_repo(repo_name)

# Obtener todas las pull requests abiertas
prs = repo.get_pulls(state='open')
changelog_content = "# CHANGELOG\n\n"

for pr in prs:
    changelog_content += f"## PR #{pr.number}: {pr.title}\n"
    branch = pr.head.ref
    # Supongamos que cada rama tiene un cómic en la carpeta 'comics' con el nombre {branch}.png
    comic_path = f"comics/{branch}.png"
    if os.path.exists(comic_path):
        changelog_content += f"![Cómic {branch}]({comic_path})\n\n"
    else:
        changelog_content += f"*No se encontró cómic para la rama {branch}*\n\n"

# Sobrescribir o crear el CHANGELOG.md con el contenido actualizado
with open("CHANGELOG.md", "w", encoding="utf-8") as f:
    f.write(changelog_content)