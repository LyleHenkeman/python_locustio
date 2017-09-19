Locust.io Docker Image
======================

What is Locust?
-----------

Locust is an easy-to-use, distributed, user load testing tool. It is intended for load-testing web sites (or other systems) and figuring out how many concurrent users a system can handle.


The idea is that during a test, a swarm of locusts will attack your website. The behavior of each locust (or test user if you will) is defined by you and the swarming process is monitored from a web UI in real-time. This will help you battle test and identify bottlenecks in your code before letting real users in.


Locust is completely event-based, and therefore it’s possible to support thousands of concurrent users on a single machine. In contrast to many other event-based apps it doesn’t use callbacks. Instead it uses light-weight processes, through gevent. Each locust swarming your site is actually running inside its own process (or greenlet, to be correct). This allows you to write very expressive scenarios in Python without complicating your code with callbacks.


Features
-----------

**Write user test scenarios in plain-old Python**

No need for clunky UIs or bloated XML—just code as you normally would. Based on coroutines instead of callbacks, your code looks and behaves like normal, blocking Python code.


**Distributed & Scalable - supports hundreds of thousands of users**

Locust supports running load tests distributed over multiple machines. Being event-based, even one Locust node can handle thousands of users in a single process. Part of the reason behind this is that even if you simulate that many users, not all are actively hitting your system. Often, users are idle figuring out what to do next. Requests per second != number of users online.


**Web-based UI**

Locust has a neat HTML+JS user interface that shows relevant test details in real-time. And since the UI is web-based, it’s cross-platform and easily extendable.


**Can test any system**

Even though Locust is web-oriented, it can be used to test almost any system. Just write a client for what ever you wish to test and swarm it with locusts! It’s super easy!


**Hackable**

Locust is small and very hackable and we intend to keep it that way. All heavy-lifting of evented I/O and coroutines are delegated to gevent. The brittleness of alternative testing tools was the reason we created Locust.


This docker-locust allows you to run [locust.io] in any CI tools e.g. [Jenkins] and generate HTML report at the end of load test.

Requirement
-----------
1. [docker-compose] version v1.6.0+
2. python 2.6
3. Docker must be running i.e. "dev-environments"

Run locust application locally
------------------------------

Run the application with the commands:
```
export COMPOSE_FILE=docker-compose.yml

#MacOSX
sh local.sh deploy

#Linux
./local.sh deploy

...stuff will build...

#you might be requird required to grant permissions to the file
chmod u+r,g+x local.sh
```

You will be prompted for certain inputs required

```
Target url: http://www.lyle.env
Path of load testing script: tests/wms/test_promise_date.py
Number of slave(s): 5
Run type [automatic/manual]: manual
```

**Or you can simplify it with following command:**

```bash
sh local.sh deploy http://www.lyle.env example/simple.py 5 manual
```

**Check that the locust-io container is running:**
```
 lyle@Lyle-Henkeman  ~/workspace/qa-docker-locust-io   master  docker ps                                                                                                                                                                             ✓  10434  13:40:41
CONTAINER ID        IMAGE                                                  COMMAND                  CREATED             STATUS              PORTS                                                      NAMES
0857d5909777        qadockerlocustio_slave                                 "/usr/bin/python src/"   2 minutes ago       Up 2 minutes                                                                   qadockerlocustio_slave_1
a4e197e050fb        qadockerlocustio_master                                "/usr/bin/python src/"   2 minutes ago       Up 2 minutes        0.0.0.0:5557-5558->5557-5558/tcp, 0.0.0.0:8089->8089/tcp   qadockerlocustio_master_1
```

**But how do I slavery??**
Locust can be run in a single-master, multiple-slave configuration. The slaves do all the load generation, while the master controls and monitors. Every (by default) 3 seconds, a slave sends a single report for all requests made on that slave in the last 3 seconds. The master receives these reports from all of its slaves and consolidates them in real time.

The master controls the starting and stopping of load generation on the slaves. The master cannot start/stop the locust process running on the slaves. This means you need to create servers and start locust's processes yourself.

**Running Manually:**
If somehow all of the above fails, you can run locust in isolation.

- To run Locust with the above locust file, if it was named locustfile.py and located in the current working directory, we could run:
```
locust --host=http://example.com
```
- If the locust file is located under a subdirectory and/or named different than locustfile.py, specify it using -f:
```
locust -f locust_files/my_locust_file.py --host=http://example.com
```


**Note:**
The load test script will be automatically saved in Docker image when the given command above is executed.

Report Generation
-----------------

Simply after load test run, append "/htmlreport" to the URL which will download the report of the recent run. Example:

![][Download report]

Setup in jenkins
----------------

docker-locust can be run automatically by using CI tool like jenkins.

**Sample case:**

- Target url: http://www.lyle.com
- Number of slaves: 5
- Number of users [total users that will be simulated]: 100
- Hatch rate [number of user will be added per second]: 5
- Duration [in seconds]: 20

**Steps:**

1. Put following command in "Execute shell" field:

	```bash
	(echo 100 && echo 5 && echo 30) | bash local.sh deploy http://www.lyle.com example/simple.py 5 automatic
	```

2. Install [html-publisher-plugin] in jenkins to display load test result. Example configuration in jenkins job:

 ![][HTML-Publisher configuration]

Unit tests
----------

Run the unit tests with this command:

```bash
sh local.sh test
```

Troubleshooting
---------------

All output from containers can be see by running:

```bash
docker-compose logs -f
```

[locust.io]: <http://locust.io>
[Jenkins]: <https://jenkins.io>
[docker-compose]: <https://docs.docker.com/compose/install/>
[html-publisher-plugin]: <https://wiki.jenkins-ci.org/display/JENKINS/HTML+Publisher+Plugin>
[Download report]: <images/download_report.png> "Download report"
[HTML-Publisher configuration]: <images/usage_html_publisher.png> "Example configuration of HTML Publisher in jenkins job"

**Accessing the UI:**
Once you containers are up and running you can access the UI with
```
http://<your-docker-machine-ip-address>:8089
```
![screen shot 2017-02-21 at 13 40 05](https://cloud.githubusercontent.com/assets/16188304/23163653/f3c78340-f83b-11e6-8f6f-a27144f704af.png)


![screen shot 2017-02-21 at 13 44 44](https://cloud.githubusercontent.com/assets/16188304/23163659/f9070a60-f83b-11e6-8715-8737af024033.png)
