from bs4 import BeautifulSoup
import os
import random
import string

# Function to generate random translation keys
def generate_translation_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Function to process HTML files
def process_html_file(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Add data-i18n attribute to relevant tags
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'a']):
        tag['data-i18n'] = generate_translation_key()

    # Write changes back to the file
    with open(file_path, 'w') as file:
        file.write(str(soup))

# Main function to process all HTML files in a directory
def process_html_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            process_html_file(file_path)

# Example usage
directory_path = '/Users/mathieunauleau/Documents/GitHub/mathnauleau.github.io/parse/'
process_html_files_in_directory(directory_path)


# https://beautiful-soup-4.readthedocs.io/en/latest/