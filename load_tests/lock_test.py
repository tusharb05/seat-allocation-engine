from locust import HttpUser, task, between
import uuid

SHOW_ID = "show_1"
SEAT_IDS = ["A1", "A2", "A3"]

class LockUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def try_lock(self):
        self.client.post(
            "/seat-lock",
            json={
                "show_id": SHOW_ID,
                "seat_ids": SEAT_IDS,
                "user_id": str(uuid.uuid4())
            }
        )
