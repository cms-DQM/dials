# How to make a new release?

## Overview

This document outlines the steps involved in managing the release process of this project. Following these steps ensures a smooth transition from development to production.

## Contributors development phase

The following branch model should be followed in your own fork of this repository.

1. **Develop Branch**:
   - Start development from the `develop` branch.
   - Work on general new features and bug fixes without affecting the stable `main` branch.

2. **Refactor Branch**:
   - Create a `refactor/my-refactor` branch to address code refactoring.
   - Submit a PR and merge it into `develop` after review.

3. **Fix Branch**:
   - Create a `fix/issue-14` branch to solve an specific issues.
   - Submit a PR and merge it into `develop` after review.

4. **Feature Branch**:
   - Create a `feature/my-feature` branch for adding new functionality.
   - Submit a PR and merge it into `develop` after review.

## Maintainer release phase

The following branch model should be followed in this repository by one of the maintainers.

1. **Release Branch**:
   - Create a `release/1.1.X` branch from `develop` depending on the next release version.

2. **Test the Release Candidate**:
   - Thoroughly test the `release/1.1.X` branch.
   - Ensure all features work as expected.

Notify any contributors working in the latest release that they can address any last minute modifications creating new branches in their own fork from `release/1.1.X` branch and PR into this branch.

## Finishing the release

The following steps should be followed in this repository by one of the maintainers.

- Update relevant documentation not yer addressed.
- Increment the version number in `__version__.txt` (e.g. `1.1.0`).
- Create a new tag (e.g. `v1.1.0`) for the release.

```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push --tags
```

- Merge the `release/1.1.X` branch into the `main` branch.
- Merge the `release/1.1.X` branch into the `develop` branch.
- Deploy the code from the `main` branch to production
