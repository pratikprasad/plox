import subprocess
import unittest

CASES = {
    "while": (
        """1.0
2.0
3.0
4.0
5.0
6.0
7.0
8.0
9.0
10.0
""",
        "",
    ),
    "conditions": ("lolol\n3.0\n", ""),
    "scoping": ("3.0\n", ""),
    "variable": ("3.0\n", "Variable initialized but not defined: c"),
    "blocks": (
        """inner a
outer b
global c
outer a
outer b
global c
global a
global b
global c
""",
        "",
    ),
    "test1": (
        """one
True
3.0
""",
        "",
    ),
    "hello_world": ("hello world\n", ""),
}


class TestPrograms(unittest.TestCase):
    def testPrograms(self):
        for filename, (out, err) in CASES.items():
            output = subprocess.run(
                f"python3 lox.py ./test_programs/{filename}.lox".split(" "),
                capture_output=True,
                text=True,
            )
            self.assertEqual(str(output.stdout), out)
            self.assertIn(err, str(output.stderr))
