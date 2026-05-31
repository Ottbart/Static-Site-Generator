import unittest
from textwrap import dedent
from htmlnode import HTMLNode, LeafNode, ParentNode, markdown_to_html_node

class TestTextNode(unittest.TestCase):
    def test_goodcase(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)
    
    def test_not_eq(self):
        node1 = HTMLNode(props={"href": "https://www.google.com"})
        node2 = HTMLNode(props=None)
        self.assertNotEqual(node1.props_to_html(), node2.props_to_html())
    
    def test_None(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_missing_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_without_tag(self):
        node = LeafNode(None, "sometext")
        self.assertEqual(node.to_html(), "sometext")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_markdown_to_html_node_renders_heading_and_paragraph(self):
        md = "# Hello World\n\nThis is **bold** and _italic_."
        root = markdown_to_html_node(md)
        self.assertEqual(
            root.to_html(),
            "<div><h1>Hello World</h1><p>This is <b>bold</b> and <i>italic</i>.</p></div>",
        )

    def test_markdown_to_html_node_code_block_does_not_parse_inline(self):
        md = "```\nprint(**hello**)\n```"
        root = markdown_to_html_node(md)
        self.assertEqual(root.to_html(), "<div><pre><code>print(**hello**)\n</code></pre></div>")

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = dedent("""
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    if __name__ == "__main__":
        unittest.main()