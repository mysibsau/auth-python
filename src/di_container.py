from dependency_injector import containers, providers

from services.psql_service import PsqlService
from services.user_service import UserService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    psql_service = providers.Singleton(PsqlService, connection_str=config.db_connection_string)
    user_service = providers.Factory(UserService, psql_service=psql_service)
