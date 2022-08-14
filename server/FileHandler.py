from tornado.web import StaticFileHandler


class FileHandler(StaticFileHandler):
    def initialize(self, path):
        self.absolute_path = False
        super(FileHandler, self).initialize(path)
