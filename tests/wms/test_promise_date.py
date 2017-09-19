from locust import HttpLocust, TaskSet, task
import requests
import json


class PromiseDateLoadTest(TaskSet):
    @task
    def get_status(self):
        self.client.get('/status')

    @task(2)
    def get_error(self):
        self.client.get('/error')

    @task(3)
    def get_order_1(self):
        self.client.get('/order/1232341')

    @task(4)
    def post_products(self):
        self.client.post("/products/", json={
            'product_id': 12123,
            'qty': 1,
            'is_personalised': True,
            'mrd_zone': "Main Mrd",
            'sales_region': "cpt",
            'payment_method': "Credit Card",
            'delivery_method': "Standard",
            'is_risky': False,
            'is_po_box': False
        })


class WebsiteUser(HttpLocust):
    task_set = PromiseDateLoadTest
    min_wait = 1000
    max_wait = 5000
