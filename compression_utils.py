#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compression Utilities for Email Attachments

This module provides functions to create various types of compressed archives
(tar, gzip, bzip2, zip) from files and directories, which can be used as
email attachments.
"""

import os
import tarfile
import zipfile
import gzip
import bz2
import shutil
from pathlib import Path


def create_tar(source_paths, output_path, compression=None):
    """
    Create a tar archive from files and/or directories.
    
    Args:
        source_paths (str or list): Path(s) to files/directories to include in the archive
        output_path (str): Path where the tar file will be saved
        compression (str, optional): Compression type - 'gz', 'bz2', or None for no compression
    
    Returns:
        str: Path to the created archive
    
    Raises:
        ValueError: If an invalid compression type is specified
    """
    if isinstance(source_paths, str):
        source_paths = [source_paths]
    
    # Determine the mode based on compression type
    if compression is None:
        mode = 'w'
    elif compression == 'gz':
        mode = 'w:gz'
    elif compression == 'bz2':
        mode = 'w:bz2'
    else:
        raise ValueError(f"Invalid compression type: {compression}. Use 'gz', 'bz2', or None.")
    
    # Create the tar archive
    with tarfile.open(output_path, mode) as tar:
        for source_path in source_paths:
            source_path = os.path.abspath(source_path)
            arcname = os.path.basename(source_path)
            
            if os.path.isdir(source_path):
                # For directories, add all files recursively
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calculate the relative path for the archive
                        rel_path = os.path.relpath(file_path, os.path.dirname(source_path))
                        tar.add(file_path, arcname=rel_path)
            else:
                # For individual files, add them directly
                tar.add(source_path, arcname=arcname)
    
    print(f"Created tar archive: {output_path}")
    return output_path


def create_zip(source_paths, output_path, compression_level=6):
    """
    Create a zip archive from files and/or directories.
    
    Args:
        source_paths (str or list): Path(s) to files/directories to include in the archive
        output_path (str): Path where the zip file will be saved
        compression_level (int, optional): Compression level (0-9, 0=no compression, 9=max)
    
    Returns:
        str: Path to the created archive
    """
    if isinstance(source_paths, str):
        source_paths = [source_paths]
    
    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED, 
                         compresslevel=compression_level) as zipf:
        for source_path in source_paths:
            source_path = os.path.abspath(source_path)
            
            if os.path.isdir(source_path):
                # For directories, add all files recursively
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Calculate the relative path for the archive
                        rel_path = os.path.relpath(file_path, os.path.dirname(source_path))
                        zipf.write(file_path, arcname=rel_path)
            else:
                # For individual files, add them directly
                arcname = os.path.basename(source_path)
                zipf.write(source_path, arcname=arcname)
    
    print(f"Created zip archive: {output_path}")
    return output_path


def compress_file_gzip(source_path, output_path=None):
    """
    Compress a single file using gzip.
    
    Args:
        source_path (str): Path to the file to compress
        output_path (str, optional): Path where the compressed file will be saved.
                                    If not provided, will use source_path + '.gz'
    
    Returns:
        str: Path to the compressed file
    """
    if not output_path:
        output_path = source_path + '.gz'
    
    with open(source_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    print(f"Created gzip file: {output_path}")
    return output_path


def compress_file_bzip2(source_path, output_path=None):
    """
    Compress a single file using bzip2.
    
    Args:
        source_path (str): Path to the file to compress
        output_path (str, optional): Path where the compressed file will be saved.
                                    If not provided, will use source_path + '.bz2'
    
    Returns:
        str: Path to the compressed file
    """
    if not output_path:
        output_path = source_path + '.bz2'
    
    with open(source_path, 'rb') as f_in:
        with bz2.open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    print(f"Created bzip2 file: {output_path}")
    return output_path


def create_archive(source_paths, output_path, archive_type='zip', compression_level=6):
    """
    Create an archive of the specified type from files and/or directories.
    
    Args:
        source_paths (str or list): Path(s) to files/directories to include in the archive
        output_path (str): Path where the archive will be saved
        archive_type (str): Type of archive to create - 'zip', 'tar', 'tar.gz', 'tar.bz2', 'gz', or 'bz2'
        compression_level (int, optional): Compression level for zip archives (0-9)
    
    Returns:
        str: Path to the created archive
    
    Raises:
        ValueError: If an invalid archive type is specified
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create the appropriate archive type
    if archive_type == 'zip':
        return create_zip(source_paths, output_path, compression_level)
    elif archive_type == 'tar':
        return create_tar(source_paths, output_path)
    elif archive_type == 'tar.gz':
        return create_tar(source_paths, output_path, compression='gz')
    elif archive_type == 'tar.bz2':
        return create_tar(source_paths, output_path, compression='bz2')
    elif archive_type == 'gz':
        if isinstance(source_paths, list) and len(source_paths) > 1:
            raise ValueError("gzip compression can only be applied to a single file")
        source_path = source_paths[0] if isinstance(source_paths, list) else source_paths
        return compress_file_gzip(source_path, output_path)
    elif archive_type == 'bz2':
        if isinstance(source_paths, list) and len(source_paths) > 1:
            raise ValueError("bzip2 compression can only be applied to a single file")
        source_path = source_paths[0] if isinstance(source_paths, list) else source_paths
        return compress_file_bzip2(source_path, output_path)
    else:
        raise ValueError(f"Invalid archive type: {archive_type}. "
                         f"Use 'zip', 'tar', 'tar.gz', 'tar.bz2', 'gz', or 'bz2'.")


if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description='Create compressed archives')
    parser.add_argument('--type', choices=['zip', 'tar', 'tar.gz', 'tar.bz2', 'gz', 'bz2'],
                        default='zip', help='Type of archive to create')
    parser.add_argument('--output', '-o', required=True, help='Output archive path')
    parser.add_argument('--compression', '-c', type=int, choices=range(10), default=6,
                        help='Compression level (0-9, for zip only)')
    parser.add_argument('sources', nargs='+', help='Files/directories to archive')
    
    args = parser.parse_args()
    
    try:
        archive_path = create_archive(args.sources, args.output, args.type, args.compression)
        print(f"Successfully created {args.type} archive: {archive_path}")
    except Exception as e:
        print(f"Error creating archive: {str(e)}")

