# Launch as shell script in tests directory like `locust -H http://127.0.0.1:8000`
# Documentation https://docs.locust.io/en/stable/quickstart.html

from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/hello/User")
