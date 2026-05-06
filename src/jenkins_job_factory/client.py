from urllib.parse import quote

import requests


class JenkinsClient:
    def __init__(self, base_url: str, user: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = (user, token)

    def path(self, *items: str) -> str:
        parts = []

        for item in items:
            parts.append("job")
            parts.append(quote(item, safe=""))

        return "/" + "/".join(parts) if parts else ""

    def exists(self, *items: str) -> bool:
        url = f"{self.base_url}{self.path(*items)}/api/json"

        response = self.session.get(url, timeout=30)

        if response.status_code == 200:
            return True

        if response.status_code == 404:
            return False

        raise RuntimeError(
            f"Error consultando {'/'.join(items)}: "
            f"{response.status_code} - {response.text}"
        )

    def create_item(self, parent_path: list[str], name: str, xml: str) -> None:
        if parent_path:
            url = f"{self.base_url}{self.path(*parent_path)}/createItem?name={quote(name, safe='')}"
        else:
            url = f"{self.base_url}/createItem?name={quote(name, safe='')}"

        response = self.session.post(
            url,
            headers={"Content-Type": "application/xml"},
            data=xml.encode("utf-8"),
            timeout=30,
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(
                f"No se pudo crear {'/'.join(parent_path + [name])}: "
                f"{response.status_code} - {response.text}"
            )

    def trigger_scan(self, *items: str) -> None:
        url = f"{self.base_url}{self.path(*items)}/build?delay=0"

        response = self.session.post(url, timeout=30)

        if response.status_code not in (200, 201, 202):
            raise RuntimeError(
                f"No se pudo lanzar scan de {'/'.join(items)}: "
                f"{response.status_code} - {response.text}"
            )