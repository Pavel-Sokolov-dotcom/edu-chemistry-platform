from locust import HttpUser, task, between


class ChemistryUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 3)

    def on_start(self):

        resp = self.client.post(
            "/api/v1/auth/login",
            data={"username": "test1@gmail.com", "password": "testpass"},
        )

        if resp.status_code == 200:
            token = resp.json()["access_token"]
            self.client.headers.update({"Authorization": f"Bearer {token}"})
        else:
            print("LOGIN FAILED", resp.status_code, resp.text)

    @task(3)  # вес этого теста выше, будет вызываться чаще
    def health(self):
        self.client.get("/health")

    @task(1)
    def get_tasks(self):
        self.client.get("/tasks")
