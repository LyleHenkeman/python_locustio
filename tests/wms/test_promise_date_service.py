import argparse
from datetime import datetime

import tal.core.util
from tal.rest_services.promise_date.client import PromiseDateServiceClient

logger = tal.core.util.get_logger(__name__)


def median(lst):
    """ Return the median of a list of values, which is:
     * the middle value if the number of items in the list is odd
     * the average of the two middle values if the number of items in a list is even
    :param lst:
    :return:
    """
    sorted_list = sorted(lst)
    len_list = len(lst)
    mid_list_index = (len_list - 1) // 2
    if len_list % 2:
        return sorted_list[mid_list_index]
    else:
        return (sorted_list[mid_list_index] + sorted_list[mid_list_index + 1]) / 2.0


class PromiseDateLoadTest(object):

    def __init__(self, cycles, endpoint):
        self.cycles = cycles
        self.endpoint = endpoint

    def run(self):
        """ Run the load test through the required cycles.
        :return:
        """
        cycle_times = []
        promise_date_client = PromiseDateServiceClient()
        for cycle in range(self.cycles):
            start_time = datetime.now()
            if self.endpoint == "status":
                promise_date_client.get_status()
            elif self.endpoint == "order":
                promise_date_client.get_promised_date_by_order(9883073)
            elif self.endpoint == "products":
                promise_date_client.get_promised_date()
            cycle_time = datetime.now() - start_time
            cycle_times.append(cycle_time.seconds * 1000000 + cycle_time.microseconds)
            logger.info("Load-test step [%d]: time [%d us]" % (cycle, cycle_time.seconds * 1000000 + cycle_time.microseconds))

        logger.info("Load-test of [%d] cycles: average time [%d us], median time [%d us]" %
                    (self.cycles, (sum(cycle_times) / len(cycle_times)), median(cycle_times)))


def _get_args(*the_args):
    parser = argparse.ArgumentParser(description="""Load-test for this service""")
    parser.add_argument("-c", "--cycles", help="Number of load-test cycles to be run for an average", default=100)
    parser.add_argument("-e", "--endpoint", help="Promise-date endpoint to use",
                        choices=["status", "order", "products"], required=True)
    return parser.parse_args(*the_args)


if __name__ == "__main__":
    args = _get_args()
    promise_date_load_test = PromiseDateLoadTest(args.cycles, args.endpoint)
    promise_date_load_test.run()
