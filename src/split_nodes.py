from textnode import TextNode, TextType
from extract_image_and_link import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        pieces = node.text.split(delimiter)
        if len(pieces) % 2 == 0:
            raise Exception("invalid markdown syntax")
        for i, piece in enumerate(pieces):
            if i % 2 == 0:
                new_nodes.append(TextNode(piece, TextType.TEXT))
            else:
                new_nodes.append(TextNode(piece, text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue            
        images = extract_markdown_images(node.text)  #images = [("alt-text", "https://i.imgur.com/zjjcJKZ.png")]
        if not images:
            new_nodes.append(node)
            continue
        original_text = node.text
        for pic in images:
            image_alt, image_url = pic[0], pic[1]
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)
            # sections[0] = text before this image
            # sections[1] = everything AFTER this image (may contain more images)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            original_text = sections[1]  # <-- advance past the current image
        # after the loop, whatever remains in original_text is the trailing text
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue            
        links = extract_markdown_links(node.text)  #links = [("alt-text", "https://boot.dev")]
        if not links:
            new_nodes.append(node)
            continue
        original_text = node.text
        for link in links:
            link_alt, link_url = link[0], link[1]
            sections = original_text.split(f"[{link_alt}]({link_url})", 1)
            # sections[0] = text before this image
            # sections[1] = everything AFTER this image (may contain more images)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            original_text = sections[1]  # <-- advance past the current image
        # after the loop, whatever remains in original_text is the trailing text
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes