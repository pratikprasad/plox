import subprocess
import unittest

CASES = {
    "variable": "3.0\n",
    "blocks": """inner a
outer b
global c
outer a
outer b
global c
global a
global b
global c
""",
    "test1": """one
True
3.0
""",
    "hello_world": "hello world\n",
}


class TestPrograms(unittest.TestCase):
    def testPrograms(self):
        for filename, expected in CASES.items():
            output = subprocess.run(
                f"python3 lox.py ./test_programs/{filename}.lox".split(" "),
                capture_output=True,
                text=True,
            )
            self.assertEqual(str(output.stdout), expected)