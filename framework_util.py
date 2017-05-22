import csv, codecs, cStringIO
from sys import platform
from datetime import datetime
import getpass
import framework_config as config


def write_result(result):
    pass

def strip_commas(text):
    pass


def base_verify(expected_result, actual_result):
    if expected_result == actual_result:
        return True
    else:
        return False


def simple_verify(expected_result, actual_result):
    result = base_verify(expected_result, actual_result)
    return result


def dictionary_verify(dict_expected_result, dict_actual_result):
    result_dict = {0: True, -1: False, 1: False}
    result = cmp(dict_expected_result, dict_actual_result)
    return result_dict[result]


def get_platform():
    return platform.platform()


def get_current_datetime():
    return datetime.utcnow().isoformat()


def get_user():
    return getpass.getuser()


def get_machine():
    return platform.node()

class UTF8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)