import logging


class BaseCommand(object):
    def __init__(self, args):
        self.args = args
        self.logger = logging.getLogger(__name__)
