import os
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

project_name = "textSummarizer"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/logging/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",   
    "config/config.yaml",
    "params.yaml", 
    'app.py',
    "requirements.txt",
    "README.md",
    "setup.py",
    "main.py",
    "Dockerfile",
    "research/trials.ipynb"
]

for file in list_of_files:
    file_path = Path(file)
    # Create parent directories if they do not exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # Create the file if it does not exist
    if not file_path.exists():
        file_path.touch() # Create an empty file
    
