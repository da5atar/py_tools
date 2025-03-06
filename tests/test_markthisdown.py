import unittest
from py_tools.sys_tools.markdownthis import mkdownthis


class TestMarkdownThis(unittest.TestCase):

    def test_conversion(self):
        # Example test case for the markdown conversion function
        input_file = 'test_input.md'
        output_file = 'test_output.md'
        mkdownthis(input_file, output_file)
        with open(output_file, 'r') as f:
            content = f.read()
        self.assertIn('Expected Content', content)


if __name__ == '__main__':
    unittest.main()
