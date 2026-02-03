import argparse
import json
import os
import sys
import time
from typing import Any

# Add project root to Python path to ensure src module is found
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
from src.scraper import InstagramScraper

load_dotenv()


def _now_ts() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def save_json(data: Any, name: str) -> str:
    os.makedirs("output", exist_ok=True)
    path = f"output/{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved to {path}")
    return path


def save_error(data: Any, name: str) -> str:
    os.makedirs("output", exist_ok=True)
    path = f"output/error_{name}_{_now_ts()}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved error to {path}")
    return path


def save_result(data: Any, name: str) -> None:
    if isinstance(data, dict) and data.get("error"):
        save_error(data, name)
        raise SystemExit(data.get("error"))
    save_json(data, name)

def main():
    parser = argparse.ArgumentParser(description="Instagram scraper powered by Thordata")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Posts by profile
    posts = sub.add_parser("posts", help="Get posts from a profile URL")
    posts.add_argument("--profile", required=True, help="Profile URL, e.g. 'https://www.instagram.com/username'")
    posts.add_argument("--limit", type=int, default=10, help="Number of posts to scrape")
    posts.add_argument("--start-date", help="Start date (MM-DD-YYYY), e.g. '01-01-2025'")
    posts.add_argument("--end-date", help="End date (MM-DD-YYYY), e.g. '12-31-2025'")
    posts.add_argument("--post-type", choices=["Post", "Reel", "Both"], default="Post", help="Post type filter")

    # Single post
    post = sub.add_parser("post", help="Get post details by post URL")
    post.add_argument("url", help="Post URL, e.g. 'https://www.instagram.com/p/ABC123/'")

    # Profile
    profile = sub.add_parser("profile", help="Get profile information")
    profile.add_argument("target", help="Username (e.g. 'zoobarcelona') or profile URL")
    profile.add_argument(
        "--mode",
        choices=["username", "url"],
        default=None,
        help="Force mode. Default: auto-detect",
    )

    # Reels
    reels = sub.add_parser("reels", help="Get reels from a profile")
    reels.add_argument("url", help="Profile URL, e.g. 'https://www.instagram.com/username'")
    reels.add_argument("--limit", type=int, default=10, help="Number of reels to scrape")
    reels.add_argument("--exclude", help="Post IDs to exclude (comma-separated)")
    reels.add_argument("--start-date", help="Start date (MM-DD-YYYY)")
    reels.add_argument("--end-date", help="End date (MM-DD-YYYY)")

    # Reels list
    reels_list = sub.add_parser("reels-list", help="Get reels list from a profile URL")
    reels_list.add_argument("url", help="Profile URL, e.g. 'https://www.instagram.com/username'")
    reels_list.add_argument("--limit", type=int, default=10, help="Number of reels to scrape")
    reels_list.add_argument("--exclude", help="Post IDs to exclude (comma-separated)")
    reels_list.add_argument("--start-date", help="Start date (MM-DD-YYYY)")
    reels_list.add_argument("--end-date", help="End date (MM-DD-YYYY)")

    # Single reel
    reel = sub.add_parser("reel", help="Get reel details by reel URL")
    reel.add_argument("url", help="Reel URL, e.g. 'https://www.instagram.com/reel/ABC123/'")

    # Comments
    comments = sub.add_parser("comments", help="Get comments from a post or reel")
    comments.add_argument("url", help="Post or reel URL")

    args = parser.parse_args()
    bot = InstagramScraper()

    if args.cmd == "posts":
        data = bot.get_posts_by_profile(
            args.profile,
            limit=args.limit,
            start_date=args.start_date,
            end_date=args.end_date,
            post_type=args.post_type
        )
        save_result(data, f"posts_{args.profile.split('/')[-1]}")

    elif args.cmd == "post":
        data = bot.get_post_by_url(args.url)
        save_result(data, "post_details")

    elif args.cmd == "profile":
        target = args.target
        mode = args.mode

        if mode == "username":
            data = bot.get_profile_by_username(target)
        elif mode == "url":
            data = bot.get_profile_by_url(target)
        else:
            if target.startswith(("http://", "https://")):
                data = bot.get_profile_by_url(target)
            else:
                data = bot.get_profile_by_username(target)

        save_result(data, "profile")

    elif args.cmd == "reels":
        data = bot.get_all_reels_by_profile(
            args.url,
            limit=args.limit,
            exclude_posts=args.exclude,
            start_date=args.start_date,
            end_date=args.end_date
        )
        save_result(data, f"reels_{args.url.split('/')[-1]}")

    elif args.cmd == "reels-list":
        data = bot.get_reels_list_by_profile(
            args.url,
            limit=args.limit,
            exclude_posts=args.exclude,
            start_date=args.start_date,
            end_date=args.end_date
        )
        save_result(data, f"reels_list_{args.url.split('/')[-1]}")

    elif args.cmd == "reel":
        data = bot.get_reel_by_url(args.url)
        save_result(data, "reel_details")

    elif args.cmd == "comments":
        data = bot.get_comments_by_post(args.url)
        save_result(data, "comments")

if __name__ == "__main__":
    main()
