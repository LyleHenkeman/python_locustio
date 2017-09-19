#!/usr/bin/env python2

import logging
import multiprocessing
import os
import signal
import subprocess

import requests

processes = []
logging.basicConfig()
logger = logging.getLogger('bootstrap')


def bootstrap():
    """
    Initialize role of running docker container.

    master: web interface / API.
    slave: node that load test given url.
    controller: node that control the automatic run.
    """
    role = get_or_raise('ROLE')
    logger.info('Role :{role}'.format(role=role))

    if role == 'master':
        target_host = get_or_raise('TARGET_HOST')
        locust_file = get_or_raise('LOCUST_FILE')
        logger.info('target host: {target}, locust file: {file}'.format(target=target_host, file=locust_file))

        processes.append(subprocess.Popen([
            'locust', '-H', target_host, '--loglevel', 'debug', '--master', '-f', locust_file
        ]).communicate())

    elif role == 'slave':
        try:
            target_host = get_or_raise('TARGET_HOST')
            locust_file = get_or_raise('LOCUST_FILE')
            master_host = get_or_raise('MASTER_HOST')
            multiplier = int(os.getenv('SLAVE_MUL', (multiprocessing.cpu_count() * 2) + 1))
        except ValueError as verr:
            logger.error(verr)

        logger.info('target host: {target}, locust file: {file}, master: {master}, multiplier: {multiplier}'.format(
            target=target_host, file=locust_file, master=master_host, multiplier=multiplier))
        for _ in range(multiplier):
            logger.info('Started Process')
            s = subprocess.Popen([
                'locust', '-H', target_host, '--loglevel', 'debug', '--slave', '-f', locust_file,
                '--master-host', master_host
            ])
            processes.append(s)

    elif role == 'controller':
        automatic = str_to_bool(os.getenv('AUTOMATIC', str(False)))
        logger.info('Automatic run: {auto}'.format(auto=automatic))

        if automatic:
            try:
                master_host = get_or_raise('MASTER_HOST')
                master_url = 'http://{master}:8089'.format(master=master_host)
                users = int(get_or_raise('USERS'))
                hatch_rate = int(get_or_raise('HATCH_RATE'))
                duration = int(get_or_raise('DURATION'))
                logger.info(
                    'master url: {url}, users: {users}, hatch_rate: {rate}, duration: {duration}'.format(
                        url=master_url, users=users, rate=hatch_rate, duration=duration))

                for _ in range(0, 5):
                    import time
                    time.sleep(3)

                    res = requests.get(url=master_url)
                    if res.ok:
                        logger.info('Start load test automatically for {duration} seconds.'.format(duration=duration))
                        payload = {'locust_count': users, 'hatch_rate': hatch_rate}
                        res = requests.post(url=master_url + '/swarm', data=payload)

                        if res.ok:
                            time.sleep(duration)
                            requests.get(url=master_url + '/stop')
                            logger.info('Load test is stopped.')

                            logger.info('Downloading reports...')
                            report_path = os.path.join(os.getcwd(), 'reports')
                            os.makedirs(report_path)

                            res = requests.get(url=master_url + '/htmlreport')
                            with open(os.path.join(report_path, 'reports.html'), "wb") as file:
                                file.write(res.content)
                            logger.info('Reports is successfully downloaded.')
                        else:
                            logger.error('Locust cannot be started. Please check logs!')

                        break
                    else:
                        logger.error('Attempt: {attempt}. Locust master might not ready yet. '
                                     'Status code: {status}'.format(attempt=_, status=res.status_code))
            except ValueError as v_err:
                logger.error(v_err)

    else:
        raise RuntimeError('Invalid ROLE value. Valid Options: master, slave, controller.')

    for s in processes:
        s.communicate()


def str_to_bool(str):
    """
    Convert string to boolean.

    :param str: given string
    :type str: str
    :return: converted string
    :rtype: bool
    """
    return str.lower() in ('yes', 'true', 't', '1')


def get_or_raise(env):
    """
    Check if needed environment variables are given.

    :param env: key
    :type env: str
    :return: value
    :rtype: str
    """
    env_value = os.getenv(env)
    if not env_value:
        raise RuntimeError('The environment variable {0:s} should be set.'.format(env))
    return env_value


def kill(signal, frame):
    logger.info('Received KILL signal')
    for s in processes:
        s.kill(s)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.info('Started main')
    signal.signal(signal.SIGTERM, kill)
    bootstrap()
