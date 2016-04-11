import random
import unittest
from types import GeneratorType

from seismograph import Suite
from seismograph.collector import *
from seismograph.config import Config


class TestCollector(unittest.TestCase):

    def setUp(self):
        self.TEST_COMMAND = "one:two.test"
        self.WRONG_COMMAND = "onetwothree"
        self.config = Config()
        self.config.TESTS = []
        for index in range(3):
            self.config.TESTS.append("one:two" + str(index) + ".test" + str(index))
        self.config.RANDOM = True
        self.config.RANDOM_SEED = 2
        self.config.__class__name = "test_class"

    #@unittest.skip("demonstrating skipping")
    def test_get_shuffle(self):
        test_object = random.Random(self.config.RANDOM_SEED)

        self.assertEqual(id(test_object.shuffle), id(get_shuffle(self.config)))

    #@unittest.skip("demonstrating skipping")
    def test_get_suite_name_from_command(self):
        self.assertEqual("one", get_suite_name_from_command(self.TEST_COMMAND))

    #@unittest.skip("demonstrating skipping")
    def test_get_suite_name_from_command_error(self):
        self.assertEqual(self.WRONG_COMMAND, get_suite_name_from_command(self.WRONG_COMMAND))

   # @unittest.skip("demonstrating skipping")
    def test_get_case_name_from_command(self):
        self.assertEqual("two", get_case_name_from_command(self.TEST_COMMAND))

    #@unittest.skip("demonstrating skipping")
    def test_get_case_name_from_command_error(self):
        self.assertEqual(None, get_case_name_from_command(self.WRONG_COMMAND))

    #@unittest.skip("demonstrating skipping")
    def test_get_test_name_from_command(self):
        self.assertEqual("test", get_test_name_from_command(self.TEST_COMMAND))

    #@unittest.skip("demonstrating skipping")
    def test_get_test_name_from_command_error(self):
        self.assertEqual(None, get_test_name_from_command(self.WRONG_COMMAND))

    #@unittest.skip("demonstrating skipping")
    def test_try_apply_rules(self):
        suite = Suite("test_suite")
        rules = []
        test_rules = []
        test_suite_rules = []

        for index in range(2):
            rule = BuildRule("test_suite", "test_case")
            rules.append(rule)
            test_suite_rules.append(rule)
        for index in range(3):
            rule = BuildRule("test_different_suite")
            rules.append(rule)
            test_rules.append(rule)
        try_apply_rules(suite, rules)

        self.assertItemsEqual(test_rules, rules)
        self.assertItemsEqual(test_suite_rules, suite.context.build_rules)

    #@unittest.skip("demonstrating skipping")
    def test_base_generator(self):
        suites = []
        for i in range(3):
            suite = Suite("test_suite" + str(i))
            suites.append(suite)
        test_generator = base_generator(suites, random.shuffle)

        self.assertIsInstance(test_generator, GeneratorType)
        test_generator.next()

    #@unittest.skip("demonstrating skipping")
    def test_generator_by_commands(self):
        rules = []
        for index in range(2):
            rule = BuildRule("test_suite" + str(index), "test_case")
            rules.append(rule)
        suites = []
        for index in range(2):
            suite = Suite("test_suite" + str(index))
            suites.append(suite)
        test_generator = generator_by_commands(suites, rules)

        self.assertIsInstance(test_generator, GeneratorType)

    #@unittest.skip("demonstrating skipping")
    def test_create_generator(self):
        suites = []
        for index in range(2):
            suite = Suite("test_suite" + str(index))
            suites.append(suite)
        test_generator = create_generator(suites, self.config)

        self.assertIsInstance(test_generator, GeneratorType)

if __name__ == "__main__":
    unittest.main()
