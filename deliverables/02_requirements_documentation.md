# Requirements Documentation

## 1. Purpose

This document defines what the Medical Chatbot system must do and how it should behave. It separates the required user-facing features from quality attributes such as security, maintainability, and performance.

## 2. Functional Requirements

### 2.1 Account Management

- Users shall be able to create a new account using the sign-up page.
- Users shall be able to log in using a valid username and password.
- Users shall be able to log out of the system.
- Users shall be able to reset their password if they forget it.

### 2.2 Identity Verification and Security

- The system shall send an email verification step before chatbot access is granted.
- The system shall restrict chatbot access for unverified users.
- The system shall apply login protection or rate limiting after repeated failed attempts.

### 2.3 Chatbot Interaction

- Users shall be able to enter a medical question through the chatbot interface.
- The system shall validate whether the user is permitted to use the chatbot.
- The system shall generate and display a response to the submitted question.
- The system shall maintain a readable conversation thread in the interface.

### 2.4 History and Administration

- Users shall be able to view their own chat history.
- Administrators shall be able to view all chat history records.
- The system shall store chat messages and responses in the database.

### 2.5 Configuration and Integration

- The system shall support environment-based configuration for email and API settings.
- The system shall support optional external AI/API-based response generation.

### 2.6 Privacy and Data Handling

- The system shall display a privacy and consent notice before chatbot use.
- The system shall require the user to acknowledge the notice before chatting.
- The system shall minimize stored medical text by masking obvious personal identifiers.
- The system shall keep chat history only for a defined retention period.
- The system shall allow users to export and delete their own chat history.

## 3. Non-Functional Requirements

### 3.1 Usability

- The interface shall be easy to understand for non-technical users.
- The layout shall be responsive so it can be used on standard laptop and desktop screens.

### 3.2 Security

- Sensitive values shall not be hardcoded in source files.
- Authentication, verification, and role checks shall protect restricted pages.
- The application shall minimize exposure of private user data in views and templates.

### 3.3 Maintainability

- The application shall use modular Django files such as views, templates, and static assets.
- The codebase shall be organized so that features can be extended without major rewrites.

### 3.4 Performance and Reliability

- Pages shall load in a reasonable time during local development.
- The system shall continue to function even when optional external services are not configured.

### 3.5 Security Hardening

- The system shall load secrets from environment variables in production.
- The system shall support secure cookie and HTTPS-related settings when deployed outside development.
- The system shall avoid storing sensitive values directly in source code.

## 4. Use Cases

### Use Case 1: Register Account

- **Actor:** New user
- **Goal:** Create a valid account
- **Precondition:** The user is not already signed in.
- **Main Flow:**
  1.  User opens the sign-up page.
  2.  User enters account details.
  3.  System validates the form.
  4.  Account is created.
  5.  Verification email is issued.
- **Postcondition:** A new account exists and the user can verify their email.

### Use Case 2: Log In

- **Actor:** Registered user
- **Goal:** Access the application
- **Precondition:** The user has a valid account.
- **Main Flow:**
  1.  User opens the login page.
  2.  User submits credentials.
  3.  System authenticates the user.
  4.  User is redirected to the chatbot page.
- **Postcondition:** The user is authenticated and can continue using the system.

### Use Case 3: Ask a Medical Question

- **Actor:** Verified patient or doctor
- **Goal:** Receive an answer from the chatbot
- **Precondition:** The user is logged in and allowed to chat.
- **Main Flow:**
  1.  User types a health-related question.
  2.  System checks access and verification status.
  3.  Backend sends the input to the chatbot logic or API.
  4.  Response is returned and shown in the interface.
  5.  Conversation is saved.
- **Postcondition:** The conversation is visible and stored.

### Use Case 4: Review Chat History

- **Actor:** User or administrator
- **Goal:** Review previous conversations
- **Precondition:** The actor is logged in.
- **Main Flow:**
  1.  Actor opens the history page.
  2.  System retrieves saved chat records.
  3.  Records are displayed in chronological order.
- **Postcondition:** Past conversations are available for review.

## 5. Activity Flow Summary

1. User opens the website.
2. User either logs in or registers a new account.
3. System verifies access and email status.
4. User enters a question in the chatbot.
5. Backend processes the request and returns a response.
6. The system saves the conversation.
7. User can later open the history page to review previous messages.

## 6. UML Notes

In the final PDF, this section should be accompanied by:

- a use case diagram showing user, admin, and chatbot interactions;
- an activity diagram showing the login-to-chat flow;
- any supporting diagram labels or legends required by the course.

## 7. Privacy and Consent Summary

Before a user enters chat input, the system shows a privacy notice explaining consent, retention, export, deletion, and emergency limitations. This is especially important because the application may process health-related text.
