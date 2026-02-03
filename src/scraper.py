# src/scraper.py
import json
import os
import logging
from typing import Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from thordata import ThordataClient
from thordata.exceptions import ThordataNetworkError
from .config import SPIDER_CONFIG, DEFAULT_TIMEOUT, POLL_INTERVAL

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("InstagramScraper")


class InstagramScraper:
    def __init__(self):
        self.api_key = os.getenv("THORDATA_SCRAPER_TOKEN")
        self.public_token = os.getenv("THORDATA_PUBLIC_TOKEN")
        self.public_key = os.getenv("THORDATA_PUBLIC_KEY")
        
        if not all([self.api_key, self.public_token, self.public_key]):
            raise ValueError("Missing required tokens in .env")
            
        self.client = ThordataClient(
            scraper_token=self.api_key,
            public_token=self.public_token,
            public_key=self.public_key
        )

        # Create HTTP session with retry logic
        self._http = requests.Session()
        retry = Retry(
            total=5, connect=5, read=5, backoff_factor=0.6,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"], raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._http.mount("https://", adapter)
        self._http.mount("http://", adapter)

    def _download_json(self, url: str) -> Any:
        """Download and parse JSON from result URL, supporting multiple formats"""
        resp = self._http.get(url, timeout=60)
        resp.raise_for_status()

        text = resp.text.strip()
        if not text:
            raise ValueError("Empty response from server")

        # Try standard JSON first
        try:
            return resp.json()
        except json.JSONDecodeError as e:
            # If standard JSON fails, try NDJSON (one JSON per line)
            try:
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                if not lines:
                    raise ValueError("No valid JSON lines found")
                
                # Try parsing as NDJSON
                parsed = [json.loads(line) for line in lines]
                # If we got multiple objects, return as list
                # If single object, return as dict (for backward compatibility)
                if len(parsed) == 1:
                    return parsed[0]
                return parsed
            except (json.JSONDecodeError, ValueError):
                # Last resort: try to parse multiple concatenated JSON objects
                try:
                    decoder = json.JSONDecoder()
                    idx = 0
                    out = []
                    while idx < len(text):
                        # Skip whitespace/newlines
                        while idx < len(text) and text[idx].isspace():
                            idx += 1
                        if idx >= len(text):
                            break
                        try:
                            obj, end = decoder.raw_decode(text, idx)
                            out.append(obj)
                            idx = end
                        except json.JSONDecodeError:
                            # If we can't parse from this position, break
                            break
                    
                    if out:
                        # Return single object if only one, otherwise return list
                        return out[0] if len(out) == 1 else out
                    raise ValueError(f"Could not parse JSON: {str(e)}")
                except Exception as parse_error:
                    logger.error(f"Failed to parse JSON response: {parse_error}")
                    logger.error(f"Response text (first 500 chars): {text[:500]}")
                    raise ValueError(f"JSON parsing failed: {str(e)}. Additional error: {str(parse_error)}")

    def _run(self, mode: str, params: Dict[str, Any]) -> Dict:
        cfg = SPIDER_CONFIG.get(mode)
        if not cfg:
            raise ValueError(f"Invalid mode: {mode}")

        logger.info(f"Instagram {mode}: {cfg['desc']}")
        
        try:
            result_url = self.client.run_task(
                file_name=f"ig_{mode}_{os.getpid()}",
                spider_id=cfg["id"],
                spider_name=cfg["name"],
                parameters=params,
                max_wait=DEFAULT_TIMEOUT,
                initial_poll_interval=POLL_INTERVAL
            )
            
            logger.info("Finished! Downloading...")
            return self._download_json(result_url)

        except Exception as e:
            task_id = "N/A"
            if isinstance(e, ThordataNetworkError):
                msg = str(e)
                if msg.startswith("Task "):
                    parts = msg.split()
                    if len(parts) > 1:
                        task_id = parts[1]

            error_details = {
                "error": str(e),
                "error_type": type(e).__name__,
                "task_id": task_id,
                "spider_id": cfg["id"],
                "parameters": params,
            }
            logger.error(f"Scraping task failed: {error_details}")
            return error_details

    # --- Post Methods ---
    def get_posts_by_profile(
        self,
        profile_url: str,
        limit: int = 10,
        start_date: str = None,
        end_date: str = None,
        post_type: str = "Post"
    ):
        """Get posts from a profile URL with optional filtering"""
        if not profile_url.startswith(("http://", "https://")):
            raise ValueError("Profile URL must start with http:// or https://")
        
        params = {
            "profileurl": profile_url,
            "resultsLimit": str(limit),
            "post_type": post_type
        }
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._run("posts_by_profileurl", params)

    def get_post_by_url(self, post_url: str):
        """Get post details by post URL"""
        if not post_url.startswith(("http://", "https://")):
            raise ValueError("Post URL must start with http:// or https://")
        return self._run("post_by_posturl", {"posturl": post_url})

    # --- Profile Methods ---
    def get_profile_by_username(self, username: str):
        """Get profile information by username"""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        return self._run("profile_by_username", {"username": username.strip()})

    def get_profile_by_url(self, profile_url: str):
        """Get profile information by profile URL"""
        if not profile_url.startswith(("http://", "https://")):
            raise ValueError("Profile URL must start with http:// or https://")
        return self._run("profile_by_profileurl", {"profileurl": profile_url})

    # --- Reel Methods ---
    def get_reel_by_url(self, reel_url: str):
        """Get reel details by reel URL"""
        if not reel_url.startswith(("http://", "https://")):
            raise ValueError("Reel URL must start with http:// or https://")
        return self._run("reel_by_url", {"url": reel_url})

    def get_all_reels_by_profile(
        self,
        profile_url: str,
        limit: int = 10,
        exclude_posts: str = None,
        start_date: str = None,
        end_date: str = None
    ):
        """Get all reels from a profile URL"""
        if not profile_url.startswith(("http://", "https://")):
            raise ValueError("Profile URL must start with http:// or https://")
        
        params = {
            "url": profile_url,
            "num_of_posts": str(limit)
        }
        if exclude_posts:
            params["posts_to_not_include"] = exclude_posts
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._run("all_reels_by_url", params)

    def get_reels_list_by_profile(
        self,
        profile_url: str,
        limit: int = 10,
        exclude_posts: str = None,
        start_date: str = None,
        end_date: str = None
    ):
        """Get reels list from a profile URL"""
        if not profile_url.startswith(("http://", "https://")):
            raise ValueError("Profile URL must start with http:// or https://")
        
        params = {
            "url": profile_url,
            "num_of_posts": str(limit)
        }
        if exclude_posts:
            params["posts_to_not_include"] = exclude_posts
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._run("reels_by_listurl", params)

    # --- Comment Methods ---
    def get_comments_by_post(self, post_url: str):
        """Get comments from a post or reel URL"""
        if not post_url.startswith(("http://", "https://")):
            raise ValueError("Post URL must start with http:// or https://")
        return self._run("comments_by_posturl", {"posturl": post_url})
