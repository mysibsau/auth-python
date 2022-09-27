import xmlrpc.client

from config import Config


class OdooService:
    def __init__(self, config: Config):
        self.config = config
        self.password = None
        self.uid = None

    def login(self, login, password):
        self.uid = self._get_uid(login, password)
        self.password = password

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

    def get_fio_group_and_average(self) -> tuple[str, str, float]:
        tmp = self.search_read(
            "portfolio_science.grade_view",
            [[["ID_student", "!=", ""]]],
            {"fields": ["ID_student", "display_name", "grade"]},
        )

        if not tmp:
            return "-", "-", 5.0

        average = 0
        count = 0

        for i in tmp:
            if not i["grade"][0].isdigit():
                continue
            average += int(i["grade"][0])
            count += 1

        if count:
            average = round(average / count, 2)
        else:
            average = 0

        return tmp[0]["ID_student"], tmp[0]["display_name"], average
