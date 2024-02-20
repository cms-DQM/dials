# How to Contribute

Welcome fellow contributors! We're thrilled that you want to join our open-source project. This guide outlines best practices for contributing code while following semantic commit messages to keep our repository well organized and maintainable.

## Setting up Your Environment

First, ensure you have the necessary dependencies installed, as described in [`LOCAL DEVELOPMENT`](/docs/LOCAL_DEVELOPMENT.md). Once you've configured your development environment successfully, create a fork of the original repo on GitHub to avoid modifying the main branch directly.

## Git workflow

This project tries to always follow the Git flow branching model that you can read in more details [here](https://nvie.com/posts/a-successful-git-branching-model/). In general this methodology is based on three kind of branches: main (in the past also referred as master), develop and supporting branches (feature, hotfix, release).

* `main`: contain production-ready code that can be released.
* `develop`: contain pre-production code with newly developed features that are in the process of being tested.
* `feature`: contain feature-specific code, must always start from `develop` and be merged back to it.
* `hotfix`: quickly address necessary changes in `main` branch, should always start from `main` anb be merge back into both the `main` and `develop`.
* `release`: used to prepare new production releases.

## Committing

Always ensure you write descriptive commit messages adhering to the [Conventional Commits](https://www.conventionalcommits.org/) standard:

* `build:` for changes that affect build scripts, configuration files or dependencies but don't alter functionality.
* `ci:` for continuous integration changes unrelated to code modifications.
* `docs:` for documentation updates.
* `feat:` for new features.
* `fix:` for bug fixes.
* `perf:` for improvements regarding performance, but without changing external behavior.
* `refactor:` when refactoring code without introducing functional changes.
* `test:` for testing framework alterations or additions not affecting code functionality directly.
* `style:` for updating code formatting, indentation or similar aesthetic changes without impacting functionality.
* `chore:` for updating supporting development environments, like modifying `.gitignore` files or managing dependencies but not affecting code functionality.

Your commit message should comprise a type, an optional scope (either a file path relative to the repo root or subject area), a concise description starting with a capital letter, and an optional body section for more extensive explanations when necessary. Here's an example:

```bash
git commit -m "fix: login page broken links after recent updates  # Fixes #37"
```
