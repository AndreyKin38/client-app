import json
from dataclasses import dataclass

from backend.repository import ClientRepository, ClientCache
from backend.schemas import Form


@dataclass
class ClientService:
    client_repository: ClientRepository
    client_cache: ClientCache

    def get_client(self, id_client) -> Form | str:
        if client_data := self.client_cache.get_client_data(id_client):
            return Form(**json.loads(client_data))

        client_data = self.client_repository.get_client_data(id_client)
        self.client_cache.set_client_data(client_data)
        return client_data
