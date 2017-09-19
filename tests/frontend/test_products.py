from locust import HttpLocust, TaskSet, task
import requests


class GetProductsAddtoCart(TaskSet):
    @task
    def get_product_bestway(self):
        self.client.get('/bestway-star-wars-single-slide-silver/PLID42314487')

    @task(2)
    def get_cart(self):
        self.client.get('/cart')


class WebsiteUser(HttpLocust):
    task_set = GetProductsAddtoCart
    min_wait = 1000
    max_wait = 2000
