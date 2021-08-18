import random
import sys
import logging
import numpy as np

import torch

from dependency_injection.ioc_container import IocContainer

if __name__ == '__main__':
    # Configure container:
    container = IocContainer()

    # Run application:
    container.main()
