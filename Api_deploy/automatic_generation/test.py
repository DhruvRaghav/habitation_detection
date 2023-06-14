import sqlite3

def create_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS image_geojson (image_name text, geojson text)''')
    conn.commit()
    conn.close()

def insert_data(db_name, image_name, geojson):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("INSERT INTO image_geojson VALUES (?,?)", (image_name, geojson))
    conn.commit()
    conn.close()

def retrieve_data(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM image_geojson")
    return c.fetchall()

# Create the database
create_db("image_geojson.db")

# Insert data
insert_data("image_geojson.db", "image1.jpg", '{"type": "Point", "coordinates": [102.0, 0.5]}')
insert_data("image_geojson.db", "image2.jpg", '{"type": "LineString", "coordinates": [[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]]}')

# Retrieve data
print(retrieve_data("image_geojson.db"))