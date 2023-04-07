# api_final
API for the social network kittygram.
It allows developers to integrate kittygram into their products.
It also provides users with the ability to conveniently and securely
log into their account and share cat photos.

## Packages:
Django 3.2.16

Djangorestframework 3.12.4

## Installation
1) Clone repostitory.
```
git clone git@github.com:ghostblade3301/api_final_yatube.git
```
2) Install virtual environment.
```
python -m venv venv
```
3) Activate virtual environment.
```
source venv/bin/activate
```
4) Install the required packages.
```
pip install -r requirements.txt
```
5) Make migrations
```
python manage.py migrate
```
or
```
./manage.py migrate
```
6) Run server
```
python manage.py runserver
```
or
```
./manage.py runserver
```
# Available endpoints
| endpoint  | method |  action |        
| --- | --- | --- |
| api/v1/posts/	  | GET, POST  | Get list of posts/create post |
| api/v1/groups/  | GET  | Get list of groups |
| api/v1/posts/{post_id}/ | GET, PUT, PATCH, DELETE | Get, replace, change/update, delete post |
| api/v1/groups/{group_id}/ | GET | Get specific group |
| api/v1/posts/{post_id}/comments/	| GET, POST | Get post's comments, create comment |
| api/v1/posts/{post_id}/comments/{comment_id}/	| GET, PUT, PATCH, DELETE | Get, replace, change/update, delete comment |
| api/v1/api-token-auth/ | POST | Get login by POST'in login and password |
