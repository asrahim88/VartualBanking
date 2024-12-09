# VirtualBanking

[Live Demo of VirtualBanking](https://virtualbanking.onrender.com/)

## Project Overview
"VirtualBanking" is a Django-based web application designed to provide a secure and efficient online banking experience. It offers two types of users: regular users who can view the homepage and learn about banking features, and registered users who can fully access banking features by creating an account. The application ensures complete security for personal and banking data and includes multiple functionalities such as account creation, profile management, and banking operations like deposit, withdrawal, and loan management.

---

## Key Features

### 1. User Registration & Authentication
- **Two Types of Users**:
  - General Users: Can browse the homepage and learn about the banking features without logging in.
  - Registered Users: Must create an account to access full banking features.
  
- **Account Creation Requirements**:
  - Unique username, email, mobile number, and National ID (NID) number.
  - Personal information including first name, last name, email, phone number, birthdate (must be above 18), gender, NID, account type, street address, postal code, city, country.
  - Profile picture upload during account creation.
  - Password and confirmation password to ensure account security.

- **Account Creation Validation**:
  - Age verification for users below 18 years.
  - Unique username, email, mobile number, and NID check.

---

### 2. Banking Features for Logged-In Users
- **Profile Information**:
  - After logging in, users can view their profile, including their unique bank account number generated automatically.
  - Users can view and manage personal details and banking operations.

- **Banking Operations**:
  - **Deposit & Withdrawal**: Users can deposit money into their accounts or withdraw funds.
  - **Loan Application**: Users can apply for a loan. A maximum of 3 loan requests can be made at a time.
  - **Loan Approval**: Upon loan approval, funds are transferred into the user’s account.
  - **Transaction History**: Users can view detailed transaction history, including transaction date, amount, and type.

---

### 3. Profile Management & Password Reset
- **Profile Update**:
  - Users can update their profile information (except for username and bank account number).
  - Users can change their password anytime.

- **Forgot Password**:
  - If a user forgets their password, they can reset it via email.
  - A password reset link is sent to the user’s email, allowing them to change their password securely.

---

### 4. Admin Dashboard
- **Admin Panel**: 
  - Admin can manage users and monitor activities, such as approving loan requests and viewing transaction history.

---

## Tech Stack
- **Backend**: Django
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Database**: SQLite (for development)
- **Authentication**: Django's built-in authentication system
- **Hosting**: Render for deployment

---

## Screenshots

### Home Page
![Home Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/HomePage.png)

### Login Page
![Login Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/loginPage.png)

### Registration Page
![Registration Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/registrationPage.png)

### Profile Page
![Registration Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/profilePage.png)

### Deposit Page
![Deposit Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/depositMoneyPage.png)

### Withdraw Page
![Withdraw Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/withdrawPage.png)

### Loan Request Page
![Loan Request Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/loanRequestPage.png)

### View All Loan Requests Page
![All Loan Requests Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/showAllLoanRequestsPage%20.png)

### All Transaction Reports Page
![All Transaction Reports Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/allTransaction%20reoprtsPage.png)

### Change Password Page
![Change Password Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/passwordChangePage.png)

### Forgot Password Page
![Forgot Password Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/forgotPasswordPage.png)

### Check Email Page
![Forgot Password Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/checkEmailPage.png)

### Password Reset Page
![Forgot Password Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/resetPasswordForm.png)

### Password Reset Complete Page
![Forgot Password Page](https://github.com/asrahim88/VirtualBanking/blob/main/screenShots/passwordResetCompletePage.png)


---

## Getting Started

### Prerequisites
Before running the project locally, make sure you have the following installed:
- Python (3.x)
- Django
- PostgreSQL (if using production database)
- Tailwind CSS (for styling)

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/asrahim88/VirtualBanking.git
    ```

2. Navigate to the project directory:

    ```bash
    cd VirtualBanking
    ```

3. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations to set up the database:

    ```bash
    python manage.py migrate
    ```

5. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

6. Access the application at [http://localhost:8000](http://localhost:8000).

---

## Why Choose This Project?

- **Comprehensive Banking Solution**: The project provides a comprehensive banking platform, allowing users to manage their accounts and perform various banking operations securely.
- **Secure and Scalable**: Built with Django, which is a reliable framework for handling sensitive financial data.
- **User-Centric Features**: Designed to ensure a smooth experience for both general and registered users, with secure authentication and detailed transaction reports.
- **Easy to Maintain**: The Django framework makes it easy to maintain and scale as needed, with an admin panel for managing users and overseeing banking operations.

---

