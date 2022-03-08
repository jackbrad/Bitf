# Python


from google import api_core
import time
from multiprocessing import Process, Manager, Value, Lock, Queue, Pipe
import platform, sys
import multiprocessing
import collections
import tsfresh
import numpy as np
import copy
import concurrent.futures
import json
import logging
import logging.handlers
import time
from google.cloud import pubsub


class ClientMatcher():
    def set_logging(self, process_modulo_turn, process_key):
        logging_name = "logs/processes/p_" + str(process_key) + "_" + str(process_modulo_turn)
        logger = logging.getLogger(logging_name)
        logger.setLevel(logging.INFO)
        # handler = logging.FileHandler('coco.log')
        handler = logging.handlers.TimedRotatingFileHandler(filename=logging_name + '.log', when='d')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s],%(msecs)d p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def run(self, process_key, incoming_queue, publisher_creds_file, publisher_topic, project_id):
        ### PUBSUB STUFF ###
        custom_retry = api_core.retry.Retry(initial=0.550,  # seconds (default: 0.1)
                                            maximum=190.0,  # seconds (default: 60.0)
                                            multiplier=1.9,  # default: 1.3
                                            deadline=3000.0,  # seconds (default: 60.0)
                                            predicate=api_core.retry.if_exception_type(api_core.exceptions.Aborted, api_core.exceptions.DeadlineExceeded, api_core.exceptions.InternalServerError, api_core.exceptions.ResourceExhausted,
                                                                                       api_core.exceptions.ServiceUnavailable, api_core.exceptions.Unknown, api_core.exceptions.Cancelled, ), )

        batch_settings = pubsub.types.BatchSettings(max_messages=2,  # default 100
                                                    # max_bytes=1024,  # default 1 MB
                                                    max_latency=10,  # default 10 ms
                                                    )
        publisher_options = pubsub.types.PublisherOptions(enable_message_ordering=False)
        publisher = pubsub.PublisherClient.from_service_account_file(filename=publisher_creds_file, batch_settings=batch_settings, publisher_options=publisher_options,  # client_options=client_options
                                                                     )

        topic_path = publisher.topic_path(project_id, publisher_topic)  # todo: make test topic

        counter = 0
        logger = self.set_logging(process_key, "pubsub_writer")
        print("started pubsub writer process nr " + str(process_key))

        cycle_latency_sec = 0
        while (True):
            try:
                counter = counter + 1
                print("pubsub " + str(counter))
                pub_sub_msg = incoming_queue.get()  # todo: implement shutdown message
                # TODO: 1) get the message and de serial it
                # 2) compare against current copy in hot memory
                # 3) - stack into an orderbook (if no match)
                # 4) - rearrange the orderbook (until no match)
                # 5) - --in parallel issue to topic_path pipeline - trades if there
                # 6) - loop again // repair if fails


                future = publisher.publish(topic_path, data=pub_sub_msg.encode("utf-8"), retry=custom_retry)


            except Exception as ex:
                # connection fail - save the reason in database
                # todo: publisher reinstate logic
                logger.error(str(ex))
                time.sleep(5) #antipattern
                print(str(ex))
                publisher = pubsub.PublisherClient.from_service_account_file(filename=publisher_creds_file, batch_settings=batch_settings, publisher_options=publisher_options, )  # client_options=client_options
            finally:
                # recreate the publisher
                # publisher = pubsub.PublisherClient.from_service_account_file(filename=publisher_creds_file, batch_settings=batch_settings, publisher_options=publisher_options,  # client_options=client_options

                pass




if __name__ == '__main__':
    if platform.system() == "Darwin":
        multiprocessing.set_start_method('spawn')

    lulucoco = ClientMatcher()
    lulucoco.set_logging("Matcher",0)
    lulucoco.run(sys.argv)