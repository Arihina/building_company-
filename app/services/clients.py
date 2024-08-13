from sqlalchemy import select

from .. import db
from ..models import Client
from ..schemas import ClientDto


class ClientService:

    @staticmethod
    def get_client_by_id(id: int) -> Client:
        return Client.query.get(id)

    @staticmethod
    def get_client_by_name(name: str) -> Client:
        return Client.query().select().where(Client.full_name == name)

    @staticmethod
    def set_client(client_dto: ClientDto):
        client = Client(
            full_name=client_dto['full_name'],
            phone_number=client_dto['phone_number'],
            organization_name=client_dto['organization_name']
        )

        db.session.add(client)
        db.session.commit()

    @staticmethod
    def update_client(id: int, client_dto: ClientDto) -> bool:
        client = Client.query.get(id)

        if not client:
            return False

        if 'full_name' in client_dto:
            client.full_name = client_dto['full_name']
        if 'phone_number' in client_dto:
            client.phone_number = client_dto['phone_number']
        if 'organization_name' in client_dto:
            client.organization_name = client_dto['organization_name']

        db.session.commit()

        return True

    @staticmethod
    def get_clients() -> list[dict]:
        query = (
            select(Client)
        )
        clients = db.session.execute(query).scalars().all()
        clients_dto = [
            ClientDto.from_orm(client).dict() for client in clients
        ]

        return clients_dto

    @staticmethod
    def delete_client(id: int) -> bool:
        client = Client.query.get(id)
        if not client:
            return False
        else:
            db.session.delete(client)
            db.session.commit()
            return True

    @staticmethod
    def get_join_clients(manager_id: int):
        pass
