import requests
from requests.auth import HTTPBasicAuth

# Your Mux API credentials
API_KEY = "bc9b8f31-29a5-4b84-86bf-931504c48fbf"
  # Replace with your Mux access token
MUX_SECRET_KEY="JGLkf1qi5SYhmD5PFUanGgt0kuSDIUQts3LkvrvXioPfMF3FnQLwHCuICu+ykRFyv3aY8JWanxw"
auth= HTTPBasicAuth(API_KEY,MUX_SECRET_KEY)
# Step 1: Create an upload URL
def create_upload_url():
    url = "https://api.mux.com/video/v1/uploads"
    headers = {
        # "Authorization": f"Basic {API_KEY}",
    }
    auth= HTTPBasicAuth(API_KEY,MUX_SECRET_KEY)
    data = {
        "new_asset": True,
        "playback_policy": [
                "public"
            ],
    }
    response = requests.post(url, headers=headers, data=data,auth=auth)
    
    if response.status_code == 201:
        upload_url = response.json().get("data", {}).get("url")
        upload_id = response.json().get("data",{}).get("id")
        print("Upload URL created successfully!")
        return upload_url,upload_id
    else:
        print(f"Error creating upload URL: {response.text}")
        return None

# Step 2: Upload the video file to Mux
def upload_video(upload_url, video_file):
    # with open(video_path, "rb") as video_file:
    auth= HTTPBasicAuth(API_KEY,MUX_SECRET_KEY)
    response = requests.put(upload_url, data=video_file,auth=auth)
        
    if response.status_code == 200 | 201:
        # print(response.headers,"hello")
        print("Video uploaded successfully!",response.json())
        # return response
    else:
        print(f"Error uploading video: {response.text}")
        return None


def get_asset_id(upload_id):
    url = f"https://api.mux.com/video/v1/uploads/{upload_id}"
    auth= HTTPBasicAuth(API_KEY,MUX_SECRET_KEY)
    headers = {
        # "Authorization": get_auth_header(),
    }
    response = requests.get(url, headers=headers,auth=auth)

    if response.status_code == 200:
        data = response.json().get("data", {})
        asset_id = data.get("asset_id")
        print(f"Asset ID: {asset_id}")
        return asset_id
    else:
        print(f"Error fetching upload details: {response.status_code}, {response.text}")
        return None


# Step 3: Get the asset information (including playback ID)
def get_playback_id(asset_id):
    auth= HTTPBasicAuth(API_KEY,MUX_SECRET_KEY)
    url = f"https://api.mux.com/video/v1/assets/{asset_id}"
    headers = {
        # "Authorization": f"Basic {API_KEY}",
    }
    response = requests.get(url, headers=headers,auth=auth)
    print(response.json(),"12345")
    if response.status_code == 200:
        playback_id = response.json().get("data", {}).get("playback_ids", [])[0].get("id")
        if playback_id:
            print(f"Playback ID: {playback_id}")
            return playback_id
        else:
            print("No playback ID found.")
            return None
    else:
        print(f"Error getting playback ID: {response.text}")
        return None

# # Main function to execute the steps
# def main(video_path):
#     upload_url = create_upload_url()
    
#     if upload_url:
#         # Upload the video
#         upload_response = upload_video(upload_url, video_path)
        
#         if upload_response:
#             asset_id = upload_response.get("data", {}).get("id")
#             if asset_id:
#                 # Get the playback ID
#                 get_playback_id(asset_id)


