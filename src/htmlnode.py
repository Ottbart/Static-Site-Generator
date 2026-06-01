from split_blocks import BlockType, block_to_block_type, markdown_to_blocks

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value          #A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children    #A list of HTMLNode objects representing the children of this node
        self.props = props          #A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        out = ""
        if self.props is None:
            return out
        for prop in self.props:
            value = self.props[prop]
            out += f' {prop}="{value}"'
        return out        
    
    def __repr__(self):
       return (
            f"tag: {self.tag}\n"
            f"value: {self.value}\n"
            f"children: {self.children}\n"
            f"props: {self.props}"
)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if  self.value is None:
            raise ValueError
        elif self.tag is None:
            return str(self.value)
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return (
            f"tag: {self.tag}\n"
            f"value: {self.value}\n"
            f"props: {self.props}"
        )
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag given")
        elif self.children is None:
            raise ValueError("No child given")
        children_string = ""
        for child in self.children:
            children_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"

def markdown_to_html_node(markdown):
    #
    blocks = markdown_to_blocks(markdown)
    children = [make_block_node(block) for block in blocks]
    return ParentNode("div", children)


def make_block_node(block):
    #
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return make_heading_node(block)
    elif block_type == BlockType.CODE:
        return make_code_node(block)
    elif block_type == BlockType.QUOTE:
        return make_quote_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return make_list_node(block, ordered=False)
    elif block_type == BlockType.ORDERED_LIST:
        return make_list_node(block, ordered=True)
    return make_paragraph_node(block)


def make_heading_node(block):
    # Extract the heading level and text and return a ParentNode with the appropriate tag (e.g. "h1", "h2", etc.) and children representing the text of the heading.
    level = get_heading_level(block)
    text = block[level + 1 :].strip()
    return ParentNode(f"h{level}", text_to_children(text))


def get_heading_level(block):
    count = 0
    while count < len(block) and block[count] == "#":
        count += 1
    return count


def make_code_node(block):
    # Extract the code text from the block and return a <pre><code> node with raw code text.
    from textnode import TextNode, TextType, text_node_to_html_node

    code_text = extract_code_text(block)
    code_text_node = TextNode(code_text, TextType.CODE)
    code_html_node = text_node_to_html_node(code_text_node)
    return ParentNode("pre", [code_html_node])


def extract_code_text(block):
    # Removes the opening and closing code fences and preserves raw inner code formatting.
    if not block.startswith("```"):
        return block

    start = block.find("\n")
    if start == -1:
        return ""

    content = block[start + 1 :]
    if content.endswith("```"):
        content = content[: -3]
    content = "\n".join(line.strip() for line in content.splitlines()) + "\n"
    return content


def make_quote_node(block):
    #Removes the leading > characters from each line of the block, and returns a ParentNode with the tag "blockquote" and the quote text as the children.
    quote_text = "\n".join(
        line[1:].lstrip() if line.startswith(">") else line
        for line in block.splitlines()
    )
    return ParentNode("blockquote", text_to_children(quote_text))


def make_list_node(block, ordered=False):
    #Splits the block into lines, and for each line, removes the leading - or 1. characters, and returns a ParentNode with the tag "ul" or "ol" (depending on whether ordered is False or True) and the list items as children. Each list item should be represented as a ParentNode with the tag "li" and the item text as the children.
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    item_nodes = []
    for line in lines:
        if ordered:
            _, item_text = line.split(". ", 1)
        else:
            item_text = line[2:]
        item_nodes.append(ParentNode("li", text_to_children(item_text.strip())))
    return ParentNode("ol" if ordered else "ul", item_nodes)


def make_paragraph_node(block):
    block = " ".join(line.strip() for line in block.splitlines())
    return ParentNode("p", text_to_children(block))


def text_to_children(text):
    from split_nodes import text_to_textnodes
    from textnode import text_node_to_html_node

    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def extract_title(markdown):
    #finds the heading by identifying the first line that starts with #, and returns the text of that heading as the title. If no heading is found, it raises an exception.
    for line in markdown.splitlines():
        if line.startswith("#"):
            return line[1:].strip()
    raise ValueError("No heading found")