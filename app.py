from flask import Flask, request
from TikTokApi import TikTokApi

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
        with open(args.get("tag") + str(i) + ".mp4", "wb") as out:
            out.write(video_bytes)
        i += 1
        if i > count:
            break
    return urls


if __name__ == "__main__":
    app.run()
