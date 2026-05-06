import argparse
import os
import sys

from dotenv import load_dotenv

from jenkins_job_factory.client import JenkinsClient
from jenkins_job_factory.config import load_config
from jenkins_job_factory.xml_templates import folder_xml, multibranch_xml


def get_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Falta variable de entorno: {name}")

    return value


def ensure_folder(client: JenkinsClient, parent_path: list[str], folder_name: str) -> None:
    full_path = parent_path + [folder_name]

    if client.exists(*full_path):
        print(f"[OK] Folder ya existe: {'/'.join(full_path)}")
        return

    client.create_item(
        parent_path=parent_path,
        name=folder_name,
        xml=folder_xml(folder_name),
    )

    print(f"[CREATED] Folder creada: {'/'.join(full_path)}")


def ensure_multibranch(
    client: JenkinsClient,
    folder_path: list[str],
    job_name: str,
    repo_url: str,
    credentials_id: str,
    script_id: str,
    branch_regex: str,
    scan: bool,
) -> None:
    full_path = folder_path + [job_name]

    if client.exists(*full_path):
        print(f"[OK] Job ya existe: {'/'.join(full_path)}")
        return

    xml = multibranch_xml(
        job_name=job_name,
        repo_url=repo_url,
        credentials_id=credentials_id,
        script_id=script_id,
        branch_regex=branch_regex,
    )

    client.create_item(
        parent_path=folder_path,
        name=job_name,
        xml=xml,
    )

    print(f"[CREATED] Multibranch creado: {'/'.join(full_path)}")

    if scan:
        client.trigger_scan(*full_path)
        print(f"[SCAN] Scan ejecutado: {'/'.join(full_path)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Jenkins Multibranch Job Factory"
    )

    parser.add_argument(
        "-c",
        "--config",
        default="jobs.yml",
        help="Archivo YAML de configuración",
    )

    parser.add_argument(
        "--no-scan",
        action="store_true",
        help="No ejecutar Scan Multibranch Pipeline Now después de crear cada job",
    )

    args = parser.parse_args()

    load_dotenv()

    client = JenkinsClient(
        base_url=get_env("JENKINS_URL"),
        user=get_env("JENKINS_USER"),
        token=get_env("JENKINS_TOKEN"),
    )

    config = load_config(args.config)

    scan_enabled = not args.no_scan

    ensure_folder(client, [], config.root_folder)

    for folder in config.folders:
        root_path = [config.root_folder]

        ensure_folder(client, root_path, folder.name)

        target_path = [config.root_folder, folder.name]

        for job in folder.jobs:
            ensure_multibranch(
                client=client,
                folder_path=target_path,
                job_name=job.name,
                repo_url=job.repo_url,
                credentials_id=job.credentials_id,
                script_id=job.script_id,
                branch_regex=job.branch_regex,
                scan=scan_enabled,
            )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        sys.exit(1)
