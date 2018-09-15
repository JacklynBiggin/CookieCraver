# CookieClicker

API Endpoints:
* POST `/user`
    * Create new saved user with `uid` 
    *   ``` 
            {
                "uid": 1234
            } 
        ```
* PUT `/user/update`
    * Add `new` to user's current score
    *   ``` 
            {
                "uid": 1234,
                "new": 5
            } 
        ``` 
* GET `/user/cookies?uid=<uid>`
    *   Returns user's score
* GET `/leaderboard`
    * Returns DB rows for top 100 users
