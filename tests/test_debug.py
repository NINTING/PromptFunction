import unittest

from promptfunction import prompt_func
from promptfunction.parse import NumberParse
from promptfunction.util import debug_template


class MyTestCase(unittest.TestCase):
    def test_debug_template_void(self):
        @prompt_func()
        def base_usage(name):
            """
            Hello {{name}}
            """

        print(debug_template(base_usage))

    def test_debug_template_int(self):
        @prompt_func()
        def base_usage(a, b) -> int:
            """
            {{a}} + {{b}} = ?
            """

        self.assertListEqual(base_usage.template.input_variables, ['a', 'b'])
        self.assertEqual(type( base_usage.context.output_parse ), NumberParse)

if __name__ == '__main__':
    unittest.main()
