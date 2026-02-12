import flickrapi
import urllib.request
import os
import json
import time

# --- CONFIGURATION ---
API_KEY = '{KEY}'
API_SECRET = '{SECRET}'
SAVE_FOLDER = 'downloads'

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET)

# --- AUTHENTICATION ---
if not flickr.token_valid(perms='read'):
    flickr.get_request_token(oauth_callback='oob')
    auth_url = flickr.auth_url(perms='read')
    print(f'Open this URL: {auth_url}')
    verifier = input('Enter code: ').strip()
    flickr.get_access_token(verifier)

user_info = flickr.test.login()
my_nsid = user_info.find('user').get('id')

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

print("\nStarting high-fidelity backup...")

page = 1
while True:
    # Get basic photo list
    result = flickr.photos.search(user_id=my_nsid, extras='url_o,original_format', per_page=500, page=page)
    photos_element = result.find('photos')
    photo_list = photos_element.findall('photo')
    
    if not photo_list:
        break

    for photo in photo_list:
        img_id = photo.get('id')
        img_url = photo.get('url_o')
        
        if img_url:
            ext = photo.get('original_format', 'jpg')
            img_path = os.path.join(SAVE_FOLDER, f"{img_id}.{ext}")
            json_path = os.path.join(SAVE_FOLDER, f"{img_id}.json")

            # 1. Download Image
            if not os.path.exists(img_path):
                print(f"Downloading Image {img_id}...")
                urllib.request.urlretrieve(img_url, img_path)

            # 2. Download DEEP Metadata
            if not os.path.exists(json_path):
                print(f"Fetching Deep Metadata for {img_id}...")
                # This call gets everything: dates, comments, location
                info_xml = flickr.photos.getInfo(photo_id=img_id)
                p = info_xml.find('photo')
                
                # Fetch comments separately
                comments_xml = flickr.photos.comments.getList(photo_id=img_id)
                comments = []
                for c in comments_xml.find('comments').findall('comment'):
                    comments.append({
                        "author": c.get('realname') or c.get('authorname'),
                        "date": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(c.get('datecreate')))),
                        "text": c.text
                    })

                full_meta = {
                    "id": img_id,
                    "title": p.find('title').text or "",
                    "description": p.find('description').text or "",
                    "dates": {
                        "posted_unix": p.find('dates').get('posted'),
                        "posted_human": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(p.find('dates').get('posted')))),
                        "taken": p.find('dates').get('taken'),
                        "last_update": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(p.find('dates').get('lastupdate'))))
                    },
                    "visibility": {
                        "is_public": p.find('visibility').get('ispublic'),
                        "is_friend": p.find('visibility').get('isfriend'),
                        "is_family": p.find('visibility').get('isfamily')
                    },
                    "tags": [tag.text for tag in p.find('tags').findall('tag')],
                    "comments": comments,
                    "location": {
                        "latitude": p.find('location').get('latitude') if p.find('location') is not None else None,
                        "longitude": p.find('location').get('longitude') if p.find('location') is not None else None
                    }
                }

                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(full_meta, f, indent=4)
        
    if page >= int(photos_element.get('pages')):
        break
    page += 1

print("\nBackup complete!")
