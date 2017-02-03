#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os
import unittest
from glob import glob

from flowgen import language
from pypeg2 import parse, some


class PEGMixin(unittest.TestCase):

    def assertPEG(self, obj, cls, value=None):
        self.assertIsInstance(obj, cls)
        self.assertEqual(obj, value)

    def assertConditionEqual(self, obj, name, condition):
        self.assertIsInstance(obj, language.Condition)
        self.assertEqual(obj.name, name)
        self.assertEqual(obj.condition, condition)


class InstructionTestCase(PEGMixin, unittest.TestCase):

    def _test_instructions(self, case, result):
        tree = parse(case, language.Instruction)
        self.assertPEG(tree, language.Instruction, result)

    def test_instructions_parse(self):
        self._test_instructions('Welcome to code2flow;', 'Welcome to code2flow')
        self._test_instructions('Some text!;', 'Some text!')


class ConditionTestCase(PEGMixin, unittest.TestCase):

    def test_basic_while(self):
        tree = parse("""while (my_condition) {
                        instruction;
                     }""", language.Condition)
        self.assertConditionEqual(tree, 'while', "my_condition")

        self.assertPEG(tree[0], language.Instruction, "instruction")

    def test_basic_if(self):
        tree = parse("""if (example && aa) {
                        instruction;
                     }""", language.Condition)

        self.assertConditionEqual(tree, 'if', "example && aa")

        self.assertPEG(tree[0], language.Instruction, "instruction")

    def test_single_line_condition(self):
        tree = parse("if (cond) instruction;", language.Condition)

        self.assertConditionEqual(tree, 'if', "cond")

        self.assertPEG(tree[0], language.Instruction, "instruction")

    def test_condition_with_multiline_comment(self):
        tree = parse("""if (my_condition) {
                                    code;
                        /* XXX */
                     }""", language.Condition)

        self.assertConditionEqual(tree, 'if', "my_condition")

        self.assertPEG(tree[0], language.Instruction, "code")
        self.assertPEG(tree[1], language.Comment, "/* XXX */")

    def test_condition_with_multiline_comment_in_multi_lines(self):
        tree = parse("""if (my_condition) {
                                    code;
                        /* XXX
                        xxx
                        */
                     }""", language.Condition)

        self.assertConditionEqual(tree, 'if', "my_condition")

        self.assertPEG(tree[0], language.Instruction, "code")
        self.assertPEG(tree[1], language.Comment, """/* XXX
                        xxx
                        */""")

    def test_nested_condition(self):
        tree = parse("""if(my_condition) {
                        while(nested) {
                            code;
                        }
                    }""", language.Condition)

        self.assertConditionEqual(tree, 'if', "my_condition")

        self.assertConditionEqual(tree[0], 'while', "nested")

        self.assertEqual(tree[0][0], "code")


class CommentUnitTestCase(PEGMixin, unittest.TestCase):

    def test_plain_multiline_comment(self):
        tree = parse("""/* foo
                    bar */
                    """, language.Comment)

        self.assertPEG(tree, language.Comment, """/* foo
                    bar */""")

    def test_plain_end_line_comment(self):
        tree = parse("""// foo""", language.Comment)
        self.assertPEG(tree, language.Comment, "foo")


class CodeUnitTestCase(PEGMixin, unittest.TestCase):
    heading = """Welcome to code2flow;
    """
    condition = """if(In doubt?) {
      Press Help;
      while(!Ready?)
        Read help;
    }
    """
    comment = """//the preview updates
                //as you write"""
    footer = "Improve your workflow!;"""

    def test_heading(self):
        parse(self.heading, some(language.Instruction))
        parse(self.heading, language.Code)

    def test_condition(self):
        parse(self.condition, some(language.Condition))
        parse(self.condition, language.Code)

    def test_comment(self):
        parse(self.comment, some(language.Comment))
        parse(self.comment, language.Code)

    def test_footer(self):
        parse(self.footer, some(language.Instruction))
        parse(self.footer, language.Code)

    def test_concat(self):
        parse(self.heading + self.condition + self.comment + self.footer, language.Code)

    def test_ignore_condition_in_comment(self):
        tree = parse("""// foo if(cond) instruction;
            // bar""", language.Code)
        self.assertPEG(tree[0], language.Comment, "foo if(cond) instruction;")
        self.assertPEG(tree[1], language.Comment, "bar")

    def test_condition_with_end_line_comment(self):
        tree = parse("""if (my_condition) {
                                    code;
                     };// simple comment""", language.Code)

        self.assertConditionEqual(tree[0], 'if', "my_condition")

        self.assertPEG(tree[0][0], language.Instruction, 'code')

        self.assertPEG(tree[1], language.Comment, 'simple comment')

    def test_condition_with_multiple_end_line_comments(self):
        tree = parse("""if (my_condition) {
                                    code;
                     }; // simple comment
                      // second comment
                     """, language.Code)

        self.assertConditionEqual(tree[0], 'if', 'my_condition')

        self.assertPEG(tree[1], language.Comment, 'simple comment')

        self.assertPEG(tree[2], language.Comment, 'second comment')

    def test_empty_string(self):
        parse("", language.Code)

    def _get_root_dir(self):
        return os.path.join(os.path.dirname(__file__), '..')

    def test_parse_examples(self):
        path = os.path.join(self._get_root_dir(), 'examples', '*.txt')
        files = glob(path)
        for file in files:
            with open(file, 'r') as fp:
                parse(fp.read(), language.Code)
