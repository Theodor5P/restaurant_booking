# Restaurant Booking System


A comprehensive Django-based restaurant booking system that allows customers to make, manage, and track their restaurant reservations online. The system features role-based access control, real-time availability checking, and an intuitive user interface for both customers and restaurant staff.

The live link can be found here - [Restaurant Booking System](https://p5-restaurant-booking-22136e9a206d.herokuapp.com/)

The Github link can be found here - [Restaurant Booking System](https://p5-restaurant-booking-22136e9a206d.herokuapp.com/)

## Contents

- [User Experience (UX)](#user-experience-ux)
  - [Project Goals](#project-goals)
  - [User Stories](#user-stories)
  - [Design](#design) 
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Future Features](#future-features)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Deployment](#deployment)


## User Experience (UX)

### Project Goals

The Restaurant Booking System aims to modernize the traditional restaurant reservation process by providing:

- **Streamlined Booking Process**: Allow customers to book tables online 24/7
- **Real-time Availability**: Display live availability for different time slots
- **User Management**: Comprehensive user profiles and booking history
- **Staff Dashboard**: Enable restaurant staff to manage bookings efficiently
- **Responsive Design**: Ensure seamless experience across all devices

### User Stories

#### First Time Visitor Goals

- As a first time visitor, I want to easily understand the purpose of the site and learn about the restaurant
- As a first time visitor, I want to view available time slots and restaurant information without creating an account
- As a first time visitor, I want to easily register for an account to make bookings
- As a first time visitor, I want the navigation to be intuitive and user-friendly

#### Returning Visitor Goals

- As a returning visitor, I want to quickly log in to my account
- As a returning visitor, I want to view my booking history and upcoming reservations
- As a returning visitor, I want to easily modify or cancel existing bookings
- As a returning visitor, I want to check availability for specific dates and times

#### Customer Goals

- As a customer, I want to make new restaurant bookings with ease
- As a customer, I want to specify party size and special dietary requirements
- As a customer, I want to receive confirmation of my booking details
- As a customer, I want to manage all my bookings from a single dashboard
- As a customer, I want to cancel bookings when plans change

#### Restaurant Staff Goals

- As restaurant staff, I want to view all bookings for today and upcoming dates
- As restaurant staff, I want to see customer details and special requests
- As restaurant staff, I want to track booking statuses (confirmed, completed, cancelled)
- As restaurant staff, I want to manage restaurant capacity and time slots

### Design

#### Color Scheme

The website uses a sophisticated color palette that reflects the restaurant industry:

- **Primary Gold (#d4af37)**: Used for call-to-action buttons and highlights, representing luxury and quality
- **Dark Navigation (#343a40)**: Professional dark gray for the navigation bar
- **Bootstrap Colors**: Success green, danger red, and warning amber for status indicators
- **Clean Whites and Grays**: For optimal readability and modern aesthetics

#### Typography

- **Primary Font**: System fonts with Bootstrap's native font stack for optimal performance
- **Icons**: Font Awesome 6.0.0 for consistent iconography throughout the application
- **Hierarchy**: Clear typographic hierarchy using Bootstrap's heading classes

#### Imagery

- **Hero Background**: High-quality restaurant interior image from Unsplash
- **Icons**: Font Awesome icons for navigation, status indicators, and user actions
- **Cards**: Clean card-based layout for displaying booking information


## Features

### Existing Features

#### **User Authentication & Profiles**
- **User Registration**: Complete registration form with profile creation
- **Secure Login/Logout**: Django's built-in authentication system
- **User Profiles**: Extended profiles with phone numbers and role management
- **Role-Based Access**: Different access levels for customers, staff, and admins

#### **Restaurant Management**
- **Restaurant Information**: Comprehensive restaurant details (capacity, hours, contact)
- **Time Slot Management**: Configurable booking time slots
- **Capacity Management**: Real-time capacity tracking and availability calculation
- **Staff Dashboard**: Overview of today's bookings and upcoming reservations

#### **Booking System**
- **Create Bookings**: User-friendly booking form with date/time selection
- **Availability Checking**: Real-time availability display for selected dates
- **Booking Management**: View, edit, and cancel existing bookings
- **Capacity Validation**: Automatic validation against restaurant capacity
- **Special Requests**: Text field for dietary requirements and special occasions

#### **User Interface**
- **Responsive Design**: Bootstrap 5.3.0 for mobile-first responsive design
- **Intuitive Navigation**: Clear navigation with user-specific menu items
- **Status Indicators**: Color-coded badges for booking statuses
- **Interactive Forms**: Client-side validation and user-friendly error messages
- **Search & Filtering**: Filter bookings by date, status, and time slots

#### **Data Management**
- **CRUD Operations**: Full Create, Read, Update, Delete functionality for bookings
- **Data Validation**: Comprehensive server-side validation for all forms
- **Database Relationships**: Properly structured foreign key relationships
- **Unique Constraints**: Prevent duplicate bookings for same customer/time/date

### Future Features

- **Email Notifications**: Automated confirmation and reminder emails
- **Payment Integration**: Online payment processing for deposits
- **Menu Integration**: Display restaurant menu with booking system
- **Reviews & Ratings**: Customer feedback system
- **Mobile App**: Native mobile application
- **Multi-Restaurant**: Support for multiple restaurant locations
- **Advanced Analytics**: Booking trends and customer insights
- **SMS Notifications**: Text message confirmations and reminders

## Technologies Used

### Languages Used

- [HTML5](https://en.wikipedia.org/wiki/HTML5)
- [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- [Python](https://www.python.org/)

### Frameworks, Libraries & Programs Used

1. **[Django 4.2.23](https://www.djangoproject.com/)** - Main web framework
2. **[Bootstrap 5.3.0](https://getbootstrap.com/)** - CSS framework for responsive design
3. **[Font Awesome 6.0.0](https://fontawesome.com/)** - Icons throughout the website
4. **[PostgreSQL](https://www.postgresql.org/)** - Production database (Heroku)
5. **[SQLite](https://www.sqlite.org/)** - Development database
6. **[Gunicorn](https://gunicorn.org/)** - Python WSGI HTTP Server
7. **[dj-database-url](https://pypi.org/project/dj-database-url/)** - Database URL parsing
8. **[Heroku](https://www.heroku.com/)** - Cloud deployment platform
9. **[Git](https://git-scm.com/)** - Version control
10. **[GitHub](https://github.com/)** - Code repository hosting
11. **[Visual Studio Code](https://code.visualstudio.com/)** - IDE

### Django Packages

- **django.contrib.admin** - Admin interface
- **django.contrib.auth** - Authentication system
- **django.contrib.messages** - Flash messages
- **django.contrib.sessions** - Session management

## Testing

### Validator Testing

#### HTML
- All HTML pages passed through the [W3C Markup Validator](https://validator.w3.org/)
- No errors or warnings found

#### CSS
- CSS passed through the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/)
- No errors found

#### Python
- All Python code follows PEP 8 standards
- Code passed through [PEP8 Online Checker](http://pep8online.com/)
- No errors found

#### Accessibility
- Pages tested using [WAVE Web Accessibility Evaluator](https://wave.webaim.org/) and Lighthouse 
- High contrast ratios maintained throughout
- Alt text provided for all images
- Semantic HTML structure implemented

### Manual Testing

#### User Registration & Authentication
| Test | Expected Result | Actual Result | Pass/Fail |
|------|----------------|---------------|-----------|
| User can register with valid details | Account created successfully | Account created successfully | Pass |
| User cannot register with existing username | Error message displayed | Error message displayed | Pass |
| User can login with correct credentials | Redirected to dashboard | Redirected to dashboard | Pass |
| User cannot login with incorrect credentials | Error message displayed | Error message displayed | Pass |
| User can logout successfully | Redirected to home page | Redirected to home page | Pass |

#### Booking Management
| Test | Expected Result | Actual Result | Pass/Fail |
|------|----------------|---------------|-----------|
| User can create new booking | Booking saved to database | Booking saved to database | Pass |
| System prevents overbooking | Error message when capacity exceeded | Error message when capacity exceeded | Pass |
| User can view their bookings | All user bookings displayed | All user bookings displayed | Pass |
| User can edit upcoming bookings | Changes saved successfully | Changes saved successfully | Pass |
| User can cancel confirmed bookings | Booking status updated to cancelled | Booking status updated to cancelled | Pass |
| User cannot book past dates | Error message displayed | Error message displayed | Pass |

#### Availability Checking
| Test | Expected Result | Actual Result | Pass/Fail |
|------|----------------|---------------|-----------|
| Availability shows correct capacity | Real-time capacity calculated | Real-time capacity calculated | Pass |
| Fully booked slots show as unavailable | Correct status displayed | Correct status displayed | Pass |
| Available slots allow booking | Booking form pre-populated | Booking form pre-populated | Pass |

#### Staff Dashboard
| Test | Expected Result | Actual Result | Pass/Fail |
|------|----------------|---------------|-----------|
| Staff can view today's bookings | All today's bookings displayed | All today's bookings displayed | Pass |
| Staff can access booking details | Detailed view available | Detailed view available | Pass |
| Non-staff users cannot access dashboard | Access denied message | Access denied message | Pass |

### Browser Testing

The website was tested on the following browsers:
- **Google Chrome** (Latest version) - Full functionality
- **Mozilla Firefox** (Latest version) - Full functionality
- **Microsoft Edge** (Latest version) - Full functionality

### Device Testing

The website was tested on various devices:
- **Desktop** (1920x1080) - Excellent
- **Laptop** (1366x768) - Excellent
- **Tablet** (iPad) - Good
- **Mobile** (iPhone 12/13) - Good
- **Mobile** (Samsung Galaxy) - Good

### Known Issues

1. **Date Picker Styling**: Some browsers may display the date picker differently
2. **Long Restaurant Names**: Very long restaurant names may cause layout issues on small screens
3. **Time Zone Handling**: Currently uses UTC, may need localization for different regions

## Deployment

### Local Development

#### Requirements
- Python 3.8+
- pip package manager
- Git

#### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Theodor5P/restaurant_booking.git
   cd restaurant_booking
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment variables**
   Create `env.py` in the root directory:
   ```python
   import os
   
   os.environ["SECRET_KEY"] = "your-secret-key-here"
   os.environ["DATABASE_URL"] = "sqlite:///db.sqlite3"
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Setup initial data**
   ```bash
   python manage.py setup_timeslots
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Heroku Deployment

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Deployment Steps

1. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DATABASE_URL="your-postgres-url"
   ```

3. **Add Heroku Postgres**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Deploy to Heroku**
   ```bash
   git push heroku main
   ```

5. **Run migrations on Heroku**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py setup_timeslots
   heroku run python manage.py createsuperuser
   ```

#### Heroku Configuration Files

**Procfile**
```
web: gunicorn restaurant_booking.wsgi
```

**requirements.txt**
```
asgiref==3.9.0
dj-database-url==0.5.0
Django==4.2.23
gunicorn==20.1.0
psycopg2==2.9.10
setuptools==80.9.0
sqlparse==0.5.3
tzdata==2025.2
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| SECRET_KEY | Django secret key for security | Yes |
| DATABASE_URL | Database connection string | Yes |
| DEBUG | Set to False in production | Yes |

## Credits

### Code

- [Django Documentation](https://docs.djangoproject.com/) - Django framework guidance
- [Bootstrap Documentation](https://getbootstrap.com/docs/) - CSS framework implementation
- [MDN Web Docs](https://developer.mozilla.org/) - JavaScript and HTML reference
- [Stack Overflow](https://stackoverflow.com/) - Problem-solving and code snippets
- [Django Tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/) - Initial project structure

### Content

- Restaurant description and content created by the developer
- User stories and feature descriptions written by the developer
- All text content is original

### Media

- **Hero Image**: Restaurant interior from [Unsplash](https://unsplash.com/photos/N_Y88TWmGwA) by Jay Wennington
- **Icons**: [Font Awesome](https://fontawesome.com/) for all icons throughout the site
- **Logo**: Created using text-based styling (no external logo used)


---

**Note**: This project was created for educational purposes as part of the Code Institute Full Stack Developer course. It demonstrates proficiency in Django, Python, HTML, CSS, JavaScript, and database management.

