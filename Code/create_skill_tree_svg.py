import yaml
import argparse
import os

def load_yaml(file_path):
    with open(file_path) as file:
        return yaml.safe_load(file)

def load_svg_template(file_path):
    with open(file_path) as file:
        return file.read()

def make_text_multiline(text: list, length1: int = 18, length2: int = 25) -> str:
    """Split long one-line strings into multiple-lines strings with a maximum length."""
    desired_l = length1
    processed_str_len = 0
    space_indexes = [i for i, char in enumerate(text) if char == " "]
    for i in range(1, len(space_indexes)):
        if space_indexes[i] < desired_l + processed_str_len:
            pass
        else:
            text[space_indexes[i - 1]] = "&#10;"
            desired_l = length2
            processed_str_len += space_indexes[i - 1] - 1
    return "".join(text)

def process_svg(template, data):
    processed = template.replace("{{ title }}", data["title"])
    processed = processed.replace("{{ footer }}", data["footer"])

    displacement = (0, 9, 19, 29, 39, 49, 59, 69)
    for i in range(10):
        for j in range(7):
            if i < 9:
                box_number = i + displacement[j]
            elif i == 9:
                box_number = i + displacement[j + 1]
                if j >= 5:
                    continue
            value = data["row"][i][j]
            splitted_string = make_text_multiline(list(value))
            placeholder = f"{{{{ box_{box_number:03d} }}}}"
            processed = processed.replace(placeholder, splitted_string)
    return processed

def save_processed_svg(content, output_path):
    with open(output_path, "w") as file:
        file.write(content)

input_yaml = "input.yml"  # Path to uploaded YAML file
output_svg = "output.svg"  # Output file
svg_template_path = "skill_tree_template.svg.j2"  # Path to uploaded SVG template

# Load files
yaml_data = load_yaml(input_yaml)
svg_template = load_svg_template(svg_template_path)

# Process and save the output
processed_svg = process_svg(svg_template, yaml_data)
save_processed_svg(processed_svg, output_svg)

# Download the output SVG file
from google.colab import files
files.download(output_svg)
