"""
نظام مجتمع GOE
"""
from typing import Dict, List
from datetime import datetime

class GOECommunity:
    def __init__(self):
        self.posts = []
        self.user_contributions = {}
    
    def create_post(self, user_id: str, title: str, content: str, tags: List[str] = None) -> Dict:
        post = {
            "id": f"post_{len(self.posts) + 1}",
            "user_id": user_id, "title": title, "content": content,
            "tags": tags or [], "created_at": datetime.utcnow().isoformat(),
            "views": 0, "likes": 0, "comments": []
        }
        self.posts.append(post)
        if user_id not in self.user_contributions:
            self.user_contributions[user_id] = {"posts": 0, "comments": 0, "likes": 0}
        self.user_contributions[user_id]["posts"] += 1
        return post
    
    def add_comment(self, post_id: str, user_id: str, comment: str) -> Dict:
        for post in self.posts:
            if post["id"] == post_id:
                comment_obj = {"user_id": user_id, "text": comment, "created_at": datetime.utcnow().isoformat(), "likes": 0}
                post["comments"].append(comment_obj)
                if user_id not in self.user_contributions:
                    self.user_contributions[user_id] = {"posts": 0, "comments": 0, "likes": 0}
                self.user_contributions[user_id]["comments"] += 1
                return {"status": "success", "comment": comment_obj}
        return {"error": "Post not found"}
    
    def like_post(self, post_id: str, user_id: str) -> Dict:
        for post in self.posts:
            if post["id"] == post_id:
                post["likes"] += 1
                return {"status": "success", "likes": post["likes"]}
        return {"error": "Post not found"}
