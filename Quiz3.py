""" პირველი ნაწილი """
import requests
import json
import sqlite3

url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
key = "L1wREXqH3d05fQERKjeQnGKLaDQBfYYNBf2T3KII"
"""შეიძლება შეყვანილ თარიღზე ასევე შეყვანილი კამერის მოდელით ფოტო გადაღებული არ იყოს
და ინდექსის ერორი ამოაგდოს,მარა უმეტესად არ აგდებს,ბოლო წლებში შობის დღეებზე თითქმის
 სულ არის ფოტოები"""
date = input("Insert a date on which you'd like to see a mars photo: ")
camera_type = input(f"Insert camera model to see it's taken photo on mars on {date},\n "
                    "models are - FHAZ,MAST,RHAZ,CHEMCAM: ")
payload = {"api_key": key, "earth_date": date, 'camera': camera_type}
response = requests.get(url, params=payload)

print(response.reason)
print(response.status_code)
print(response.headers)
print(response.text)

""" მეორე ნაწილი"""
res = response.json()
with open("data1.json", 'w') as file:
    json.dump(res,file,indent=4)

""" მესამე ნაწილი, აქ მომხმარებლის შეყვანილი თარიღისა და კამერის მოდელის შესაბამის მონაცემებს ვეძებ,
კონკრეტულად: ამ დღეს შეყვანილი კამერით გადაღებული პირველი ფოტოს აიდი და ამ ფოტოს url გამომაქვს,
ასევე ამ თარიღის შესაბამისი მარსის დღე და კამერის სახელი"""
photo_id = res['photos'][0]['id']
mars_day = res['photos'][0]['sol']
camera_name = res['photos'][0]['camera']['name']
img_src = res['photos'][0]['img_src']

print(photo_id, 'is an id of the photo')
print(mars_day, 'is a solar day on Mars; that is, a Mars-day')
print(camera_name, 'is a camera model')
print(img_src, 'is an URL of the photo')
print(f"{len(res['photos'])} is a total number of photos taken by {camera_name} on that day'")


img_download = input(f"would you like to save image of mars on {date}: ")
if img_download == 'yes':
    responsee = requests.get(img_src)
    file1 = open('mars.jpg', 'wb')
    file1.write(responsee.content)
    print("image was saved successfully")
else:
    print("image won't be saved")


"""მეოთხე ნაწილი,აქ ვქმნი 5 სვეტიან ცხრილს,მომხმარებლის შეყვანილი თარიღისა და კამერის შესაბამისად მონაცემები
ემატება ცხრილში.სვეტებია:აიდი,ფოტოს აიდი,მარსის დღე,კამერის სახელი და ფოტოს url"""
conn = sqlite3.connect("mars_photos_db.sqlite")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS mars_photos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      photo_id INTEGER,
                      mars_day INTEGER,
                      camera_name VARCHAR(10),
                      img_src VARCHAR(200))''')

cursor.execute('INSERT INTO mars_photos (photo_id, mars_day, camera_name,img_src) VALUES (?, ?, ?,?)',
               (photo_id, mars_day, camera_name, img_src))
conn.commit()
conn.close()
