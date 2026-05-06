from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class JobConfig:
    name: str
    repo_url: str
    branch_regex: str
    credentials_id: str
    script_id: str


@dataclass
class FolderConfig:
    name: str
    jobs: list[JobConfig]


@dataclass
class JenkinsFactoryConfig:
    root_folder: str
    folders: list[FolderConfig]


def load_config(path: str) -> JenkinsFactoryConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))

    defaults: dict[str, Any] = raw.get("defaults", {})

    folders = []

    for folder in raw["folders"]:
        jobs = []

        for job in folder.get("jobs", []):
            jobs.append(
                JobConfig(
                    name=str(job["name"]).strip(),
                    repo_url=str(job["repo_url"]).strip(),
                    branch_regex=job.get(
                        "branch_regex",
                        defaults.get("branch_regex", "^(?:dev|qa|main|master)$"),
                    ),
                    credentials_id=job.get(
                        "credentials_id",
                        defaults.get("credentials_id"),
                    ),
                    script_id=job.get(
                        "script_id",
                        defaults.get("script_id"),
                    ),
                )
            )

        folders.append(FolderConfig(name=str(folder["name"]).strip(), jobs=jobs))

    return JenkinsFactoryConfig(
        root_folder=str(raw["root_folder"]).strip(),
        folders=folders,
    )