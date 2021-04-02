# SWApp

#### Video Demo:  https://youtu.be/sUuk3O5h06E
#### Description:
  SWApp is a platform where people can barter - swap(p)! - objects they don't use anymore or "services", such as piano or yoga lessons, small repairs and so on.
  Money is banned and everyone is free to give an item or service the value they see fit! (if someone is willing to give away their Ferrari for your wedding tape     good for you! 😉)
Also, people can decide to donate an object or a service to the platform without asking anything in return... That item or service will appear in the Donations board.
  
------
  
#### Platform Features:
- Authentication (Registration, Login and Logout).
- Changing password.
- Updating profile.
- Deleting account.
- Uploading Items and Services to the platform.
- Updating an Item or Service.
- Delete an Item or Service previously uploaded.
- Searching for SWAppers (Users) and Items/Services.
- Creating and sending SWApp requests (which are the platform's core fuctionality and consist in a User asking another User to exchange an Item or Service with something else).
- Deleting a SWApp request.
- Accepting or rejecting a received SWApp request.
- Receiving and checking notifications for various actions performed through the website including receiving SWApp requests or modifying profile and password.
- Donate an Item or Service to the platform to be given to someone who might need it.

------

#### Technologies Used:
- Mainly Python/Django with some CSS for styling and a little JavaScript. SQLite has been used as database engine.

------

#### Project Structure:
The swapp-django project uses a Django structure as its base.
In the project folder we can find a general settings.py file, a urls.py file (which includes all the swapp app urls in it plus the django default admin urls) and a wsgi.py file (a django file used for deployment).
In the swapp app folder we can find a bunch of sub-folders, namely forms, media, migrations, models, static, templates and views:
- In the Forms folder, as the name suggests, we have all those files whose task is to define the various forms (such as Profile or Item forms) fields and their types (some of them may have additional informations about the field CSS' class and so forth).
- The Media folder (in its Pictures sub-folder) contains all the images uploaded to the  platform.
- The Migrations folder contains all the additions/deletions/updates and more generally all the changes made to the database structure through the Django's models system.
- In the Models folder we can find the Django's version of the database structure, with a model file for each database table. Any change to those models files will reflect on the SQLite database structure through the aforementioned migrations.
- In the Static folder we store the CSS and JavaScript file(s).
- The Templates folder contains the files that in other frameworks would be named views (like in Ruby on Rails), HTML files named templates with some Django syntax in them to take care of the logic.
- The Views folder contains probably the most important files of the project, the views (known as controllers in RoR), whose task is to determine which actions need to be performed when a certain URL is called within the platform. Some of these actions might be logging in a User after running some checks, make the appropriate changes to the system when a SWApp request has been made, sending a notification after a profile update, and so forth.
- The last important file in the swapp folder is urls.py, which contains all the platform routes alongside with the method/function/action to be called when requested by the User.
