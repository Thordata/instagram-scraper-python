# src/config.py

# Spider ID Configuration (Verified from Thordata Documentation)
SPIDER_CONFIG = {
    # Posts
    "posts_by_profileurl": {
        "id": "ins_posts_by-profileurl",
        "name": "instagram.com",
        "desc": "Instagram posts by profile URL with date range and post type filtering",
        "input_keys": ["profileurl", "resultsLimit", "start_date", "end_date", "post_type"],
    },
    "post_by_posturl": {
        "id": "ins_posts_by-posturl",
        "name": "instagram.com",
        "desc": "Instagram post details by post URL",
        "input_keys": ["posturl"],
    },

    # Profiles
    "profile_by_username": {
        "id": "ins_profiles_by-username",
        "name": "instagram.com",
        "desc": "Instagram profile information by username",
        "input_keys": ["username"],
    },
    "profile_by_profileurl": {
        "id": "ins_profiles_by-profileurl",
        "name": "instagram.com",
        "desc": "Instagram profile information by profile URL",
        "input_keys": ["profileurl"],
    },

    # Reels
    "reel_by_url": {
        "id": "ins_reel_by-url",
        "name": "instagram.com",
        "desc": "Instagram reel details by reel URL",
        "input_keys": ["url"],
    },
    "all_reels_by_url": {
        "id": "ins_allreel_by-url",
        "name": "instagram.com",
        "desc": "All reels from a profile URL with filtering options",
        "input_keys": ["url", "num_of_posts", "posts_to_not_include", "start_date", "end_date"],
    },
    "reels_by_listurl": {
        "id": "ins_reel_by-listurl",
        "name": "instagram.com",
        "desc": "Reels list from a profile URL",
        "input_keys": ["url", "num_of_posts", "posts_to_not_include", "start_date", "end_date"],
    },

    # Comments
    "comments_by_posturl": {
        "id": "ins_comment_by-posturl",
        "name": "instagram.com",
        "desc": "Instagram post/reel comments by post URL",
        "input_keys": ["posturl"],
    },
}

DEFAULT_TIMEOUT = 600
POLL_INTERVAL = 3
