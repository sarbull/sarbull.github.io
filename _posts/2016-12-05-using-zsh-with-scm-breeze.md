---
title: "Using Oh My Zsh with SCM Breeze for Git shortcuts"
description: "Set up Oh My Zsh with the Frisk theme and SCM Breeze, then use numbered file shortcuts to stage changes in Git."
author: "sarbull"
tags: [developer-tools, git]
image: "/frisk-theme.png"
---

Oh My Zsh manages Zsh configuration and themes. SCM Breeze adds numbered Git file shortcuts, so you can stage files by number instead of typing their paths. These are my setup notes for combining the two tools with the Frisk theme.

## Install Oh My Zsh

See the [Oh My Zsh installation instructions](https://ohmyz.sh/#install) for the supported installer and prerequisites.

```bash
$ sudo apt-get install zsh # for Ubuntu
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
$ vim ~/.zshrc # ZSH_THEME="frisk"
```

### "Frisk" theme
![Git branch and working directory in the Oh My Zsh Frisk theme]({{ "/frisk-theme.png" | relative_url }}){: width="654" height="374" loading="lazy" decoding="async" }

## scm_breeze
[SCM Breeze](https://github.com/scmbreeze/scm_breeze) is a set of shell scripts for Bash and Zsh that adds shortcuts for working with Git.

### Installing scm_breeze
```bash
$ git clone https://github.com/scmbreeze/scm_breeze.git ~/.scm_breeze
$ ~/.scm_breeze/install.sh
```
### Example scm_breeze commands
```bash
$ mkdir test
$ cd test
$ git init
$ touch file{1..4}.txt
$ gs
# On branch: master
#
> Untracked files
#
#      untracked:  [1] file1.txt 
#      untracked:  [2] file2.txt 
#      untracked:  [3] file3.txt 
#
$ git add 1-3
$ gs
# On branch: master
#
> Changes to be committed
#
#       new file:  [1] file1.txt 
#       new file:  [2] file2.txt 
#       new file:  [3] file3.txt 
#
> Untracked files
#
#      untracked:  [4] file4.txt 
#
```
