import random
from locust import HttpUser, task, between, SequentialTaskSet

class UserBehavior(HttpUser):
    # Tiempo de espera entre peticiones (think time) de 1 a 3 segundos
    wait_time = between(1, 3)

    @task(4)
    def test_get_users(self):
        """Tarea: Listado general paginado (Ponderación 4)"""
        page = random.randint(1, 10)
        with self.client.get(f"/api/users?page={page}", name="/api/users", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Fallo con código: {response.status_code}")

    @task(3)
    def test_get_emails(self):
        """Tarea: Listado de correos paginado (Ponderación 3)"""
        page = random.randint(1, 10)
        with self.client.get(f"/api/users/emails?page={page}", name="/api/users/emails", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Fallo con código: {response.status_code}")

    @task(2)
    def test_get_over_twenty(self):
        """Tarea: Usuarios mayores de 20 años paginados (Ponderación 2)"""
        page = random.randint(1, 10)
        with self.client.get(f"/api/users/over-twenty?page={page}", name="/api/users/over-twenty", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Fallo con código: {response.status_code}")

    @task(1)
    def test_post_bulk(self):
        """Tarea: Alta en lote con correos únicos (Ponderación 1)"""
        rand_id = random.randint(100000, 999999)
        payload = {
            "users": [
                {"name": f"Locust User A {rand_id}", "email": f"locust_a_{rand_id}@test.com", "birth_date": "1995-05-10"},
                {"name": f"Locust User B {rand_id}", "email": f"locust_b_{rand_id}@test.com", "birth_date": "2001-08-15"},
                {"name": f"Locust User C {rand_id}", "email": f"locust_c_{rand_id}@test.com", "birth_date": "1988-12-01"}
            ]
        }
        with self.client.post("/api/users/bulk", json=payload, name="/api/users/bulk", catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Fallo en bulk store: {response.status_code}")
