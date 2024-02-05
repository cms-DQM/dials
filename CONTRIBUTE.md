# How to Contribute

Welcome fellow contributors! We're thrilled that you want to join our open-source project. This guide outlines best practices for contributing code while following semantic commit messages to keep our repository well organized and maintainable.

## Setting up Your Environment

First, ensure you have the necessary dependencies installed, as described in our `README`. Once you've configured your development environment successfully, create a fork of the original repo on GitHub to avoid modifying the main branch directly.

## Developing Features and Fixes

When starting new features or bug fixes, create an isolated branch for your work using the following format:

```bash
git checkout -b feature/<brief_description>  # For adding a new feature
git checkout -b fix/<bug_number>-<brief_summary>  # For fixing an existing bug
```

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
