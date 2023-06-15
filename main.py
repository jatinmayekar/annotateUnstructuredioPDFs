import os
import nltk
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
from fpdf import FPDF
from unstructured.partition.pdf import partition_pdf
from collections import Counter
from unstructured.staging.base import convert_to_dict
from collections import defaultdict
import shutil

# Dictionary for colors for each type
color_dict = {
    "Title": "red",
    "FigureCaption": "blue",
    "NarrativeText": "green",
    "ListItem": "yellow",
    "Table": "orange",
    "Address": "purple",
    "PageBreak": "brown"
}

# Paths
input_pdf_path = "C:/Users/jatin/OneDrive/Desktop/ai/pdf_2.pdf"

# Annotate PDF
annotate_pdf(input_pdf_path)

def parse_pdf(pdf_path):
    elements = partition_pdf(pdf_path,strategy="hi_res")
    list_elements(elements)
    return convert_to_dict(elements)

def list_elements(elements)
    print("List of elements identified:\n")
    display(Counter(type(element) for element in elements))

def copy_pdf(pdf_path):
    directory, file_name = os.path.split(pdf_path)
    base_name, ext = os.path.splitext(file_name);
    new_file_name = f"{base_name}_annotate{ext}"
    new_file_path = os.path.join(directory, new_file_name)
    shutil.copy(file_path, new_file_path)
    return new_file_path

def annotate_pdf(pdf_path):   
    data = parse_pdf(pdf_path);

    # Convert the pdf pages into images
    images = convert_from_path(pdf_path)

    # Load the font and set the size
    font_size = 30  # Change this value to increase or decrease the text size
    font = ImageFont.truetype("arial.ttf", font_size)

    # Create a dictionary mapping page numbers to list of data
    page_data_dict = defaultdict(list)
    for item in data:
        page_data_dict[item['metadata']['page_number']].append(item)

    # Iterate through pages in ascending order
    for page_number in sorted(page_data_dict.keys()):
        # Fetch the corresponding image based on page number
        img = images[page_number - 1]
        draw = ImageDraw.Draw(img)
        
        # Iterate through each data entry for this page
        for page_data in page_data_dict[page_number]:
            # Fetch the color for the type
            color = color_dict.get(page_data['type'], "blue")  # default color is blue

            # Draw the bounding box
            draw.rectangle(
                [(page_data['coordinates'][0][0], page_data['coordinates'][0][1]), (page_data['coordinates'][2][0], page_data['coordinates'][2][1])],
                outline=color, 
                width=2
            )

            # Write the type next to the bounding box with the new font size
            draw.text((page_data['coordinates'][0][0], page_data['coordinates'][0][1] - 10), page_data['type'], fill=color, font=font)
        
        # Save the image
        img.save(f"temp_img_{page_number}.png")

    # Now we convert these images back into a PDF
    pdf = FPDF()

    # Only include images for pages for which we have data
    for page_number in sorted(page_data_dict.keys()):
        img_path = f"temp_img_{page_number}.png"
        pdf.add_page()
        pdf.image(img_path, x=0, y=0, w=210, h=297)  # width and height are in millimeters
        os.remove(img_path)  # Remove the temporary image

    output_pdf_path = copy_pdf(pdf_path)
    pdf.output(output_pdf_path)

