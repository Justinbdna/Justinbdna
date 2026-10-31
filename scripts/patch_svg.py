import glob
import re

def patch_svgs():
    svg_files = glob.glob("profile-3d-contrib/*.svg")
    if not svg_files:
        print("Aucun fichier SVG trouvé.")
        return

    translations = {
        r'>other<': '>Autres<',
        r'<title>other ': '<title>Autres ',
        r'>Commit<': '>Commits<',
        r'>Issue<': '>Tickets<',
        r'>PullReq<': '>Pull Requests<',
        r'>Review<': '>Revues<',
        r'>Repo<': '>Dépôts<',
    }

    # Icône repo SVG et affichage '12 dépôts'
    repo_icon_path = (
        '<g transform="translate(555, 802), scale(2)">'
        '<path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1h-8a1 1 0 00-1 1v6.708A2.486 2.486 0 014.5 9h8V1.5z" fill="{color}"></path>'
        '</g>'
        '<text style="font-size: 32px; font-weight: bold;" x="595" y="830" text-anchor="start" fill="{color}">12 <tspan style="font-size: 24px; font-weight: normal;">dépôts</tspan><title>12 dépôts</title></text>'
    )

    for path in svg_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Détection de la couleur du texte/icône
        color_match = re.search(r'fill="([^"]+)">contributions', content) or re.search(r'fill="([^"]+)"', content)
        color = color_match.group(1) if color_match else "#000000"

        # Remplacement de l'étoile et du 0 par 12 dépôts
        content = re.sub(
            r'<g transform="translate\((?:608|555), 802\), scale\(2\)">.*?</text>',
            repo_icon_path.format(color=color),
            content,
            flags=re.DOTALL
        )

        # Décalage de l'icône Fork pour éviter le chevauchement
        content = re.sub(
            r'translate\(736, 802\)',
            'translate(755, 802)',
            content
        )
        content = re.sub(
            r'x="772" y="830"',
            'x="791" y="830"',
            content
        )

        # Application des traductions
        for pattern, replacement in translations.items():
            content = re.sub(pattern, replacement, content)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    print("SVG patchés avec succès.")

if __name__ == "__main__":
    patch_svgs()
