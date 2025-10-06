from redis import Redis
from backend.schemas import Form


class ClientCache:

    def __init__(self, redis: Redis):
        self.redis = redis

    def get_client_data(self, id_client: int) -> Form | None:
        with self.redis as redis:
            client_data = redis.get(str(id_client))
            return client_data

    def set_client_data(self, client_data: Form):
        with self.redis as redis:
            redis.set(str(client_data.id_client), client_data.json())

