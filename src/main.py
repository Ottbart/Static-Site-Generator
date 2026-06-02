import shutil
import os
import sys



def move_files(src, dst):
    if os.path.exists(dst):
        print(f"Destination {dst} already exists. Removing it.")
        shutil.rmtree(dst)
    if not os.path.exists(dst):
        print(f"Creating destination directory {dst}.")
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            print(f"Moving directory {s} to {d}.")
            move_files(s, d)
        else:
            print(f"Copying file {s} to {d}.")
            shutil.copy2(s, d)

def generate_page(from_path, template_path, dest_path, basepath="/"):
    # This function should read the markdown file from from_path, convert it to HTML, read the template from template_path, insert the HTML into the template, and write the final HTML to dest_path.
    from htmlnode import markdown_to_html_node, extract_title
    
    print(f"Generating page from {from_path} using template {template_path} and writing to {dest_path}")
    
    with open(from_path) as f:
        markdown = f.read()
    
    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)

    with open(template_path) as f:
        template = f.read()

        final_html = (
            template
            .replace("{{ Title }}", title)
            .replace("{{ Content }}", html_node.to_html())
            .replace('href="/', f'href="{basepath}')
            .replace('src="/', f'src="{basepath}')
        )

        #if dest_path does not exist, create it.
        #if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # If dest_path is a directory, write the page as index.html inside it.
        #if dest_path.endswith(os.sep) or os.path.isdir(dest_path) or not os.path.splitext(dest_path)[1]:
        #dest_path = os.path.join(dest_path, "index.html")


        with open(dest_path, "w") as f:
            f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    # This function should recursively crawl every entry in the content directory and create a html document for every md found.
    for item in os.listdir(dir_path_content):
        print(f"Processing {item} in {dir_path_content}")
        if os.path.isdir(os.path.join(dir_path_content, item)):
            generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item))
        elif item.endswith(".md"):
            generate_page(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item[:-3] + ".html")) 

def main():
    basepath = sys.argv[0]
    move_files("static", "docs")

    generate_pages_recursive("content/", "template.html", "docs/", basepath=basepath)

main()