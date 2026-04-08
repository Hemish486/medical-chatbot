# Design Documentation

## 1. Architecture Overview

The Medical Chatbot uses a layered web architecture built on Django. This keeps the presentation, application logic, and data storage responsibilities separate, which improves clarity and maintainability.

### Layer 1: Presentation Layer

The presentation layer contains the HTML templates, CSS styling, and JavaScript interactivity. This layer renders the pages the user sees, including the chatbot screen, login pages, history views, and password reset screens.

### Layer 2: Application Layer

The application layer is implemented in Django views and supporting authentication logic. It handles page rendering, form processing, chatbot request handling, access control, and role-based restrictions.

### Layer 3: Data Layer

The data layer stores user accounts, profiles, and conversation history in SQLite. Optional external services can be used for AI response generation or Firebase persistence.

## 2. System Components

### 2.1 `core/views.py`

This file contains the main request-handling logic. It processes chatbot messages, login-related behavior, email verification flows, and history pages.

### 2.2 Templates

The `templates/` directory contains all user-facing pages. The project uses separate templates for the chatbot home page, login, signup, password reset pages, and history views.

### 2.3 Static Assets

The `static/` directory stores the shared CSS and JavaScript files. These files provide the visual theme and support chat interaction behavior.

### 2.4 Models and Storage

The model layer stores user profile information and chat history records. This allows the application to track conversations and display them later.

## 3. Dependencies

The project depends on the following technologies:

- Django for the web framework
- Requests for HTTP API calls
- python-dotenv for environment variable loading
- django-axes for login attempt protection
- SQLite for local database storage
- Optional Firebase integration for alternative persistence
- Optional AI API service for generated responses

## 4. Data Flow

1. The user opens the interface and submits a chat question.
2. JavaScript sends the input to a Django endpoint.
3. Django validates the session, role, and email verification status.
4. The backend determines whether the response should come from local logic or an external API.
5. The returned answer is sent back to the browser.
6. The conversation is stored for later viewing.
7. The user can open the history page to review previous entries.

## 5. User Interface Design

### 5.1 Chat Page

The chatbot page uses a top navigation bar, a content shell, and a message panel. The message area shows the bot greeting, user messages, and bot replies in a conversational layout.

### 5.2 Authentication Pages

The login, signup, and password reset pages use a centered card design. Each page includes a heading, supporting text, form fields, and action buttons.

### 5.3 History Pages

The history views display conversation records as stacked cards. Each record contains the message metadata, user message, and bot response.

## 6. Wireframe Notes

The final PDF should include simple wireframes for:

- the chatbot page;
- the login/sign-up pages;
- the history page;
- the admin history page.

## 7. UML Class Diagram Notes

The final PDF should include a class diagram showing the relationship between the user, user profile, and chat history entities, as well as how views interact with those models.
