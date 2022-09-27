from dependency_injector import containers, providers

from config import Config
from services import OdooService, PsqlService, UserService


class Container(containers.DeclarativeContainer):

    config = providers.Factory(Config)
    psql_service = providers.Singleton(PsqlService, config=config)
    odoo_service = providers.Factory(OdooService, config=config)
    user_service = providers.Factory(UserService, psql_service=psql_service, odoo_service=odoo_service)
