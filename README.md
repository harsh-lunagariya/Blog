# Blog Project

This is a simple Django blog application where users can join the platform, publish articles, explore posts from other users, and interact through likes, comments, and replies.

## Project Overview

The project includes a custom user system with profile support. After creating an account, a user can log in, log out, create blog posts, edit or delete their own posts, visit profile pages, and read content shared by other users.

## Main Features

- User registration with username, first name, last name, and password
- User login and logout
- Personal profile page with bio and published blogs
- Profile editing for updating the user bio
- Create, edit, and delete blog posts
- Read blogs posted by other users
- Like and unlike blog posts
- Add comments to blog posts
- Reply to comments
- Delete your own comments and replies
- Slug-based blog URLs for cleaner article links

## Pages Included

### Home Page

The home page shows a blog feed with article title, publish date, preview text, and author username. It also includes a users section where visitors can browse user cards and open profile pages. Logged-in users can quickly go to their profile, add a new blog, or log out from this page.

### Blog Detail Page

Each blog page shows the full article title, author name, date, time, and complete content. Users can like the article, read the total like count, add comments, reply to comments, and open the author profile. If the post belongs to the logged-in user, edit and delete actions are also available on the same page.

### Profile Page

The profile page displays the user's full name, username, bio, and all blogs published by that user. When the owner opens their own profile, they can create a new blog, edit their profile, and log out directly from the page.

### Authentication Pages

The project also includes separate register and login pages. New users can create an account, and existing users can sign in to access features like posting blogs, liking articles, commenting, and managing their own content.
