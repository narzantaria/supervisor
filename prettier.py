import os
import autopep8

# Get current path
current_dir = os.getcwd()

# Get the list of all Python files
py_files = [file for file in os.listdir(current_dir) if file.endswith(".py")]

# Format each file
for file in py_files:
  file_path = os.path.join(current_dir, file)

  with open(file_path, "r") as f:
    code = f.read()

  # Format the file code
  formatted_code = autopep8.fix_code(code, options={"indent_size": 2})

  with open(file_path, "w") as f:
    f.write(formatted_code)

  print(f"File {file} successfully formatted")
