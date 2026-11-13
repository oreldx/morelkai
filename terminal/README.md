# morelkai — Ghostty, Herdr, Zsh et Claude Code

Les deux palettes reprennent les thèmes VS Code du dépôt : fond bleu nuit et accents Monokai pour **night**, fond gris bleuté et accents plus foncés pour **day**. Les 16 couleurs ANSI de Ghostty sont identiques à celles du terminal intégré de VS Code. La sélection semi-transparente de VS Code est composée sur son fond pour Ghostty.

## Bascule automatique

La chaîne est : **apparence macOS → Ghostty → Herdr et prompt Zsh**.

- Ghostty choisit sa palette avec `theme = light:…,dark:…` selon l'apparence du système.
- Herdr suit l'apparence signalée par le terminal avec `auto_switch = true`, puis applique `theme.custom.light` ou `theme.custom.dark`.
- Le prompt Zsh utilise les couleurs ANSI du terminal : il suit leur changement sans script de surveillance ni détection macOS dans chaque shell.
- Claude Code ne bascule pas : un thème personnalisé est choisi seul, sans paire clair/sombre. Voir [Claude Code](#4-claude-code).

Les options Herdr sont présentes dans la configuration par défaut du binaire local **0.9.3**. En l'absence de détection d'apparence, les couleurs partagées fournissent un repli sombre. Le changement effectif dans les fenêtres ouvertes reste à vérifier dans une session interactive.

## Installation

Exécuter les commandes depuis la racine de ce dépôt. Elles copient les fichiers de thème ; fusionner ensuite les réglages indiqués dans les configurations existantes.

### 1. Ghostty

```sh
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/themes"
cp "terminal/ghostty/morelkai night" "terminal/ghostty/morelkai day" \
  "${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/themes/"
```

Dans la configuration ouverte via **Ghostty → Settings**, remplacer l'éventuelle ligne `theme` par :

```ini
theme = light:morelkai day,dark:morelkai night
window-theme = system
```

Retirer les éventuels réglages de couleurs directement définis dans cette configuration (`background`, `foreground`, `palette`, sélection et curseur) s'ils écrasent les thèmes. Recharger la configuration depuis Ghostty. Les fichiers de thème doivent rester dans le dossier `themes` ci-dessus, même si macOS utilise un autre emplacement pour le fichier de configuration principal.

Pour fixer un mode, utiliser seulement `theme = morelkai night` ou `theme = morelkai day`.

### 2. Herdr

Fusionner le contenu de [`herdr/morelkai.toml`](herdr/morelkai.toml) dans `~/.config/herdr/config.toml`. Si des tables `[theme]` ou `[theme.custom…]` existent déjà, les remplacer ; TOML n'autorise pas à déclarer deux fois une même table. Conserver les autres sections du fichier.

Le thème de base utilise les noms intégrés `catppuccin` et `catppuccin-latte` ; les couleurs personnalisées les remplacent avec les palettes morelkai. Ces noms ne désignent donc pas des fichiers de thème à installer séparément.

Recharger depuis le menu global Herdr, action **reload config**. La commande suivante est également disponible :

```sh
herdr server reload-config
```

Le menu recharge explicitement les réglages du client local et ceux du serveur sélectionné, ce qui est utile avec un serveur distant. Une sélection manuelle de thème dans les Settings Herdr désactive `auto_switch` ; réactiver cette option dans le fichier si nécessaire.

Le fichier Herdr colore son interface. Les fonds et les 16 couleurs ANSI des terminaux viennent de Ghostty.

### 3. Oh My Zsh

```sh
mkdir -p "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes"
cp terminal/zsh/morelkai.zsh-theme \
  "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/morelkai.zsh-theme"
```

Dans `~/.zshrc`, remplacer `ZSH_THEME="half-life"` par cette ligne, avant le chargement d'Oh My Zsh :

```zsh
ZSH_THEME="morelkai"
```

Ouvrir un nouveau shell. Le prompt affiche :

```text
orel@machine ~/projet main * (venv)
% commande
```

Le chemin est cyan, l'utilisateur et la branche violets, `*` jaune signale les changements Git, y compris les fichiers non suivis. Le symbole est vert après une réussite ; après une erreur, il devient rouge et affiche le code de sortie. Le prompt utilise deux lignes et ne nécessite aucune police spéciale. Le contexte Python est affiché si `VIRTUAL_ENV` ou `CONDA_DEFAULT_ENV` est défini.

Sans Oh My Zsh, ajouter en fin de `~/.zshrc` un `source` vers le chemin absolu du fichier `terminal/zsh/morelkai.zsh-theme` de ce dépôt. Le thème se suffit à lui-même. Il désactive `prompt_subst` pour afficher les noms de branches comme du texte ; charger ce thème après tout autre outil qui remplace le prompt.

Pour tester temporairement dans le shell courant, depuis le dépôt :

```zsh
source ./terminal/zsh/morelkai.zsh-theme
```

Quitter ce shell restaure la configuration habituelle. Dans un autre terminal que Ghostty, le prompt utilise la palette de cet autre terminal.

### 4. Claude Code

```sh
mkdir -p ~/.claude/themes
cp terminal/claude/morelkai-night.json terminal/claude/morelkai-day.json ~/.claude/themes/
```

Dans Claude Code, lancer `/theme` et choisir **morelkai night** ou **morelkai day** en fin de liste. La préférence est enregistrée sous la forme `custom:morelkai-night` ou `custom:morelkai-day`. Si le dossier `~/.claude/themes` vient d'être créé, redémarrer Claude Code une fois ; ensuite, les fichiers modifiés sont rechargés à chaud.

Le fond vient du terminal : Claude Code ne colore que son interface. Les thèmes partent des préréglages `dark` et `light` et en remplacent les accents : violet pour Claude et les compteurs, cyan pour les demandes de permission et le mode plan, rose Monokai pour les commandes `!`, vert, jaune et rouge pour les statuts. Les fonds de diff composent les couleurs de `diffEditor` de VS Code sur le fond du terminal, et les fonds de messages reprennent les surfaces de Herdr.

Un thème personnalisé ne suit pas l'apparence macOS, contrairement au préréglage `auto` de Claude Code. Changer de variante avec `/theme` lors d'une bascule clair/sombre.

## Vérification visuelle

1. Ouvrir une fenêtre Ghostty avec le prompt, puis lancer Herdr.
2. Basculer l'apparence macOS entre clair et sombre : le fond et les accents de Ghostty et de Herdr doivent suivre.
3. Quitter Herdr : le prompt doit toujours utiliser la palette active.
4. Exécuter `false` : le prompt suivant affiche `1` en rouge. Exécuter `true` : il redevient vert.

## Mettre les palettes à jour

Après modification des couleurs des thèmes VS Code :

```sh
python3 scripts/export-terminal-themes.py
```

Le script n'utilise que la bibliothèque standard Python. Il régénère les deux fichiers Ghostty, le fichier Herdr et les deux thèmes Claude Code, sans modifier de configuration personnelle. Recopier ensuite les palettes et fusionner la section Herdr actualisée.

Références : [thèmes Herdr](https://herdr.dev/docs/configuration/#theme), [options Herdr](https://herdr.dev/docs/config-reference/), [thèmes Ghostty](https://ghostty.org/docs/config/reference#theme).
