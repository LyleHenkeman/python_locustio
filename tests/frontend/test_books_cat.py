from locust import HttpLocust, TaskSet, task
import requests


class TakealotFrontendBooks(TaskSet):
    @task
    def get_books(self):
        self.client.get('/books')

    @task(2)
    def get_books_english(self):
        self.client.get('/books/all/?language=English')

    @task(2)
    def get_books_featured(self):
        self.client.get('/books/featured-19138')


class WebsiteUser(HttpLocust):
    task = TakealotFrontendBooks
    min_wait = 1000
    max_wait = 3000
