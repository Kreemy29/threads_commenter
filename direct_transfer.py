import shutil

def copy_image(source_path, destination_path):
    """
    Directly copy an image file from source to destination.
    No encoding/decoding needed!
    """
    shutil.copy2(source_path, destination_path)

# Example usage
if __name__ == "__main__":
    source = r"C:\Users\MSI\Desktop\test.png"
    destination = r"C:\Users\MSI\Desktop\direct_copy.png"
    
    print(f"Copying image directly...")
    copy_image(source, destination)
    print(f"Done! Image copied without any encoding/decoding")
    
    # Show that the files are identical
    with open(source, 'rb') as f1, open(destination, 'rb') as f2:
        are_identical = f1.read() == f2.read()
    print(f"Files are identical: {are_identical}") 