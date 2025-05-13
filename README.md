
# AWS-Marvel-DC-Movie-Webapp



A web application that allows users to browse, add, and manage a database of Marvel and DC movies.

---

## Overview

This application provides a simple interface to manage a collection of Marvel and DC superhero movies. The project consists of:

- A frontend built with HTML, CSS, and JavaScript (hosted on AWS S3)  
- A Flask backend API with PostgreSQL database integration  
- Deployed on AWS infrastructure (EC2 for the application and RDS for the database)

---

## Features

- View the complete list of Marvel/DC movies  
- Sort movies by various attributes (ID, title, year, genre, runtime, IMDb score)  
- Add new movies to the database  
- Delete existing movies  
- Responsive design for various screen sizes  

---

## Tech Stack

### Frontend

- HTML5  
- CSS3  
- Vanilla JavaScript (no frameworks)

### Backend

- Python  
- Flask web framework  
- PostgreSQL database  
- Flask-CORS for cross-origin requests  

---

## Deployment

- **AWS EC2** for hosting the application  
- **AWS RDS** for PostgreSQL database  

---

## Project Structure
```
marvel-dc-movie-db/
├── static/
│ └── index.html # Frontend HTML/CSS/JS
├── app.py # Flask backend API
├── requirements.txt # Python dependencies
└── README.md # Project documentation

```
---

## Deployment Architecture

The application is deployed on AWS with the following configuration:

### Frontend Hosting

- The frontend file (`index_zohaib.html`) is stored in an Amazon S3 bucket  
- Static website hosting is enabled on the S3 bucket for public access  
- This approach provides high availability and scalability for the frontend  

### Backend Services

- EC2 instance running the Flask application on port 5050  
- RDS PostgreSQL instance for the database  
- Security groups configured to allow necessary traffic between components  

---

## Database

- AWS RDS PostgreSQL instance hosts the Marvel/DC movie data  
- The database schema includes movie details like title, year, genre, runtime, and IMDb scores  

---

## AWS Integration

This project demonstrates integration of multiple AWS services to create a complete web application:

### S3 (Simple Storage Service)

- Hosts the static frontend file (`index_zohaib.html`)  
- Provides reliable and scalable web content delivery  

### EC2 (Elastic Compute Cloud)

- Runs the Flask backend application  
- Handles API requests and database operations  

### RDS (Relational Database Service)

- Manages the PostgreSQL database  
- Stores all movie data securely  

---

## Acknowledgements

- Marvel and DC Comics for the amazing superhero universes  
- The IMDb database for movie information  
- AWS for cloud infrastructure services
