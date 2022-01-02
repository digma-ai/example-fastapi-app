import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test(self):
        self.client.get("/")

    @task
    def test(self):
        self.client.request_name="/validate?user_ids=[ids]"
        ids = []
        for i in range(10):
            ids.append(i)
            self.client.get(f"/validate?user_ids={ids}")
        self.client.request_name=None

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})