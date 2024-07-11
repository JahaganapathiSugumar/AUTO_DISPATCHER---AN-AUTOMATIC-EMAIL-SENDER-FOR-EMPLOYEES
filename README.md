# AUTO_DISPATCHER---AN-AUTOMATIC-EMAIL-SENDER-FOR-EMPLOYEES
The Email Management System is a versatile application designed to streamline user management and automate email communication. Built with Python, it leverages Tkinter for the GUI, MySQL for database management, and Python's email modules for sending customized emails based on user roles.

The Email Management System is a comprehensive application designed to streamline the process of managing users and automating email communications. It allows for efficient user registration, validation, and email dispatch, tailored to different user roles such as clients, project managers, and residents. This project leverages a combination of Tkinter for the user interface, MySQL for database management, and Python's email capabilities to provide a robust solution for handling user information and communication.

Key Features:

  User Registration and Management:
  
      Register multiple users by capturing their name, email, and role.
      Automatically generate unique user IDs with a role-specific prefix.
      Store user details in both CSV files and a MySQL database for persistent storage and easy access.
  
  Email Validation and Dispatch:
  
        Validate user emails to ensure correctness before sending.
        Send role-specific, customized emails to users upon validation.
        Maintain a record of sent emails, including subjects and body content, for future reference.
  
  Database Integration:
  
      Utilize MySQL to store and manage user data.
      Separate users into all_users, pending_users, and sent_users tables based on their email status.
      Update user information and manage email statuses seamlessly through SQL queries.
  
  CSV File Handling:
  
      Export user data and email logs to CSV files for backup and reporting.
      Handle pending and sent user data, ensuring synchronization between the database and CSV files.
  
  Graphical User Interface (GUI):
  
      Provide an intuitive GUI for user interaction built with Tkinter.
      Enable user actions such as registration, viewing pending users, and checking sent email logs through simple button clicks and form inputs.
      
   How It Works
  
   User Registration:
    
        Users can be registered through a Tkinter form where their name, email, and role are entered.
        Upon submission, user details are stored in both CSV files and the MySQL database.
        Unique user IDs are generated and associated with each user based on their role.
  
   Email Validation and Sending:
    
      The system validates user emails using regular expressions.
      Valid emails trigger the sending of customized emails, and the user's status is updated in the database.
      Invalid emails prompt the user to update their email address through the GUI.
  
   Database and CSV Management:
    
      User details and email logs are managed in a MySQL database and synchronized with CSV files.
      The system allows for updating user email addresses and records these changes across all storage formats.
      Sent emails are logged with detailed records, including email subjects and bodies.
  
  User Interface Interaction:
    
      The GUI enables users to register new users, view pending users, and check sent email logs.
      Actions are performed through a combination of form entries, dropdowns, and buttons, ensuring ease of use.
