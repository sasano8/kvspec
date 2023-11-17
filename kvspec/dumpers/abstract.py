class OneTimeIterator:
    def __init__(self, it):
        self.it = it
        self.opend = False

    def __iter__(self):
        if self.opend:
            raise Exception("Already opened")
        else:
            it = iter(self.it)
            self.opend = True
            return it


class DumperBase:
    content_type = "application/jsonlines"

    def __init__(self, it):
        self.it = OneTimeIterator(it)

    def dump_to(self, f):
        for data in self:
            f.write(data)

    def __iter__(self):
        raise NotImplementedError()
