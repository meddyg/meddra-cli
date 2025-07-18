import os
from typing import List, Generator
from pathlib import Path
from exceptions import FileProcessingError

def validate_file_path(file_path: str) -> None:
    """Validates that a file path exists and is readable."""
    if not os.path.exists(file_path):
        raise FileProcessingError(file_path, FileNotFoundError(f"File not found: {file_path}"))
    
    if not os.path.isfile(file_path):
        raise FileProcessingError(file_path, ValueError(f"Path is not a file: {file_path}"))
    
    if not os.access(file_path, os.R_OK):
        raise FileProcessingError(file_path, PermissionError(f"File not readable: {file_path}"))

def validate_directory_path(directory_path: str) -> None:
    """Validates that a directory path exists and is readable."""
    if not os.path.exists(directory_path):
        raise FileProcessingError(directory_path, FileNotFoundError(f"Directory not found: {directory_path}"))
    
    if not os.path.isdir(directory_path):
        raise FileProcessingError(directory_path, ValueError(f"Path is not a directory: {directory_path}"))
    
    if not os.access(directory_path, os.R_OK):
        raise FileProcessingError(directory_path, PermissionError(f"Directory not readable: {directory_path}"))

def find_meddra_files(directory_path: str) -> List[str]:
    """Finds all .asc files in the given directory."""
    validate_directory_path(directory_path)
    
    asc_files = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.asc'):
            file_path = os.path.join(directory_path, file_name)
            asc_files.append(file_path)
    
    return sorted(asc_files)

def get_file_type_from_path(file_path: str) -> str:
    """Extracts file type from file path."""
    return Path(file_path).stem + Path(file_path).suffix.lower()

def count_file_lines(file_path: str, encoding: str = 'UTF-8') -> int:
    """Counts the number of lines in a file."""
    validate_file_path(file_path)
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return sum(1 for _ in f)
    except Exception as e:
        raise FileProcessingError(file_path, e)

def get_file_info(file_path: str) -> dict:
    """Gets basic information about a file."""
    validate_file_path(file_path)
    
    stat = os.stat(file_path)
    return {
        'path': file_path,
        'name': os.path.basename(file_path),
        'size': stat.st_size,
        'type': get_file_type_from_path(file_path),
        'line_count': count_file_lines(file_path)
    }