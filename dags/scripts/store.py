import json
import os


def save_news(news_data, filename):
    """Save news data to a JSON file with indentation."""
    with open(filename, 'w') as file:
        json.dump(news_data, file, indent=4)


def initialize_dvc():
    """Initialize or ensure DVC is set up in the project directory."""
    if not os.path.exists('.dvc'):
        os.system('dvc init')


def add_to_version_control(file_path):
    """Track the specified file with DVC and commit changes."""
    os.system(f'dvc add {file_path}')
    os.system('git add .')
    os.system('git commit -m "Add new data file"')
    os.system('git push')
    os.system('dvc push')
