from locust import Locust
from locust import TaskSet
from locust import task
import os

class MyTaskSet(TaskSet):
    @task(1)
    #The tasks attribute defines the different tasks a locust user will perform. If the tasks attribute is specified as a list, each time a task is to be performed, it will be randomly chosen from the tasks attribute. If however, tasks is a dict - with callables as keys and ints as values - the task that is to be executed will be chosen at random but with the int as ratio
    def index(self):
        self.clent.get("/")

class MyLocust(Locust):
    #host     =
    #The host attribute is an adress to the host that is to be loaded. Usually, this is specified on the command line, using the host option, when locust is started. If one declares a host attribute in the locust class, it will be used in the case when no host is specified on the command line.
    host = os.environ['host']
    task_set = MyTaskSet
    min_wait = 1000
    max_wait = 5000
    # Additionally to the tasks attribute, one usually want to declare the min_wait and max_wait attributes. These are the minimum and maximum time, in milliseconds, that a simulated user will wait between executing each task. min_wait and max_wait defaults to 1000, and therefore a locust will always wait 1 second between each task if min_wait and max_wait is not declared.
