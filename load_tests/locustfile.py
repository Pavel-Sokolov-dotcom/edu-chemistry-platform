from locust import HttpUser, task, between


class ChemistryUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Получаем токен при старте "пользователя"
        resp = self.client.post(
            "/api/v1/auth/login", json={"username": "testuser", "password": "testpass"}
        )
        if resp.status_code == 200:
            self.token = resp.json()["access_token"]
            self.client.headers = {"Authorization": f"Bearer {self.token}"}

    @task
    def get_chemistry_data(self):
        self.client.get("/api/v1/chemistry/tasks/")
