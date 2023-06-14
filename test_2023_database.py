import json
import psycopg2
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

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_username",
    password="your_password"
)
cur = conn.cursor()

# Create the table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS urm_output (
        id SERIAL PRIMARY KEY,
        filename TEXT,
        label TEXT,
        bbox INT[]
    )
""")

# Iterate through each image in the result dictionary and insert into the table
for filename, image_data in data['result'].items():
    for region in image_data['regions']:
        # Extract the label and bbox values
        label = region['region_attributes']['label']
        bbox = [
            region['shape_attributes']['x'],
            region['shape_attributes']['y'],
            region['shape_attributes']['width'],
            region['shape_attributes']['height']
        ]

        # Insert the row into the table
        cur.execute("INSERT INTO urm_output (filename, label, bbox) VALUES (%s, %s, %s)",
                    (filename, label, bbox))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
