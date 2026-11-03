# morelkai — Codex

Les variantes **night** et **day** sont générées depuis les thèmes VS Code du dépôt. L'application utilise leurs fonds, textes, accents violets et couleurs des diffs. Le CLI reprend toutes leurs règles de coloration syntaxique, y compris les styles de police.

## Application Codex

Depuis la racine du dépôt, copier le thème sombre dans le presse-papiers sur macOS :

```sh
pbcopy < codex/app/morelkai-night.codex-theme
```

1. Ouvrir **Settings → Appearance** dans Codex.
2. Cliquer sur **Import** dans la section **Dark theme**.
3. Coller la chaîne entière commençant par `codex-theme-v1:` et valider.

Faire de même pour **Light theme** avec le thème clair :

```sh
pbcopy < codex/app/morelkai-day.codex-theme
```

Sur un autre système, copier directement le contenu du fichier correspondant. Chaque variante doit être importée dans sa section : un thème `dark` est refusé dans la section `light`, et inversement. Choisir ensuite **System** pour suivre l'apparence du système, ou fixer **Light** ou **Dark**.

L'import remet les polices UI et code sur les valeurs par défaut de Codex et désactive la transparence pour conserver les couleurs de fond. Les polices restent personnalisables après import.

### Coloration du code dans l'application

L'import de l'application accepte un identifiant de thème de code intégré, mais pas les règles TextMate personnalisées de Morelkai. **night** utilise donc **Monokai** et **day** utilise **One Light** (`codeThemeId: "one"`). Les couleurs du code dans l'application sont une approximation ; les couleurs de base de l'interface proviennent de Morelkai. Codex calcule lui-même les couleurs des panneaux, bordures et états à partir de ces couleurs de base et du contraste.

Les fichiers `.tmTheme` ci-dessous sont destinés au CLI et ne s'importent pas dans l'application.

## Codex CLI

Depuis la racine du dépôt :

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/themes"
cp codex/cli/morelkai-night.tmTheme codex/cli/morelkai-day.tmTheme \
  "${CODEX_HOME:-$HOME/.codex}/themes/"
```

Lancer ou relancer `codex`, exécuter `/theme`, puis choisir **morelkai-night (custom)** ou **morelkai-day (custom)**. Le choix est sauvegardé dans `tui.theme`. Il est aussi possible de fusionner ce réglage dans le `config.toml` de Codex :

```toml
[tui]
theme = "morelkai-night"
```

Utiliser `morelkai-day` pour la variante claire. Si une table `[tui]` existe, modifier sa clé `theme` au lieu de déclarer une deuxième table.

Ces thèmes règlent la coloration des blocs de code et des diffs. Le fond général et les couleurs ANSI du CLI dépendent du terminal : utiliser les [palettes Ghostty Morelkai](../terminal/README.md) pour harmoniser l'ensemble. Le choix d'un thème syntaxique personnalisé est fixe ; changer `/theme` lors d'un passage entre clair et sombre. La bascule automatique de Ghostty ne sélectionne pas une autre variante syntaxique dans Codex.

## Régénérer les fichiers

Après modification des thèmes VS Code :

```sh
python3 scripts/export-codex-themes.py
```

Le script utilise uniquement la bibliothèque standard Python. Il régénère les deux chaînes d'import et les deux fichiers TextMate, sans modifier la configuration personnelle de Codex.

## Vérification visuelle

Dans l'application, vérifier les deux modes : fond bleu nuit ou clair, texte lisible, accents violets et diffs verts/roses. Dans le CLI, prévisualiser chaque thème avec `/theme`, puis vérifier un bloc de code et un diff. Les chaînes d'import ciblent le schéma `codex-theme-v1` ; les règles TextMate du CLI préservent l'ordre, les scopes et les styles des thèmes sources.

Le chargement et la prévisualisation des deux thèmes ont été vérifiés avec Codex CLI **0.166.0**, dans une configuration temporaire. Le format des chaînes d'import a été vérifié contre le schéma de l'application installée ; l'import visuel dans l'application reste à confirmer manuellement.

Références : [apparence de l'application — documentation officielle OpenAI](https://learn.chatgpt.com/docs/reference/settings#appearance), [thèmes du CLI — documentation officielle OpenAI](https://learn.chatgpt.com/docs/cli-customization#syntax-highlighting-and-themes).
