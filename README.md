Real Estate Website

This is a real estate website built using Django and React. The website allows registered users to manage their properties for sale or rent, while visitors can browse listings, contact the real estate agent, and more. The project utilizes the Django Rest Framework for the API and React for the client-side.

Features
•	User Registration and Authentication: Users can create accounts and log in to access additional features.
•	Property Management: Registered users can add, edit, and delete their property listings.
•	Property Search: Visitors can search for properties based on various criteria such as location, price range, and property type.
•	Contact Form: Visitors can send inquiries to the real estate agent via a contact form.
•	AWS Infrastructure: The website is hosted on AWS, utilizing the AWS EC2 server for the Django server, AWS RDS for the PostgreSQL database, and AWS S3 for storing static files.

Installation
To run the project locally, follow these steps:
1.	Clone the repository: git clone https://github.com/elonlevi2/Nadlan.git
2.	Install backend dependencies: pip install -r requirements.txt
3.	Install frontend dependencies: cd frontend && npm install
4.	Set up the database: Create a PostgreSQL database and configure the database settings in settings.py.
5.	Apply database migrations: python manage.py migrate
6.	Start the backend server: python manage.py runserver
7.	Start the frontend development server: cd frontend && npm start

   Make sure you have Python, Node.js, and PostgreSQL installed on your system.

Configuration
To configure the project, you may need to update some settings:
•	Django settings: Update the database configuration, AWS S3 settings, and any other relevant settings in the settings.py file.
•	AWS credentials: Set up your AWS credentials on your local machine or provide them through environment variables.
•	Django REST Framework: Configure the API endpoints and permissions according to your requirements.
•	Gunicorn: Configure Gunicorn settings, such as the number of workers, bind address, etc., in the gunicorn.conf.py file.
•	Nginx: Configure Nginx settings, including server blocks, proxy_pass, SSL certificates, etc., in the Nginx configuration files.




Deployment
To deploy the website with Gunicorn and Nginx, you can follow these general steps:
1.	Set up an EC2 instance: Launch an EC2 instance on AWS with the appropriate configuration for your project.
2.	Install required software: Install Python, PostgreSQL, Nginx, and any other necessary dependencies on the EC2 instance.
3.	Transfer project files: Transfer your project files to the EC2 instance using SCP or any other preferred method.
4.	Configure the web server: Set up Nginx as the reverse proxy server and configure it to pass requests to Gunicorn.
5.	Set up PostgreSQL: Install and configure PostgreSQL on the EC2 instance and import your database.
6.	Set up AWS S3: Create an S3 bucket on AWS and configure your Django settings to use it for storing static files.
7.	Start Gunicorn: Configure Gunicorn to run your Django application and start it as a background process.
8.	Start Nginx: Start Nginx to listen for incoming requests and forward them to Gunicorn.
9.	Configure domain and DNS: Set up a domain name for your website and configure DNS settings to point to your EC2 instance's IP address.


Please note that these steps provide a high-level overview and may require further research and customization based on your specific AWS setup and requirements.

Contributing
Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open a new issue or submit a pull request.

Acknowledgments
•	Django
•	Django Rest Framework
•	React
•	AWS
