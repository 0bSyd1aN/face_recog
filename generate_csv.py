import os
import csv
from pathlib import Path

# Configuration
DATASET_FOLDER = 'dataset'
CSV_OUTPUT = 'dataset.csv'

def generate_dataset_csv():
    """Generate dataset.csv from images in dataset folder"""
    
    if not os.path.exists(DATASET_FOLDER):
        print(f"Error: '{DATASET_FOLDER}' folder not found!")
        return False
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    image_files = []
    
    for file in os.listdir(DATASET_FOLDER):
        if os.path.isfile(os.path.join(DATASET_FOLDER, file)):
            if Path(file).suffix.lower() in image_extensions:
                image_files.append(file)
    
    if not image_files:
        print(f"Error: No image files found in '{DATASET_FOLDER}' folder!")
        return False
    
    print(f"Found {len(image_files)} image files")
    
    # Create CSV with filename and person name (derived from filename)
    with open(CSV_OUTPUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['image_filename', 'person_name'])  # Header
        
        for image_file in sorted(image_files):
            # Extract person name from filename (remove number and extension)
            # Example: "alice_1.png" -> "alice"
            name_part = Path(image_file).stem  # Remove extension
            
            # Remove trailing numbers and underscores
            person_name = name_part.rsplit('_', 1)[0] if '_' in name_part else name_part
            person_name = person_name.strip()
            
            # Capitalize properly
            person_name = ' '.join(word.capitalize() for word in person_name.split('_'))
            
            writer.writerow([image_file, person_name])
            print(f"✓ {image_file} -> {person_name}")
    
    print(f"\n✅ Created {CSV_OUTPUT} with {len(image_files)} entries!")
    return True


if __name__ == "__main__":
    generate_dataset_csv()