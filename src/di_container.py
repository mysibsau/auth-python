from dependency_injector import containers, providers

from config import Config
from services.psql_service import PsqlService
from services.user_service import UserService


class Container(containers.DeclarativeContainer):

    config = providers.Factory(Config)
    psql_service = providers.Singleton(PsqlService, config=config)
    user_service = providers.Factory(UserService, psql_service=psql_service)
