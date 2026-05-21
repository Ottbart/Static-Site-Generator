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
        return f"<{self.tag}>{children_string}</{self.tag}>"