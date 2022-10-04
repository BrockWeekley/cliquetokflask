from flask import Flask, request
from flask_cors import CORS
from TikTokApi import TikTokApi
import glob
import os
import time


app = Flask(__name__, static_folder='videos', static_url_path='/videos')
cors = CORS(app)
tiktok = TikTokApi()


@app.route("/api/v1/videos", methods=['GET'])
def return_videos():
    response = {
        "urls": []
    }
    print('Looking up existing videos...')
    videos = os.listdir("videos/")
    if len(videos) > 0:
        response["urls"] = videos
        print('Found and returning')
        return response

    args = request.args
    count = int(args.get("count", 1))
    offset = int(args.get("offset", 0))

    print('Searching tiktok for videos')
    i = 0
    for video in tiktok.hashtag(name=args.get("tag")).videos(count, offset):
        video_bytes = video.bytes()
        timestamp = str(round(time.time()))
        response.get("urls").append(args.get("tag") + timestamp + ".mp4")
        with open("videos/" + args.get("tag") + timestamp + ".mp4", "wb") as out:
            out.write(video_bytes)
        print('Wrote video')
        i += 1
        if i > count:
            break
    return response


@app.route("/api/v1/videos", methods=['DELETE'])
def clear_videos():
    try:
        print('Clearing videos...')
        files = glob.glob('videos/*')
        for f in files:
            os.remove(f)
        print('Videos cleared.')
    except Exception as e:
        print('Videos failed to clear')
        return e

    return "Success"


if __name__ == "__main__":
    app.run()