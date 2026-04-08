#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path


VERSION_FILE = Path("tchat/version.py")
VERSION_PATTERN = r'VERSION\s*=\s*"v(\d+)\.(\d+)\.(\d+)"'


def main() -> None:
    ensure_git_clean()

    current = get_current_version()
    bump_type = detect_bump_type()
    new_tuple = bump_version(current, bump_type)
    new_version = write_version(new_tuple)

    if tag_exists(new_version):
        raise SystemExit(f"Tag already exists: {new_version}")

    run(["git", "add", str(VERSION_FILE)])
    run(["git", "commit", "--amend", "--no-edit"])
    run(["git", "tag", new_version])

    print(f"Detected bump: {bump_type}")
    print(f"Released {new_version}")
    print("Now push with:")
    print("  git push --force")
    print("  git push --tags")


def detect_bump_type() -> str:
    last_tag = get_last_tag()
    commit_subjects = get_commit_subjects_since(last_tag)

    if not commit_subjects:
        raise SystemExit(f"No commits since {last_tag}")

    if has_major_bump(commit_subjects, last_tag):
        return "major"
    if has_minor_bump(commit_subjects):
        return "minor"
    if has_patch_bump(commit_subjects):
        return "patch"

    raise SystemExit(
        "No version bump needed "
        "(only chore/test commits since last tag)"
    )


def has_major_bump(commit_subjects: list[str], last_tag: str) -> bool:
    body = get_commit_bodies_since(last_tag)
    if "BREAKING CHANGE" in body:
        return True

    return any(is_breaking_subject(subject) for subject in commit_subjects)


def has_minor_bump(commit_subjects: list[str]) -> bool:
    return any(matches_type(subject, "feat") for subject in commit_subjects)


def has_patch_bump(commit_subjects: list[str]) -> bool:
    patch_types = ("fix", "refactor", "core", "del")
    return any(
        any(matches_type(subject, commit_type) for commit_type in patch_types)
        for subject in commit_subjects
    )


def is_breaking_subject(subject: str) -> bool:
    return re.match(
        r"^[a-zA-Z]+(?:\(\s*[^)]+\s*\))?!\s*:",
        subject,
    ) is not None


def matches_type(subject: str, commit_type: str) -> bool:
    pattern = rf"^{re.escape(commit_type)}(?:\(\s*[^)]+\s*\))?\s*:"
    return re.match(pattern, subject) is not None


def get_last_tag() -> str:
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return "v0.0.0"
    return result.stdout.strip()


def get_commit_subjects_since(tag: str) -> list[str]:
    result = subprocess.run(
        ["git", "log", f"{tag}..HEAD", "--pretty=format:%s"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Failed to get git log subjects")

    return [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def get_commit_bodies_since(tag: str) -> str:
    result = subprocess.run(
        ["git", "log", f"{tag}..HEAD", "--pretty=format:%b"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Failed to get git log bodies")
    return result.stdout


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise SystemExit(f"Command failed: {' '.join(cmd)}")


def get_current_version() -> tuple[int, int, int]:
    content = VERSION_FILE.read_text(encoding="utf-8")
    match = re.search(VERSION_PATTERN, content)
    if not match:
        raise SystemExit(f"Could not find VERSION in {VERSION_FILE}")

    major, minor, patch = map(int, match.groups())
    return major, minor, patch


def write_version(version: tuple[int, int, int]) -> str:
    major, minor, patch = version
    new_version = f"v{major}.{minor}.{patch}"

    content = VERSION_FILE.read_text(encoding="utf-8")
    updated = re.sub(
        VERSION_PATTERN,
        f'VERSION = "{new_version}"',
        content,
    )
    VERSION_FILE.write_text(updated, encoding="utf-8")
    return new_version


def bump_version(
    current: tuple[int, int, int],
    bump_type: str,
) -> tuple[int, int, int]:
    major, minor, patch = current

    if bump_type == "patch":
        return major, minor, patch + 1
    if bump_type == "minor":
        return major, minor + 1, 0
    if bump_type == "major":
        return major + 1, 0, 0

    raise SystemExit(f"Invalid bump type: {bump_type}")


def ensure_git_clean() -> None:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("Failed to check git status")
    if result.stdout.strip():
        raise SystemExit("Git working tree is not clean")


def tag_exists(tag: str) -> bool:
    result = subprocess.run(
        ["git", "tag", "--list", tag],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() == tag


if __name__ == "__main__":
    main()
