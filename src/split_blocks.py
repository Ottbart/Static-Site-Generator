from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown) -> list[str]:
    #splits markdown text into blocks based on double newlines, and returns a list of blocks. Each block is stripped of leading and trailing whitespace, and empty blocks are removed.
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]  # strip each block
    blocks = [block for block in blocks if block]  # remove empty strings
    return blocks

def block_to_block_type(block: str) -> BlockType:
    #takes a block of markdown text and returns the corresponding BlockType based on the following rules:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH