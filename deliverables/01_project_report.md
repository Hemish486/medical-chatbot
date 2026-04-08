# Project Report

## 1. Project Overview

The Medical Chatbot is a full-stack web application designed to provide a simple virtual assistant for general medical guidance. The system combines a Django backend with a browser-based frontend so that users can create accounts, verify their email addresses, log in securely, and interact with the chatbot through a clean user interface. The application also stores chat history, supports administrator access to all conversations, and can integrate with an external AI API when configured.

## 2. Project Scope

The project focuses on the core functions needed for a student-level healthcare support platform. The implemented scope includes:

- secure user registration, login, logout, and password reset;
- email verification before chatbot access;
- role-based access control for patient, doctor, and administrator users;
- chatbot conversation handling and response display;
- user-specific chat history and admin-wide history views;
- local database storage using SQLite;
- optional API-based model responses through environment-based configuration.

The project does not attempt to replace professional healthcare services. Instead, it provides informational guidance and demonstrates how a web application can combine authentication, data persistence, and interactive messaging.

## 3. Problem Statement

Users often need a quick and accessible way to ask general health-related questions. A traditional website may present information passively, while a chatbot provides a more interactive experience. This project addresses that need by offering a conversational interface that is easier to use than searching through static pages.

## 4. Business Value

The application provides value in three main ways:

1. **Faster access to information** — users can ask questions directly rather than navigating multiple pages.
2. **Improved continuity** — previous chats are saved so users can review earlier responses.
3. **Controlled access** — authentication, verification, and role checks help keep the system organized and secure.

For a coursework setting, the project also demonstrates practical software engineering skills such as backend development, UI design, security handling, and documentation.

## 5. Software Engineering Model

The project follows an iterative development approach similar to Agile. The system was not built in a single pass. Instead, core features were implemented in stages, tested, and refined. This model was appropriate because the requirements evolved while the interface, authentication rules, and chatbot behavior were being improved.

This approach supported continuous feedback and allowed the codebase to remain maintainable. Each stage of work produced a usable version of the application, which is a strong fit for a student project that combines both backend and frontend development.

## 6. Tools, Languages, and Frameworks

The project used the following technologies:

- **Backend language:** Python
- **Web framework:** Django
- **Frontend languages:** HTML, CSS, JavaScript
- **Database:** SQLite (default configuration; MySQL optional)
- **Version control:** Git
- **Supporting packages:** `django-axes`, `python-dotenv`, `requests`, optional Firebase support

These tools were selected because they allow rapid development, clear separation of concerns, and reliable integration with modern web application workflows.

## 7. System Features Delivered

The final application includes:

- account creation and authentication;
- email verification and password recovery;
- chatbot conversation UI with modern styling;
- chat history storage and display;
- admin history access;
- protection against repeated login failures;
- environment-based configuration for sensitive values.

## 8. Security and Data Handling

Because the application deals with health-related conversations, the project includes several protective measures:

- a privacy and consent notice before chatbot use;
- automatic minimization of chat records by masking obvious personal identifiers before storage;
- chat-history retention limits so old data can be removed after a defined period;
- export and deletion controls so users can manage their own stored chat data;
- production-oriented settings options for environment-based secrets, secure cookies, and HTTPS-related flags when DEBUG is disabled.

These controls are intended to reduce unnecessary data exposure and show good handling of sensitive information in a medical-style application.

## 9. Contribution Statement

If the work was completed individually, the same student is responsible for analysis, design, implementation, testing, and documentation. If the work was completed as a team, this section should be replaced with a short breakdown of each member’s contribution.

## 10. Conclusion

The Medical Chatbot project demonstrates a complete full-stack solution with a usable interface, a structured backend, and a documented development process. It shows how a lightweight Django application can support authentication, messaging, persistence, and documentation requirements in a single system.
