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

    videos = os.listdir("videos/")
    if len(videos) > 0:
        response["urls"] = videos
        return response

    args = request.args
    count = int(args.get("count", 1))
    offset = int(args.get("offset", 0))

    i = 0
    for video in tiktok.hashtag(name=args.get("tag")).videos(count, offset):
        video_bytes = video.bytes()
        timestamp = str(round(time.time()))
        response.get("urls").append(args.get("tag") + timestamp + ".mp4")
        with open("videos/" + args.get("tag") + timestamp + ".mp4", "wb") as out:
            out.write(video_bytes)
        i += 1
        if i > count:
            break
    return response


@app.route("/api/v1/videos", methods=['DELETE'])
def clear_videos():
    try:
        files = glob.glob('videos/*')
        for f in files:
            os.remove(f)
    except Exception as e:
        return e

    return "Success"


if __name__ == "__main__":
    app.run()
