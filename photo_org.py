import datetime
import os
import shutil

# FOLDER LOCATIONS
unsorted_folder = '/home/smith/Documents/Code/python/photo_org/unsorted/'
sorted_folder = '/home/smith/Documents/Code/python/photo_org/sorted/'

# PHOTO EXTENSIONS
'''
PROCESSED ----------------------------------------------------------------
JPEG (.jpg, .jpeg):
    A widely used format for photos, known for its good compression and ability to handle a wide range of colors, but it can also result in some image quality loss.
PNG (.png):
    A lossless format that's good for images with sharp details and transparency, often used for web graphics.
GIF (.gif):
    A format known for its ability to support simple animations and images with a limited color palette, often used for web graphics and simple animations.
BMP (.bmp):
    A simple, uncompressed image format that's commonly used on Windows systems, but can result in large file sizes.
HEIF (.heic, .heif):
    A high-efficiency image format developed by Apple that offers better compression and quality than JPEG, often used on iPhones and iPads.
TIFF (.tiff):
    A versatile format that's often used for high-quality images and professional photography, known for its ability to preserve image quality and metadata.
SVG (.svg):
    A vector graphics format that's designed for web use, allowing for scalable images that can be displayed on different devices and resolutions.

IGNORED ------------------------------------------------------------------
WebP (.webp):
    A modern format developed by Google that offers a good balance of image quality and file size, often used for web images.
EPS (.eps):
    A vector graphics format that's used for images that need to be scalable without losing quality, often used in print and design applications.
RAW (.raw):
    A format that captures the raw data from a camera's sensor, offering the most flexibility for editing, but also resulting in large file sizes.
PDF (.pdf):
    A versatile format that can contain images and other content, often used for sharing documents and portfolios.
AVIF (.avif):
    A modern image format that uses the AV1 video codec for efficient compression, offering high quality and small file sizes.
'''
photo_extensions = ['jpg','jpeg','png','gif','bmp','heic','heif','tiff','svg']

# VERBOSE SETTINGS
progress = True
verbose = False

# Option to delete empty folders as files are relocated
cleanup = True

# Track outcome for files
moved = 0
skipped = 0

# Supporting Functions
# Continually increase file version number until it is a unique name
def upversionFilePath(proposed_file_path,i):
    file_pieces = os.path.splitext(proposed_file_path)
    new_file_path = file_pieces[0] + str("_v") + str(i) + file_pieces[1]
    if os.path.exists(new_file_path):
        new_file_path = upversionFilePath(proposed_file_path,i+1)
    return new_file_path

# Main Function
# Walk the directory structure
for root, dirs, files in os.walk(unsorted_folder):
    for file in files:
        # Determine the extension type
        extension = os.path.splitext(file)[-1][1:].lower()

        # Only process extensions in the desired list of extensions
        if extension in photo_extensions:
            file_path = str(root)+str("/")+str(file)
            if progress: print(f"Processed File: {file_path}")

            # Gather statistics on the file
            file_stat = os.stat(file_path)

            # Displaying extension
            if verbose: print(f"    - Extension: {extension}")

            # Display file attributes
            if verbose: print(f"    - File size: {file_stat.st_size} bytes")
            if verbose: print(f"    - Inode number: {file_stat.st_ino}")
            if verbose: print(f"    - Device ID: {file_stat.st_dev}")
            if verbose: print(f"    - Number of hard links: {file_stat.st_nlink}")
            if verbose: print(f"    - User ID of owner: {file_stat.st_uid}")
            if verbose: print(f"    - Group ID of owner: {file_stat.st_gid}")
            if verbose: print(f"    - File mode: {file_stat.st_mode}")

            # Convert timestamp to datetime object
            atime = datetime.datetime.fromtimestamp(file_stat.st_atime)
            mtime = datetime.datetime.fromtimestamp(file_stat.st_mtime)
            ctime = datetime.datetime.fromtimestamp(file_stat.st_ctime)

            # Display time-related file attributes
            if verbose: print(f"    - Last access time: {atime} ({file_stat.st_atime})")
            if verbose: print(f"    - Last modification time: {mtime} ({file_stat.st_mtime})")
            if verbose: print(f"    - Last change time: {ctime} ({file_stat.st_ctime})")

            # Determine desired older structure
            year_folder = str(ctime.year)
            if verbose: print(f"    - Year Folder: {year_folder}")
            month_folder = str(ctime.month)
            if verbose: print(f"    - Month Folder: {month_folder}")

            # Determine name of moved file
            proposed_directory = str(sorted_folder)+str(year_folder)+str("/")+str(month_folder)+str("/")
            proposed_file_name = str(file)
            proposed_file_path = proposed_directory + proposed_file_name

            # Create the directory if it does not exist
            if not os.path.exists(proposed_directory):
                os.makedirs(proposed_directory)

            # Ensure the proposed file name is unique (not overwriting another file)
            if os.path.exists(proposed_file_path):
                proposed_file_path = upversionFilePath(proposed_file_path,1)
            
            # Move the file
            '''
            shutil.move simply calls os.rename in most cases.
            If the destination is on a different disk than the source,
            it will instead copy and then delete the source file.
            '''
            shutil.move(file_path, proposed_file_path)

            # Increase the count for files moved
            moved += 1

            # Delete empty files if configured to do this
            if cleanup:
                # Refresh folder contents
                for r, d, f in os.walk(root):
                    # No subfolders or files
                    if (not d) and (not f):
                        # Delete folder
                        os.rmdir(root)
        
        # For extensions not in the desired list of extensions to process
        else:
            file_path = str(root)+str("/")+str(file)
            if progress: print(f"Ignored File: {file_path}")
            if verbose: print(f"    - Extension: {extension}")

            # Increase the count for files skipped
            skipped += 1

# Report outcome
if progress: print(f"\nNumber of files moved:   {moved}")
if progress: print(f"Number of files skipped: {skipped}")
