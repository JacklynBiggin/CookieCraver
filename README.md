# Cookie Craver
![Cookie Craver screenshot](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/000/682/804/datas/gallery.jpg)

## What is Cookie Craver?
Cookie Clicker is great, but having to actually click is soooo 2013. Cookie Craver aims to fix that - think of it as Cookie Clicker, but you earn points by collecting internet cookies, rather than having to click. It uses Chrome extension to track your cookies, and has a Python/Azure backend to store and display those all important scores.

## Folder Structure
* CookieCraver contains the Chrome extension
* marketing contains a collection of banners used for places such as Devpost and the Chrome Web Store
* web-frontend is the raw HTML files from when we were originally developing the website - these are static and purely for reference purposes
* web contains the files actually used to run the backend/website

## API Endpoints:
* POST `/user`
    * Create new saved user with `uid` 
    *   ``` 
            {
                "uid": 1234,
                "fname": "john",
                "sname": "smith",
                "pic": "some-url"
            } 
        ```
* PUT `/user/update`
    * Sets `new` to be the user's score
    *   ``` 
            {
                "uid": 1234,
                "new": 5
            } 
        ``` 
* GET `/user/cookies?uid=<uid>`
    *   Returns user information
* GET `/leaderboard`
    * Returns DB rows for top 100 users

## More Info
Cookie Craver was built as our project at the [Hack the North](https://hackthenorth.com) hackathon. For more info about the creation of it, [check it out on Devpost](https://devpost.com/software/cookie-craver).
