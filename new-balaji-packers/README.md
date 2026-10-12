# New Balaji Packers and Movers - Complete Django Web Application

A full-featured, production-ready Django web application for **New Balaji Packers and Movers**, featuring Django MVT architecture, Bootstrap 5 responsive UI matching the Navy Blue & Amber theme, interactive JavaScript features, ModelForm with custom item input and CSRF protection, SQLite/PostgreSQL database models, and deployment configuration for **Render**.

---

## 🏢 Business & Branch Details

- **Business Name:** New Balaji Packers and Movers
- **Proprietor:** Mr. Kumar
- **Official Tagline:** *Safe Move ... Happy Home | Your Trust, Our Responsibility*
- **Official Contact Numbers:** `9014331173`, `9803558899`, `8099333910`
- **Head Office / Main Branch:**
  - **Location:** Vuyyuru
  - **Address:** Thotlavallaru Road, Sai Baba Temple Back Side, Vuyyuru
  - **Phone:** `9014331173`
- **Other Branches:**
  - **Vijayawada:** Opp. Nagarjuna Hospital, Kanuru, Auto Nagar, Vijayawada | Phone: `9803558899`
  - **Machilipatnam:** Housing Board Colony, Bypass Road, Machilipatnam | Phone: `8099333910`

---

## 🛠️ Key Features & Architecture

### 1. Django MVT Architecture & 3 Database Models
- **`Branch`**: Stores official centers with Vuyyuru marked as Head Office / Main Branch (`is_head_office=True`), along with Vijayawada and Machilipatnam branch details, addresses, and phone numbers.
- **`BookingOrder`**: Stores customer shifting booking requests, pickup/drop locations, moving dates, standard item categories, manual custom typed items, calculated price estimates, notes, and fulfillment statuses (`PENDING`, `CONFIRMED`, `IN_TRANSIT`, `COMPLETED`, `CANCELLED`).
- **`CustomerReview`**: Stores customer reviews, city routes, verified approval statuses, and ratings (1 to 5 stars).

### 2. Django ModelForm with CSRF Protection
- **`BookingOrderForm`**:
  - Handles full customer details, phone validation (min 10 digits).
  - Integrates standard item checkboxes and a dedicated manual custom items field (*"Any specific items? Type manually..."*).
  - Pre-populates estimated fare from the price calculator.
  - Full CSRF token protection.
- **`CustomerReviewForm`**:
  - Validates and saves customer reviews tied dynamically to the live star rating selector.

### 3. Bootstrap 5 Responsive UI & Navy Blue / Amber Theme
- Clean Navy Blue (`#070d19` / `#0f172a` / `#1e293b`) and Amber/Gold (`#f59e0b` / `#fbbf24`) color palette.
- Modern typography with Google Fonts (*Outfit* and *Plus Jakarta Sans*).
- Responsive header navigation, branch cards, mobile menu, floating WhatsApp action button, and footer.

### 4. 2 Interactive JavaScript Features
1. **Interactive Moving Price Calculator (`static/js/main.js`)**:
   - Computes instant estimated shifting fare based on Pickup City, Drop City, Move Size (1 BHK, 2 BHK, 3+ BHK, Office, Car Transport, Single Item), Packing Tier (Standard vs. 5-Layer Bubble), and Floor/Lift accessibility.
   - Provides instant live breakdown (Freight, Packing, Labor) and a **"Book Shifting With This Estimate"** button that pre-populates the order booking form.
2. **Live Review Star Rating Selector**:
   - Interactive 5-star selector where hover and click dynamically illuminate stars in golden amber, update a hidden input, and change descriptive labels (*"5 Stars - Excellent & Highly Recommended!"*).

### 5. Pre-populated Initial Branch Records & Superuser
- Management command `setup_initial_data`:
  - Automatically seeds Vuyyuru (Head Office), Vijayawada, and Machilipatnam branches.
  - Seeds verified customer reviews.
  - Creates the default superuser (`admin` / `admin123`).

### 6. Render Production Deployment Ready
- `requirements.txt`: Django, Gunicorn, WhiteNoise, sqlparse, asgiref, tzdata.
- `render.yaml`: Render Blueprint service configuration.
- `build.sh`: Shell script running `pip install`, `collectstatic`, `migrate`, `setup_initial_data`, and `create_superuser.py`.
- `create_superuser.py`: Script to ensure superuser is generated from environment variables.
- `balaji_packers/settings.py`: Configured with WhiteNoise static compression, CSRF trusted origins, environment variables, and security settings.

---

## 🚀 Getting Started Locally

### 1. Activate Virtual Environment
On Windows PowerShell:
```powershell
..\venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run Migrations & Pre-populate Data
```powershell
python manage.py migrate
python manage.py setup_initial_data
```

### 4. Start the Django Development Server
```powershell
python manage.py runserver
```
Visit:
- Website: `http://127.0.0.1:8000/`
- Order Booking Form: `http://127.0.0.1:8000/quote/`
- Admin Portal: `http://127.0.0.1:8000/admin/`
  - **Username:** `admin`
  - **Password:** `admin123`

---

## 🧪 Running Unit Tests

Run Django's test suite:
```powershell
python manage.py test
```

---

## 🌐 Deploying to Render

1. Push this repository to GitHub or GitLab.
2. In [Render Dashboard](https://dashboard.render.com/):
   - Choose **New > Blueprint** and select this repository (or create a **Web Service** using `render.yaml`).
   - Build Command: `./build.sh`
   - Start Command: `gunicorn balaji_packers.wsgi:application`
3. Environment variables (optional overrides):
   - `SECRET_KEY`: Set your production secret key
   - `DEBUG`: `False`
   - `DJANGO_SUPERUSER_USERNAME`: `admin`
   - `DJANGO_SUPERUSER_PASSWORD`: `<your-secure-password>`
   - `DJANGO_SUPERUSER_EMAIL`: `<your-email>`
