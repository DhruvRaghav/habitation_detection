import json
import csv
import requests

url = "https://ai.mappls.com/s0/api/vision/v2/predict"

payload={}
files=[
  ('image',('061219_111847_14970_zed_l_054.jpg',open('/home/ceinfo/Desktop/061219_111847_14970_zed_l_054.jpg','rb'),'image/jpeg'))
]
headers = {
  'Authorization': 'Bearer 54c5df62-bebc-44a4-8594-3d19363461f5'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

data = json.loads(response.text)

# Open the CSV file
with open('/home/ceinfo/Desktop/URM_OUTPUT.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['filename', 'label', 'bbox'])

    # Iterate through each image in the result dictionary
    for filename, image_data in data['result'].items():

        # Iterate through each region in the image
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
