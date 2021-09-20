import unittest
from function import edit_text, count_keyword, count_switch, count_if_else

with open("c.txt") as file_object:
    read_lines = file_object.readlines()
lines = edit_text(read_lines)


class MyTestCase(unittest.TestCase):
    def test_something1(self):
        total_num = count_keyword(lines)
        self.assertEqual(total_num, 35)  # add assertion here

    def test_something2(self):
        switch_num, case_num = count_switch(lines)
        self.assertEqual(switch_num, 2)  # add assertion here
        self.assertEqual(case_num, [3, 2])

    def test_something3(self):
        if_else_num, if_elseif_else_num = count_if_else(lines)
        self.assertEqual(if_else_num, 2)  # add assertion here
        self.assertEqual(if_elseif_else_num, 2)  # add assertion here


if __name__ == '__main__':
    unittest.main()
