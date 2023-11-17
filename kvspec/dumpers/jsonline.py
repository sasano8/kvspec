from json import dumps as dump_json


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


class JsonlineDumper:
    content_type = "application/jsonlines"

    def __init__(self, it):
        self.it = OneTimeIterator(it)

    def __iter__(self):
        for row in self.it:
            yield dump_json(row, ensure_ascii=False)
            yield "\n"

    def dump_to(self, f):
        for data in self:
            f.write(data)
