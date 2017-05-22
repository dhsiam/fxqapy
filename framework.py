import framework_util as util


def write_line(self):
    pass


def read_line(self):
    pass


def create_file(self):
    pass


def create_dir(self):
    pass


def log_line(self):
    pass


class TestCase(object):

    result_header = ('test_area', 'ref', 'description', 'verification', 'expected_result', 'actual_result', 'result', 'evidence', 'timestamp', 'user', 'os', 'machine')

    def __init__(self, test_area, ref, description, verification, expected_result, actual_result, evidence):
        # create results dictionary
        self.result = dict((x, '') for x in TestCase.result_header)
        self.result['test_area'] = test_area
        self.result['ref'] = ref
        self.result['description'] = description
        self.result['verification'] = verification
        self.result['expected_result'] = expected_result
        self.result['actual_result'] = actual_result
        self.result['evidence'] = evidence
        self.result['timestamp'] = util.get_current_datetime()
        self.result['user'] = util.get_user()
        self.result['os'] = util.get_platform()
        self.result['machine'] = util.get_machine()

    def execute(self):
        # evaluate the test case
        self.evaluate_test_case()
        self.write_result()

    def write_result(self):
        # write the test case result to file
        util.write_result(self.result)

    def evaluate_test_case(self):
        result = util.dictionary_verify(self.result['expected_result'], self.results['actual_result'])
        self.result['result'] = result

