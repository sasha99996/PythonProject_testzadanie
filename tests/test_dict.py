import pytest
import allure

from clients.rest.dict_post import get_dict


@pytest.mark.post_dict
@allure.feature("POST /api/v1/dict")
class TestDict:

    @allure.title("Получение справочника за корректный период")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_dict_success(self, auth_headers):
        with allure.step("Отправка запроса на получение справочника"):
            response = get_dict(
                start_date="2026-01-01",
                finish_date="2026-01-31",
                limit=50,
                order_by="id",
                order_dir="ASC",
                headers=auth_headers,
            )

        with allure.step("Проверка HTTP-кода ответа"):
            assert response.status_code == 200, (
                f"Ожидался статус 200, получен {response.status_code}. "
                f"Ответ: {response.text}"
            )

        with allure.step("Проверка структуры JSON-ответа"):
            body = response.json()

            assert "header" in body
            assert "total" in body["header"]
            assert isinstance(body["header"]["total"], int)
            assert body["header"]["total"] >= 0

            assert "data" in body
            assert isinstance(body["data"], list)

        with allure.step("Проверка структуры элементов справочника"):
            for item in body["data"]:
                assert isinstance(item["id"], str)
                assert isinstance(item["name"], str)
                assert isinstance(item["ename"], str)

        with allure.step("Проверка соответствия количества записей лимиту"):
            assert len(body["data"]) <= 50


    @allure.title("Получение справочника без параметра limit")
    def test_get_dict_without_limit(self, auth_headers):
        with allure.step("Отправка POST-запроса без limit"):
            response = get_dict(
                start_date="2026-01-01",
                finish_date="2026-01-31",
                order_by="id",
                order_dir="ASC",
                headers=auth_headers,
            )

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200, (
                f"Ожидался статус 200, получен {response.status_code}"
            )

        with allure.step("Проверка количества возвращённых записей"):
            body = response.json()
            assert len(body["data"]) <= 50


    @allure.title("Получение справочника с сортировкой по убыванию")
    def test_get_dict_order_desc(self, auth_headers):
        with allure.step("Отправка запроса с orderDir=DESC"):
            response = get_dict(
                start_date="2026-01-01",
                finish_date="2026-01-31",
                limit=50,
                order_by="id",
                order_dir="DESC",
                headers=auth_headers,
            )

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200, (
                f"Ожидался статус 200, получен {response.status_code}"
            )

        with allure.step("Проверка сортировки по id"):
            body = response.json()
            ids = [item["id"] for item in body["data"]]

            assert ids == sorted(ids, reverse=True), (
                f"Записи не отсортированы по убыванию: {ids}"
            )