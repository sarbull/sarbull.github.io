---
title: "My VS Code settings.json configuration"
description: "My VS Code settings for two-space indentation, autosave, editor navigation, JavaScript formatting, and the Monokai Pro theme."
author: "sarbull"
tags: [developer-tools]
image: "/my-vscode-extentions-list.png"
---

This is my VS Code `settings.json` configuration. It uses two-space indentation, autosave, visible whitespace, 80- and 120-character rulers, and Prettier for JavaScript formatting. Some entries depend on extensions, including Monokai Pro and ESLint.

To apply individual settings, open your user or workspace `settings.json` and merge the entries you want to use. The [VS Code settings guide](https://code.visualstudio.com/docs/configure/settings) explains how user and workspace settings interact.

## VS Code settings.json
```json
{
  "editor.acceptSuggestionOnCommitCharacter": false,
  "editor.autoClosingBrackets": "never",
  "editor.autoIndent": "keep",
  "editor.detectIndentation": false,
  "editor.insertSpaces": true,
  "editor.minimap.enabled": true,
  "editor.renderWhitespace":"all",
  "editor.rulers": [
    80,
    120
  ],
  "editor.showUnused": true,
  "editor.tabSize": 2,
  "editor.trimAutoWhitespace": true,
  "emmet.triggerExpansionOnTab": true,
  "explorer.autoReveal": false,
  "explorer.compactFolders": false,
  "explorer.confirmDelete": false,
  "explorer.confirmDragAndDrop": false,
  "extensions.ignoreRecommendations": true,
  "files.autoSaveDelay": 0,
  "files.exclude": {
    "**/.DS_Store": true,
    "**/.git": false,
    "**/.hg": true,
    "**/.svn": true,
    "**/CVS": true
  },
  "files.trimTrailingWhitespace": true,
  "javascript.updateImportsOnFileMove.enabled": "never",
  "typescript.updateImportsOnFileMove.enabled": "never",
  "workbench.startupEditor": "newUntitledFile",
  "files.autoSave": "afterDelay",
  "diffEditor.hideUnchangedRegions.enabled": true,
  "workbench.editor.enablePreview": false,
  "editor.gotoLocation.multipleDefinitions": "goto",
  "editor.gotoLocation.multipleTypeDefinitions": "goto",
  "workbench.colorTheme": "Monokai Pro",
  "window.zoomLevel": 0.07,
  "workbench.iconTheme": "Monokai Pro Icons",
  "git.autofetch": true,
  "terminal.integrated.tabs.location": "left",
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "eslint.workingDirectories": ["ui"]
}
```

## VS Code extensions list

![Extensions installed in my VS Code development environment]({{ "/my-vscode-extentions-list.png" | relative_url }}){: width="1434" height="1016" loading="lazy" decoding="async" }

For terminal configuration, see [using Oh My Zsh with SCM Breeze]({% post_url 2016-12-05-using-zsh-with-scm-breeze %}).
