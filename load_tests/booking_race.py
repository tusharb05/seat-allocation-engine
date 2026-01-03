from locust import HttpUser, task, between
import uuid
import time

SHOW_ID = "show_1"
SEAT_IDS = ["A2", "A3"]

class BookingUser(HttpUser):
    wait_time = between(0.05, 0.2)

    @task
    def book(self):
        user_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())

        # Step 1: lock
        lock = self.client.post(
            "http://localhost:8001/seat-lock",
            json={
                "show_id": SHOW_ID,
                "seat_ids": SEAT_IDS,
                "user_id": user_id
            }
        )

        if lock.status_code == 200 and lock.json().get("success"):
            time.sleep(0.2)

            # Step 2: confirm
            with self.client.post(
                "/booking/confirm",
                json={
                    "show_id": SHOW_ID,
                    "seat_ids": SEAT_IDS,
                    "user_id": user_id,
                    "request_id": request_id
                },
                catch_response=True
            ) as resp:

                if resp.status_code == 200:
                    resp.success()
                elif resp.status_code in (400, 409):
                    resp.failure(f"Expected rejection: {resp.status_code}")
                else:
                    resp.failure(f"Unexpected status {resp.status_code}")
