# BK Furniture - HCMUT SOFTWARE PROJECT MANAGEMENT ASSIGNMENT


# Introduction
BK Furniture is a new e-commerce application that helps people to buy items about household, organization, ... Moreover, it provides two new points:

- Chatbot: for consulting and answering customers' questions.
- Custome Design: Customers are allowed to submit their design to our shop. After submitting, we will discuss together about the detail information so that we decide whether it is possible to do.

# Setting up the Environment

## Django Setting up
>**Note**
>PWD: bk_furniture_backend

1. Using Python version 3.10.0
2. Create a virtual environment to isolate our package dependencies locally
    ```
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
3. Install all requiring Python packages
    ```
    python3 -m pip install -r requirements.txt
    ```

## Database Setting up
>**Note**
>PWD: bk_furniture_backend

1. Using localhost database
    - Install Postgresql Database and GUI tool
    - Create a Database with details:
        - NAME: "BK_Furniture"
        - USER: "postgres"
        - PASSWORD: ""
        - HOST: "127.0.0.1"
        - PORT: "5432"
2. Locally starting database
3. Database migrations
    ```
    python3 manage.py makemigrations
    ```
    ```
    python3 manage.py migrate
    ```
4. Create superuser
    ```
    python3 manage.py createsuperuser
    ```
5. Runing the server
    ```
    python3 manage.py runserver
    ```