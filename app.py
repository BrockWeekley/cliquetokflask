from flask import Flask, request
from TikTokApi import TikTokApi
import glob
import os

app = Flask(__name__)
tiktok = TikTokApi()


@app.route("/api/v1/videos", methods=['GET'])
def return_videos():
    args = request.args
    count = int(args.get("count", 1))
    offset = int(args.get("offset", 0))

    i = 0
    urls = []
    for video in tiktok.hashtag(name=args.get("tag")).videos(count, offset):
        video_bytes = video.bytes()
        urls.append(args.get("tag") + str(i) + ".mp4")
        with open("videos/" + args.get("tag") + str(i) + ".mp4", "wb") as out:
            out.write(video_bytes)
        i += 1
        if i > count:
            break
    return urls


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
