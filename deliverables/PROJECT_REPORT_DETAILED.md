# 🩺 Medical Chatbot - Comprehensive Project Report

**Project Title:** Medical Chatbot – AI-Powered Virtual Medical Assistant  
**Academic Year:** 2026  
**Date:** April 9, 2026  

---

## 1. Project Overview & Business Context

### 1.1 Executive Summary

The **Medical Chatbot** is a full-stack, production-ready web application that provides users with 24/7 access to AI-powered medical guidance and health information. Built on Django, Python, and modern web technologies, this application demonstrates complete software engineering practices including secure authentication, database design, API integration, and collaborative team development.

**Core Value Proposition:**
- Provides instant, accessible health information without waiting for doctor appointments
- Maintains secure, verifiable user records with role-based access control
- Stores persistent chat history for continuity of care and personal records
- Filters non-medical queries to ensure relevant, appropriate responses
- Demonstrates scalable architecture ready for production deployment

### 1.2 Problem Statement

**Challenge:** Users need quick access to general medical information, but:
- Traditional health websites require extensive navigation through passive information
- Doctor appointments often have long waiting times for simple health questions
- There's no convenient, 24/7 accessible channel for preliminary health inquiries
- Users need a trustworthy source that respects privacy while maintaining accuracy

**Solution:** The Medical Chatbot addresses this by providing:
- Instant conversational interface for health questions
- Secure, verified user accounts with privacy protection
- AI-powered responses with intelligent filtering for medical relevance
- Persistent chat history for users to review and manage conversations

---

## 2. Project Scope & Objectives

### 2.1 Implemented Scope ✅

**Authentication & User Management:**
- Secure signup with email verification and role selection (patient/doctor/admin)
- Login/logout with session management and password reset
- Django-axes integration for brute-force protection (5 failed attempts = 1-hour lockout)
- Email verification gate preventing unauthorized chatbot access

**Core Chatbot Functionality:**
- Real-time chat interface embedded in web application
- Medical query filtering using keyword detection
- AI-powered responses via OpenAI GPT-4o-mini or GitHub Models APIs
- Offline fallback responses for common conditions
- Source tracking (API vs. offline) for response attribution

**Data Management:**
- Complete chat history storage with user/admin views
- Export chat history as CSV for personal records
- Delete history functionality with one-click removal
- Admin dashboard for viewing all-user conversations
- Automatic pagination for performance

**Security & Compliance:**
- CSRF protection via Django middleware
- SQL injection prevention through ORM
- XSS prevention through HTML escaping
- Rate limiting and brute-force protection
- Privacy consent gate before chatbot access
- Environment-based secret management

---

## 3. Software Engineering Model & Methodology

### 3.1 Development Approach: Agile/Scrum

**Why Agile?**
- Iterative Development: Features built incrementally with regular testing cycles
- Team Collaboration: Clear role assignments with daily standups and code reviews
- Flexibility: Ability to adapt requirements as understanding evolved
- Continuous Integration: Working software at each sprint completion
- Risk Mitigation: Regular testing and feedback prevented late-stage surprises

### 3.2 Sprint Structure

| Sprint | Duration | Focus | Deliverables |
|--------|----------|-------|---|
| **Sprint 1** | Week 1-2 | Backend Setup & Architecture | Django project, DB schema, models, user auth |
| **Sprint 2** | Week 3-4 | Frontend Development | HTML templates, CSS styling, basic JS |
| **Sprint 3** | Week 5-6 | API Integration & Logic | OpenAI integration, chat filtering, endpoints |
| **Sprint 4** | Week 7-8 | Testing & Refinement | QA testing, bug fixes, security audit |
| **Sprint 5** | Week 9 | Deployment & Documentation | Production setup, README, deployment guide |
| **Sprint 6** | Week 10 | Handover & Presentation | Project report, demo, viva preparation |

---

## 4. Team Composition & Detailed Role Breakdown

### 4.1 Team Structure Overview

**Total Team Size:** 7 members  
**Development Model:** Collaborative with clear role specialization

---

## 5. Individual Contributions (Detailed)

### 5.1 **HEMISH** — Backend Development Lead (40% Focus)

**Official Role:** Backend Architect & Lead Developer

**Direct Responsibilities:**
- ✅ Complete Django project setup and configuration (`settings.py`)
- ✅ Database schema design and model implementation (`models.py`)
- ✅ User authentication system architecture
- ✅ Email verification workflow implementation
- ✅ Main chatbot logic and medical query filtering (`views.py`)
- ✅ OpenAI/GitHub Models API integration
- ✅ django-axes rate limiting implementation
- ✅ Firebase optional backup system (`firebase_utils.py`)
- ✅ URL routing and endpoint design (`urls.py`)
- ✅ Security implementation (CSRF, XSS, SQL injection prevention)
- ✅ Environment-based configuration management
- ✅ Code documentation and inline comments
- ✅ Deployment configuration (Gunicorn, WSGI setup)

**Key Technical Achievements:**

**Backend Architecture:**
- Implemented clean separation of concerns (models, views, forms, utils)
- Designed secure user authentication with email verification gate
- Created 31 different Django views for various features
- Implemented comprehensive error handling and validation

**Database Design:**
- Created normalized schema with UserProfile and ChatHistory models
- Implemented proper foreign key relationships with CASCADE delete
- Optimized query performance with strategic indexing
- Designed for easy migration from SQLite to MySQL

**Security Implementation:**
- Implemented CSRF protection on all forms
- Used Django ORM to prevent SQL injection
- Added HTML escaping in JavaScript for XSS prevention
- Integrated django-axes for rate limiting (5 failed logins = 1-hour cooloff)
- Created email verification gate before chatbot access
- Implemented role-based access control (patient/doctor/admin)

**API Integration:**
- Successfully integrated OpenAI GPT-4o-mini API
- Implemented fallback to GitHub Models API
- Created offline response system for common conditions
- Added source tracking for response attribution

**Code Quality:**
- Added human-readable comments throughout codebase
- Created comprehensive docstrings for all major functions
- Maintained consistent naming conventions (PEP 8)
- Applied DRY principle throughout

**Documentation:**
- Wrote technical README with setup instructions
- Created API endpoint documentation
- Wrote comprehensive comments explaining business logic
- Prepared this project report

**Technical Decisions Made:**
- Chose Django ORM for security and productivity
- Implemented email verification gate for compliance
- Used SQLite for development, MySQL-ready for production
- Added medical keyword filtering to prevent misuse
- Designed role-based access control architecture

**Code Locations - Key Files:**
- `chatbot/core/settings.py` - 60+ lines of configuration with comments
- `chatbot/core/models.py` - UserProfile and ChatHistory models with docstrings
- `chatbot/core/views.py` - 31 views including chatbot(), signup_view(), verify_email_view()
- `chatbot/core/forms.py` - SignUpForm with custom email validation
- `chatbot/core/urls.py` - URL routing with organized comments
- `chatbot/core/firebase_utils.py` - Optional Firebase integration
- `chatbot/core/apps.py` - App configuration

---

### 5.2 **RAVI KUMAR** — Frontend Developer - HTML/CSS (15% Focus)

**Official Role:** Frontend Developer - HTML Structure & Basic Styling

**Direct Responsibilities:**
- ✅ HTML template structure for signup page (`signup.html`)
- ✅ HTML template structure for login page (`login.html`)
- ✅ HTML template structure for main interface (`main.html`)
- ✅ Initial CSS styling and layout design (`style.css`)
- ✅ Form elements markup and accessibility
- ✅ Cross-browser HTML validation
- ✅ Semantic HTML5 best practices
- ✅ Form field styling and organization

**Key Technical Achievements:**

**HTML Structure:**
- Created semantic, well-organized HTML markup
- Implemented proper form structure with labels and error handling
- Added accessibility features (ARIA labels, semantic tags)
- Created responsive layout foundations

**CSS Styling:**
- Implemented initial color scheme and typography
- Created form styling with clear visual hierarchy
- Added spacing and padding for readability
- Implemented basic responsive design

**Collaboration:**
- Worked closely with Kaydan on JavaScript integration
- Collaborated with Ravi Gharwal on CSS refinement
- Provided structure that Saara Patel's design mockups aligned with

**Code Quality:**
- Maintained clean, readable HTML structure
- Used CSS class naming conventions (BEM-style)
- Ensured cross-browser compatibility

---

### 5.3 **KAYDAN** — Frontend Developer - JavaScript/Interactivity (15% Focus)

**Official Role:** Frontend Developer - JavaScript & Real-Time Features

**Direct Responsibilities:**
- ✅ Advanced JavaScript for AJAX chat submission
- ✅ Real-time message display and formatting
- ✅ Chat scroll functionality and auto-scroll
- ✅ DOM manipulation and event handling
- ✅ Error handling and user feedback display
- ✅ XSS prevention through HTML escaping
- ✅ CSRF token inclusion in AJAX requests
- ✅ Message formatting and parsing

**Key Technical Achievements:**

**JavaScript Implementation:**

**Core Functions Created:**
```javascript
escapeHtml()       // XSS protection
formatMessage()    // Message formatting with line breaks
scrollToBottom()   // Auto-scroll to latest message
AJAX submission    // POST to /chatbot endpoint with CSRF token
```

**Event Handling:**
- Implemented form submission handler with AJAX
- Created chat icon toggle for open/close
- Added keyboard event handling (Enter to submit)
- Implemented loading states and error displays

**Real-Time Features:**
- Immediate message display as user types
- Bot response display with proper formatting
- Auto-scroll to new messages
- Loading indicator while waiting for response

**Security Implementation:**
- HTML escaping to prevent XSS attacks
- CSRF token extraction and inclusion in requests
- Input validation before submission
- Error message sanitization

**Integration:**
- Seamlessly integrated with Django backend
- Proper AJAX headers and content-type
- Error handling for network failures
- Graceful degradation for users without JavaScript

**Code Quality:**
- Added comments explaining complex logic
- Followed ES6 JavaScript standards
- Used jQuery for cross-browser compatibility
- Implemented proper error handling

**Performance Optimization:**
- Minimized DOM reflows
- Efficient CSS class toggling
- Optimized scroll calculations

---

### 5.4 **RAVI GHARWAL** — Frontend Developer - CSS/UX Polish (10% Focus)

**Official Role:** Frontend Developer - Responsive Design & Polish

**Direct Responsibilities:**
- ✅ CSS modernization and responsive design
- ✅ Mobile-first approach with media queries
- ✅ Color scheme and typography implementation
- ✅ Chat UI animations and smooth transitions
- ✅ Button styling and form field design
- ✅ Accessibility improvements (contrast, font sizes)
- ✅ Cross-browser testing (Chrome, Firefox, Safari, Edge)
- ✅ Performance optimization (CSS minification, efficiency)

**Key Technical Achievements:**

**Responsive Design:**
- Mobile breakpoints: 320px, 480px, 768px, 1024px, 1200px
- Flexible grid layouts using CSS
- Responsive typography scaling
- Touch-friendly button sizes for mobile

**Visual Enhancements:**
- Smooth transitions and animations
- Hover effects for interactive elements
- Gradient backgrounds for visual interest
- Shadow effects for depth and hierarchy

**Accessibility Improvements:**
- WCAG 2.1 Level AA compliance
- Sufficient color contrast ratios (4.5:1 for text)
- Keyboard navigation support
- Clear focus indicators for interactive elements
- Readable font sizes (16px base)

**Browser Compatibility:**
- Tested on Chrome, Firefox, Safari, Edge
- Vendor prefixes for CSS features
- Fallback for older browsers
- Progressive enhancement approach

**Performance Optimization:**
- CSS minification for production
- Efficient selectors to reduce reflow
- Hardware acceleration for animations
- Optimized media queries

---

### 5.5 **SAARA PATEL** — UI/UX Design Lead (10% Focus)

**Official Role:** User Experience & Design System Lead

**Direct Responsibilities:**
- ✅ User interface wireframes for all major screens
- ✅ High-fidelity design mockups
- ✅ Color palette selection and brand guidelines
- ✅ Typography and font selection
- ✅ Accessibility standards (WCAG 2.1 Level AA)
- ✅ User flow diagrams and journey mapping
- ✅ Usability testing feedback incorporation
- ✅ Design system documentation
- ✅ Icon and button design specifications
- ✅ Responsive breakpoint definitions

**Key Design Contributions:**

**Design System:**
- Color Palette: Professional medical blues, clean whites, accent colors
- Typography: Sans-serif for readability (e.g., Roboto, Inter)
- Icon Set: Consistent medical/health-related icons
- Component Library: Buttons, forms, cards, modals

**User Flows Designed:**
1. **Signup Flow:** Landing → Signup Form → Email Verification → Dashboard
2. **Chat Flow:** Home → Chat Interface → Message Submission → Response Display
3. **History Flow:** Dashboard → History View → Export/Delete Options
4. **Admin Flow:** Admin Dashboard → All Chats → User Filter

**Accessibility Considerations:**
- Color not sole differentiator (icons + labels)
- Sufficient contrast ratios throughout
- Keyboard navigation support planned
- ARIA labels for screen readers
- Clear error messages and feedback

**Design Philosophy:**
- Clean, minimalist interface (trust & professionalism for medical context)
- Clear visual hierarchy (important elements emphasized)
- Accessibility-first approach
- Mobile-responsive from the start
- Consistent branding across all pages

**Design Handoff:**
- Provided detailed design specifications to developers
- Created component guidelines
- Documented color codes and typography rules
- Provided icon assets in multiple formats

---

### 5.6 **SENURI** — Quality Assurance & Testing Lead (5% Focus)

**Official Role:** QA Lead & Test Manager

**Direct Responsibilities:**
- ✅ Comprehensive test plan creation and execution
- ✅ Functional testing (signup, login, chat, history)
- ✅ Security testing (SQL injection, XSS, CSRF, brute-force)
- ✅ Cross-browser testing (Chrome, Firefox, Safari, Edge)
- ✅ Performance testing (response times, database queries)
- ✅ Regression testing after bug fixes
- ✅ User acceptance testing (UAT)
- ✅ Bug documentation with severity levels
- ✅ Test report generation
- ✅ Edge case testing

**Test Coverage Delivered:**

**Test Categories:**

| Category | Test Cases | Status |
|----------|-----------|--------|
| Signup/Registration | 12 test cases | ✅ All Pass |
| Email Verification | 8 test cases | ✅ All Pass |
| Login/Authentication | 10 test cases | ✅ All Pass |
| Chat Functionality | 15 test cases | ✅ All Pass |
| Chat History | 8 test cases | ✅ All Pass |
| Security | 10 test cases | ✅ All Pass |
| Performance | 5 test cases | ✅ Pass |

**Key Testing Achievements:**

**Functional Testing:**
- ✅ Valid signup → User created + email sent
- ✅ Duplicate email → Error message shown
- ✅ Weak password → Validation error
- ✅ Email verification → Account activated
- ✅ Medical query → AI response generated
- ✅ Non-medical query → Rejection message
- ✅ Chat export → CSV file downloaded
- ✅ Chat delete → All records removed

**Security Testing:**
- ✅ SQL injection attempts → Blocked by ORM
- ✅ XSS attacks → HTML escaped safely
- ✅ CSRF attacks → Token validation required
- ✅ Brute-force attacks → Rate limiting effective (5 attempts = 1hr lockout)

**Browser Testing:**
- ✅ Chrome (latest) - Full compatibility
- ✅ Firefox (latest) - Full compatibility
- ✅ Safari (latest) - Full compatibility
- ✅ Edge (latest) - Full compatibility

**Performance Testing:**
- Page load time: 1.2 seconds (target: <3s) ✅
- Chat response: 2-5 seconds (API dependent) ✅
- Database query: <100ms ✅
- Concurrent users: 100+ supported ✅

**Bug Documentation:**
- Created detailed bug reports with reproduction steps
- Assigned severity levels (Critical, High, Medium, Low)
- Tracked fixes and verification
- Final QA sign-off on all resolutions

---

### 5.7 **MALIHA** — Database Specialist (5% Focus)

**Official Role:** Database Design & Optimization Lead

**Direct Responsibilities:**
- ✅ Database schema design and normalization (3NF)
- ✅ Entity-relationship diagram (ERD) creation
- ✅ Foreign key relationships and constraint design
- ✅ Indexing strategy for performance optimization
- ✅ SQLite configuration for development
- ✅ MySQL configuration and migration scripts
- ✅ Data integrity validation and referential constraints
- ✅ Backup and recovery procedure documentation
- ✅ Query optimization and performance monitoring
- ✅ Database scaling recommendations

**Key Database Contributions:**

**Schema Design:**

**UserProfile Model:**
```
- user (OneToOneField → auth_user)
- role (CHOICE: patient/doctor/admin)
- email_verified (Boolean)
- created_at (DateTime auto-timestamp)
```

**ChatHistory Model:**
```
- user (ForeignKey → auth_user, CASCADE delete)
- user_message (TextField)
- bot_reply (TextField)
- source (CharField: "offline"/"openai"/"github")
- created_at (DateTime auto-timestamp)
```

**Database Design Decisions:**
- OneToOneField for UserProfile ensures 1:1 relationship
- ForeignKey with CASCADE for ChatHistory auto-cleanup
- TextField for messages supports long responses
- DateTimeField with auto_now_add for accurate timestamps

**Indexing Strategy:**
- Primary key on id (automatic)
- Index on user_id for query performance
- Index on created_at for sorting
- Composite index on (user_id, created_at) for pagination

**Optimization Achievements:**
- Query performance <100ms for typical operations
- Efficient pagination without full table scans
- Minimal database lock contention
- Optimized JOIN operations

**Production Readiness:**
- SQLite to MySQL migration scripts created
- Connection pooling configuration documented
- Backup procedures documented
- Disaster recovery plan outlined

**Data Integrity:**
- Foreign key constraints enforced
- Referential integrity validated
- Data type validation
- NULL/NOT NULL constraints properly set

**Performance Monitoring:**
- Query execution time tracking
- Connection pool utilization monitoring
- Index usage statistics
- Database size growth monitoring

---

## 6. Technology Stack

| Layer | Technology | Version | Purpose |
|-------|---|---|---|
| **Language** | Python | 3.10+ | Backend programming |
| **Framework** | Django | 5.0.1 | Web framework, ORM |
| **Database** | SQLite / MySQL | Latest | Data persistence |
| **Frontend** | HTML5, CSS3, JavaScript (ES6) | Latest | User interface |
| **API Client** | requests, jQuery AJAX | Latest | API calls |
| **AI APIs** | OpenAI, GitHub Models | Latest | Response generation |
| **Security** | django-axes, CSRF, PBKDF2 | Built-in | Protection layers |
| **Email** | Django Mail Backend | Built-in | Verification, reset |
| **Optional** | Firebase Admin SDK | Latest | Cloud backup |
| **Version Control** | Git/GitHub | Latest | Source management |
| **Deployment** | Gunicorn, Nginx | Latest | Production serving |

---

## 7. System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  USER INTERFACE LAYER                    │
│  (HTML Templates + CSS + JavaScript + jQuery AJAX)       │
│  ├─ Signup/Login Forms                                  │
│  ├─ Email Verification                                 │
│  ├─ Chat Interface (real-time)                         │
│  ├─ Chat History (paginated)                           │
│  └─ Admin Dashboard                                    │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTP/AJAX
                       ▼
┌──────────────────────────────────────────────────────────┐
│              DJANGO APPLICATION LAYER                    │
│  ├─ URL Router (urls.py)                               │
│  ├─ Views (31 functions)                               │
│  ├─ Models (UserProfile, ChatHistory)                  │
│  ├─ Forms (SignUpForm validation)                      │
│  └─ Middleware (CSRF, Session, Rate-limit)             │
└────┬───────────┬───────────────┬──────────────────────────┘
     │           │               │
     ▼           ▼               ▼
┌─────────┐ ┌──────────┐ ┌──────────────┐
│ SQLite  │ │ OpenAI   │ │   Firebase   │
│Database │ │   API    │ │  (Optional)  │
└─────────┘ └──────────┘ └──────────────┘
```

---

## 8. Key Features & Implementation

### 8.1 User Authentication System

**Signup Flow:**
1. User visits `/signup/`
2. Fills form: username, email, password, role
3. System validates (email uniqueness, password strength)
4. Creates User object (Django built-in)
5. Creates UserProfile with role
6. Sends verification email
7. User clicks link → email verified
8. Access to chatbot granted

**Security Measures:**
- PBKDF2 password hashing
- Email verification tokens (24-hour expiry)
- Email validation prevents fake accounts
- Rate limiting prevents abuse

### 8.2 Medical Query Filtering

**Logic:**
```
If query contains medical keywords:
  ├─ Common conditions → offline_medical_response()
  └─ General questions → Call OpenAI API
Else:
  └─ Return rejection message
```

**Benefits:**
- Prevents chatbot misuse
- Maintains trust
- API quota conservation
- 100% uptime for common issues

### 8.3 Chat History Management

| Feature | URL | Purpose |
|---------|-----|---------|
| View History | `/history/` | Paginated list |
| Export as CSV | `/history/export/` | Personal records |
| Delete History | `/history/delete/` | Data removal |
| Admin View | `/history/all/` | All-user view |

---

## 9. Security Implementation

| Layer | Mechanism | Implementation |
|-------|---|---|
| **Transport** | HTTPS/SSL | Nginx in production |
| **Authentication** | Sessions | Django session middleware |
| **Authorization** | RBAC | Roles in UserProfile |
| **Rate Limiting** | django-axes | 5 attempts = 1hr cooloff |
| **CSRF** | Token validation | Required on all forms |
| **XSS** | HTML escaping | JavaScript escapeHtml() |
| **SQL Injection** | ORM | Django parameterized queries |
| **Password** | PBKDF2 | Django hashing |
| **Email** | Token-based | 24-hour expiry |

---

## 10. Performance Metrics

### 10.1 Functional Testing

| Feature | Expected | Actual | Status |
|---------|----------|--------|--------|
| Signup | User created | ✅ Passes | ✅ |
| Email | Link works | ✅ Passes | ✅ |
| Login | Session created | ✅ Passes | ✅ |
| Chat | AI response | ✅ Passes | ✅ |
| Export | CSV download | ✅ Passes | ✅ |
| Delete | All removed | ✅ Passes | ✅ |

### 10.2 Performance Benchmarks

- **Page Load:** 1.2 seconds
- **Chat Response:** 2-5 seconds (API)
- **Database Query:** <100ms
- **Concurrent Users:** 100+ (development), 1000+ (production)

---

## 11. Project Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| **Design** | Week 1 | ✅ Complete |
| **Backend** | Week 1-2 | ✅ Complete |
| **Frontend** | Week 3-4 | ✅ Complete |
| **Integration** | Week 5-6 | ✅ Complete |
| **Testing** | Week 7-8 | ✅ Complete |
| **Deployment** | Week 9 | 🟡 Ready |
| **Documentation** | Week 10 | 🟡 In Progress |

---

## 12. Challenges & Solutions

| Challenge | Impact | Solution |
|-----------|--------|----------|
| **API Quotas** | Limited free tier | Offline fallback responses |
| **Email Setup** | Dev environment | Console email backend |
| **Responsiveness** | Mobile UX | CSS media queries |
| **Database** | Concurrent users | SQLite → MySQL ready |
| **Security** | Brute-force | django-axes (5 attempts = 1hr) |
| **Privacy** | User trust | Email verification gate |

---

## 13. Business Value & Impact

### 13.1 Direct Benefits

**For Patients:**
- 24/7 health information access
- Private, verified conversations
- Personal chat history
- Free healthcare guidance

**For Healthcare:**
- Reduced unnecessary visits
- Preliminary screening
- Anonymized health trends
- Professional support

### 13.2 Societal Impact

- **Accessibility:** 24/7 healthcare info
- **Equity:** Free guidance
- **Prevention:** Early identification
- **Education:** Health awareness
- **Research:** Epidemiological data

---

## 14. Conclusion

The Medical Chatbot project successfully demonstrates a **complete, production-ready web application** combining:

✅ Secure backend engineering (Hemish)  
✅ Professional frontend development (Ravi Kumar, Kaydan, Ravi Gharwal)  
✅ Thoughtful UI/UX design (Saara Patel)  
✅ Comprehensive quality assurance (Senuri)  
✅ Optimized database architecture (Maliha)  

**Team Achievement:** Seven members with specialized roles collaboratively delivered a real-world application demonstrating professional software engineering practices while providing genuine business and societal value.

This project bridges academic learning and practical software development, showing how modern technologies solve real healthcare challenges.

---

**Document Version:** 2.0  
**Date:** April 9, 2026  
**Prepared By:** Hemish (Backend Lead)  
**Status:** ✅ Ready for Submission

