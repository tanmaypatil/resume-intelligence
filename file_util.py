import os
import shutil
from pathlib import Path


def list_files_with_extension(directory, extension):
    """
    List all files with a specific extension in the given directory.
    
    Args:
        directory (str): Path to the directory to search
        extension (str): File extension to filter (include the dot, e.g. '.txt')
    
    Returns:
        list: A list of filenames with the specified extension
    """
    try:
        # Get all files in the directory
        all_files = os.listdir(directory)
        print(len(all_files))
        
        # Filter files with the specified extension
        matching_files = [file for file in all_files if file.endswith(extension)]
        
        return matching_files
    
    except FileNotFoundError:
        print(f"Error: Directory {directory} not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied to access directory {directory}.")
        return []
    

def copy_folder_contents(source_dir, destination_dir):
    """
    Copy all contents from source directory to destination directory.
    
    Args:
        source_dir (str): Path to source directory
        destination_dir (str): Path to destination directory
    """
    try:
        # Convert to Path objects for better path handling
        source = Path(source_dir)
        destination = Path(destination_dir)
        
        # Check if source directory exists
        if not source.exists():
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist")
            
        # Create destination directory if it doesn't exist
        destination.mkdir(parents=True, exist_ok=True)
        
        # Copy each item in the source directory
        for item in source.glob('*'):
            if item.is_file():
                shutil.copy2(item, destination)
                print(f"Copied file: {item.name}")
            elif item.is_dir():
                shutil.copytree(item, destination / item.name, dirs_exist_ok=True)
                print(f"Copied directory: {item.name}")
                
        print(f"\nSuccessfully copied all contents from '{source_dir}' to '{destination_dir}'")
        
    except PermissionError:
        print(f"Error: Permission denied. Please check your access rights.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
def delete_files(folder_path, pattern="*", recursive=False):
    """
    Delete files from a folder with various options.
    
    Args:
        folder_path (str): Path to the folder
        pattern (str): File pattern to match (e.g., "*.txt", "*.*"), defaults to all files
        recursive (bool): Whether to delete files in subfolders too
    """
    try:
        # Convert to Path object
        folder = Path(folder_path)
        
        # Check if folder exists
        if not folder.exists():
            raise FileNotFoundError(f"Folder '{folder_path}' does not exist")
        
        # Count files before deletion
        files_to_delete = list(folder.rglob(pattern) if recursive else folder.glob(pattern))
        total_files = len(files_to_delete)
        
        # Delete files
        deleted_count = 0
        for file_path in files_to_delete:
            if file_path.is_file():  # Make sure it's a file, not a directory
                file_path.unlink()
                print(f"Deleted: {file_path}")
                deleted_count += 1
                
        print(f"\nDeleted {deleted_count} out of {total_files} files")
        return deleted_count     
    except PermissionError:
        print("Error: Permission denied. Please check your access rights.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0


