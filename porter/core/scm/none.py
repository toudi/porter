class SCM(object):
    def __init__(self, url, module):
        self.version = None

    def checkout(self, **kwargs):
        pass

    def set_version(self, version):
        self.version = version
