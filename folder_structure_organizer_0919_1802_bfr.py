# 代码生成时间: 2025-09-19 18:02:09
import os
import shutil
from celery import Celery
from celery.utils.log import get_task_logger

# Initialize Celery App
app = Celery('folder_structure_organizer',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# Get the logger from Celery
logger = get_task_logger(__name__)


# Configuration for the organizer task
class FolderStructureOrganizer:
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.error_messages = []

    def _validate_folders(self):
        """
        Validates if source and destination folders exist and are directories.
        """
        if not os.path.exists(self.source_folder):
            self.error_messages.append(f'Source folder {self.source_folder} does not exist.')
            return False
        if not os.path.exists(self.destination_folder):
            self.error_messages.append(f'Destination folder {self.destination_folder} does not exist.')
            return False
        if not os.path.isdir(self.source_folder):
            self.error_messages.append(f'Source path {self.source_folder} is not a folder.')
            return False
        if not os.path.isdir(self.destination_folder):
            self.error_messages.append(f'Destination path {self.destination_folder} is not a folder.')
            return False
        return True

    def _organize_folder(self):
        """
        Organizes the files in the source folder to the destination folder.
        """
        for item in os.listdir(self.source_folder):
            src_path = os.path.join(self.source_folder, item)
            dest_path = os.path.join(self.destination_folder, item)
            try:
                if os.path.isdir(src_path):
                    # If it's a directory, move it to the destination
                    shutil.move(src_path, dest_path)
                else:
                    # If it's a file, move it to the destination
                    shutil.move(src_path, dest_path)
            except Exception as e:
                self.error_messages.append(f'Error moving {src_path} to {dest_path}: {e}')

    def organize(self):
        """
        Public method to organize the folder structure.
        """
        if not self._validate_folders():
            for error in self.error_messages:
                logger.error(error)
            return {'errors': self.error_messages}

        self._organize_folder()
        return {'errors': [], 'message': 'Folder structure organized successfully.'}


# Celery task for folder structure organizing
@app.task
def organize_folder_structure(source_folder, destination_folder):
    organizer = FolderStructureOrganizer(source_folder, destination_folder)
    return organizer.organize()


# Example usage:
# result = organize_folder_structure.delay('/path/to/source', '/path/to/destination')
# print(result.get())
