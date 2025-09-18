# 代码生成时间: 2025-09-19 06:57:48
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Data Generator using Python and Celery
"""

import os
from celery import Celery

# Define the Celery application
app = Celery('test_data_generator',
             broker='pyamqp://guest@localhost//')

# Define a function that generates test data
@app.task
def generate_test_data(data_size):
    """
    Generate test data of a specified size.

    :param data_size: The size of the test data to be generated.
    :type data_size: int
    :return: A list of test data items.
    :rtype: list
    "