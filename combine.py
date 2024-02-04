import os

def append_files_to_txt(directory, file_extension, output_file):
    with open(output_file, 'a') as combined_file:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path) and file.endswith(file_extension):
                with open(file_path, 'r') as f:
                    combined_file.write(f.read())
                combined_file.write('\n')  # Separate files by a newline

if __name__ == "__main__":
    directory = os.getcwd()
    output_file = os.path.join(directory, 'combined_files.txt')

    # Append all .py files
    append_files_to_txt(directory, '.py', output_file)

    # Append all .html files in the 'templates' directory
    templates_directory = os.path.join(directory, 'templates')
    if os.path.exists(templates_directory) and os.path.isdir(templates_directory):
        append_files_to_txt(templates_directory, '.html', output_file)
    else:
        print("The 'templates' directory does not exist.")
