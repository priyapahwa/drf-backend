# drf-backend
Sample assignment

The system needs a basic API to handle posts and see notifications when the post is viewed, edited, created or deleted.

*Create an API using (Django, Flask).*
**There will be two segments of users:**

1: Superuser (admin)

- Create users and invite them to write the posts 
- Get all posts (draft, published, archived) 
- Get all posts for a specific user (blog state management should be maintained) 
- Archive the post (Once archived, it should be not seen either in published or draft) 
- See list of notifications coming from users doing action on posts.

2: Normal User

- Get posts (draft, published, archived) 
- Get a post by id 
- Create a post
- Update a post 
- Delete a post

On each post action, a notification should be sent to the admin that action has been taken by the fellow user. You might need to create a log notification to emit the events to the admin.

Post Model should contain only title and description along with state variables.

A basic authentication will work for user management that is username or password. It will be great if we use JWT Token.
