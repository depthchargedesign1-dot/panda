"""Schedule the 10 posts in posts.json on Facebook, Instagram and TikTok through the Postiz CLI.

Needs POSTIZ_API_KEY in the environment (environment settings, not chat). Run:
  python3 schedule_postiz.py            # dry run: shows integrations, settings rules and what would be posted
  python3 schedule_postiz.py --go       # uploads media and schedules every post
Every media file goes through `postiz upload` first (Postiz rule). TikTok uses DIRECT_POST.
Check `postiz integrations:settings <id>` output (printed in the dry run) before --go.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WANT = ("facebook", "instagram", "instagram-standalone", "tiktok")


def run(*args):
    out = subprocess.run(["postiz", *args], capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"postiz {' '.join(args)} failed: {out.stderr or out.stdout}")
    return out.stdout


def upload(rel):
    return json.loads(run("upload", os.path.join(HERE, rel)))["path"]


def main(go):
    integ = [i for i in json.loads(run("integrations:list")) if i.get("identifier") in WANT and not i.get("disabled")]
    for i in integ:
        print(i["identifier"], i["id"], i.get("name"))
        if not go:
            print(json.dumps(json.loads(run("integrations:settings", i["id"])).get("output", {}).get("rules"), indent=1))
    posts = json.load(open(os.path.join(HERE, "posts.json")))
    for p in posts:
        text = p["caption"].replace("{link}", p["link"])
        for i in integ:
            ident = i["identifier"]
            media = [p["video_tiktok"]] if ident == "tiktok" and p.get("video_tiktok") else p["images"]
            caption = text.replace(p["link"], "link in bio") if ident.startswith("instagram") or ident == "tiktok" else text
            settings = {}
            if ident.startswith("instagram"):
                settings = {"post_type": "post"}
            if ident == "tiktok":
                settings = {"privacy_level": "PUBLIC_TO_EVERYONE", "duet": False, "stitch": False, "comment": True,
                            "content_posting_method": "DIRECT_POST", "autoAddMusic": "no", "brand_content_toggle": False,
                            "brand_organic_toggle": True}
            print(f"#{p['n']} {p['at']} {ident}: {len(media)} media")
            if go:
                urls = ",".join(upload(m) for m in media)
                args = ["posts:create", "-c", caption, "-m", urls, "-s", p["at"], "-i", i["id"]]
                if settings:
                    args += ["--settings", json.dumps(settings)]
                print(run(*args).strip())


if __name__ == "__main__":
    main("--go" in sys.argv)
