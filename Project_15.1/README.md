# Project 15.1 Creating a Books Web Application
---

#### Overview:
In this project, you will expand on the concepts you learned in Module 11 to create a website that shows your collection of books. You will start by adding the cover image for each book so that they are rendered on your website beside their corresponding book titles. Next, you will add more users along with their respective usernames and passwords. Building on what you learned in Module 11, you will also set their roles to either admin or reader. This will allow the users to perform different actions on the website based on their roles. Finally, you will define a function that only allows users with the admin role to add new books to your website.

#### Data Engineering Concepts:
- Use Flask Web Server to generate a lightweight web app
  - Flask Restful Library
  - Flask JWT Extended Library
- Use Python to programitaclly load the /routes of the app and verify user logins and roles, which grant the user (depending on their role) access to certain parts of the site. 
- Utilize JSON Web Tokens (JWT) for granting access.

#### Steps:
- Open a Terminal window on your machine and install the flask-restful and flask-jwt-extended libraries using the following commands:
  ```
  pip install flask-restful
  pip install flask-jwt-extended`
  ```
- Download and unzip the Project 15.1 folder on your machine.
- In the app.py file, add two more books of your choice.
- Inside the static folder, add the cover images for the books that you just added.
- Inside the books.html file, add a line of html code to match each book cover to the book in the books list. Use the following template for this line of html code:
  ```
  <img src="static/image{*book_id_reference*}.png" width = "50">
  ```
- Inside the app.py file, add two more users, one with the role of reader and one with the role of admin.
- Write the admin_required(fn) function to your app.py file. This function will follow the template below:
  ```
  def admin_required(fn):
    @wraps(fn):
    def wrappers(*args, **kwargs):
        #add code below
    
        return fn(*args, **kwargs):
    return wrapper
  ```
- This function should get the claim from the users defined in your code and allow the users to add books only if their role is set to admin. If a user’s role is not equal to admin, then the function should return the following exception:
  ```
  return jsonify(msg = ‘Admins only!’), 403
  ```
- In your browser, navigate to localhost:5000/
- Log in using the admin username and password that you defined in your app.py file.
- After logging in, navigate to the “Books” tab. 
- Navigate to the “Add Books” tab. Then, log out of the admin account.
- Next, log in using the reader username and password that you defined in your app.py file. 
- Navigate to the “Add Books” tab. Try to add a new book. You should receive an error message.

#### Results
View the screenshots of these steps. 

