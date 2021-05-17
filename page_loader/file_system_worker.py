"""Contain functions working with file system."""

import logging
import os


def check_dir(path_to_save, to_add=False):
    """Check if destination dir exists and add it if it's not."""
    if not os.path.exists(path_to_save):
        if not to_add:
            error_msg = f'No directory {path_to_save}. Please add it'
            raise NotADirectoryError(error_msg)
        logging.info(f'Adding directory {path_to_save}')
        os.mkdir(path_to_save)
        logging.info(f'Directory {path_to_save} has been added')
    if not os.path.isdir(path_to_save):
        error_msg = f"Can't write to {path_to_save} - that's not a directory"
        raise NotADirectoryError(error_msg)


def write_file(file_path, file_content, binary=False):
    """Write content to new file."""
    logging.info(f'Writing file {file_path}')
    if binary:
        with open(file_path, 'wb') as file_to_save:
            file_to_save.write(file_content)
    else:
        with open(file_path, 'w') as file_to_save:  # noqa: WPS440
            file_to_save.write(file_content)
    logging.info(f'File {file_path} has been written')
