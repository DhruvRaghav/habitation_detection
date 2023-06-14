import os
import json
import csv
import requests

url = "https://ai.mappls.com/s0/api/vision/v2/predict"
headers = {'Authorization': 'Bearer 54c5df62-bebc-44a4-8594-3d19363461f5'}

# Folder path containing the image files
folder_path = '/path/to/folder'

# Open the CSV file
with open('/path/to/output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['filename', 'label', 'bbox'])

    # Iterate through each image file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            # Read the image file
            file_path = os.path.join(folder_path, filename)
            file_data = open(file_path, 'rb').read()

            # Send the image file to the API for prediction
            files = [('image', (filename, file_data, 'image/jpeg'))]
            response = requests.post(url, headers=headers, files=files)

            # Parse the JSON response
            data = json.loads(response.text)

            # Iterate through each region in the image
            for image_data in data['result'].values():
                for region in image_data['regions']:
                    # Extract the label and bbox values
                    label = region['region_attributes']['label']
                    bbox = [
                        region['shape_attributes']['x'],
                        region['shape_attributes']['y'],
                        region['shape_attributes']['width'],
                        region['shape_attributes']['height']
                    ]

                    # Write the row to the CSV file
                    writer.writerow([filename, label, bbox])
