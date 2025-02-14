from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests: int = 5, time_window: int = 60):
        self.max_requests = max_requests  # Maximum requests per time window
        self.time_window = time_window  # Time window in seconds
        self.requests = defaultdict(list)  # Store timestamps of requests for each user

    def is_rate_limited(self, user_id: str) -> bool:
        """
        Check if a user is rate limited
        Returns True if rate limited, False otherwise
        """
        current_time = time.time()
        
        # Clean up old timestamps
        self.requests[user_id] = [
            timestamp for timestamp in self.requests[user_id]
            if current_time - timestamp <= self.time_window
        ]
        
        # Check if user has exceeded rate limit
        if len(self.requests[user_id]) >= self.max_requests:
            return True
            
        # Add new timestamp
        self.requests[user_id].append(current_time)
        return False
