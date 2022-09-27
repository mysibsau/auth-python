import xmlrpc.client

from config import Config


class OdooService:
    def __init__(self, config: Config, login: str, password: str):
        self.config = config
        self.password = password
        self.uid = self._get_uid(login, password)

    def _get_uid(self, login: str, password: str) -> int:
        common = xmlrpc.client.ServerProxy(self.config.odoo_url + "/xmlrpc/2/common")
        return common.authenticate(
            self.config.odoo_db,
            login,
            password,
            {},
        )

    def _do(self, method: str, model_name: str, args: list, kwargs: dict):
        models = xmlrpc.client.ServerProxy(self.config.odoo_url + "/xmlrpc/2/object")
        return models.execute_kw(
            self.config.odoo_db,
            self.uid,
            self.password,
            model_name,
            method,
            args,
            kwargs,
        )

    def read(self, model_name: str, args: list, kwargs: dict):
        return self._do("read", model_name, args, kwargs)

    def search(self, model_name: str, args: list, kwargs: dict):
        return self._do("search", model_name, args, kwargs)

    def count(self, model_name: str, args: list, kwargs: dict):
        return self._do("count", model_name, args, kwargs)

    def fields_get(self, model_name: str, args: list, kwargs: dict):
        return self._do("fields_get", model_name, args, kwargs)

    def search_read(self, model_name: str, args: list, kwargs: dict):
        return self._do("search_read", model_name, args, kwargs)
