# blog-website-project

### After Click on the blew link click the blog icon to go to the blog page
### Live demo <span>https://infinite-hollows-50552.herokuapp.com</span>

#### Features

- 1 . Add post with (ritch text editor), View Post, Update Post and Delete Post
- 2 . Authorized user can add post, update and delete post which is created by that user
- 3 . Home page display blogs (created by admin only) and on blog page display blogs created by user and admin both
- 4 . filter blogs in a page with two section (recent blogs and random blogs) 
    - section1 - latest post will show on first
    - section2 - on page refresh show random blogs
- 5 . Add blogs in different category like programming and travel and more
- 6 . Login
- 7 . Signup with email verification
- 8 . Forgot password reset with email

# Steps for Set Up

- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser (enter username, email, password)
- python manage.py runserver

# Now Django blog Ready

