import unittest
from split_blocks import BlockType, block_to_block_type, markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_levels(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_not_valid_without_space(self):
        self.assertNotEqual(block_to_block_type("#Heading"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("##Heading"), BlockType.HEADING)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```python\nprint('Hello, world!')\n```"), BlockType.CODE)
    
    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE) 

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("2. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 2"), BlockType.PARAGRAPH)


    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)