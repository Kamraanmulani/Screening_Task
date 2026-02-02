# Chemical Equipment Visualizer
**IIT Bombay Screening Task**

Full-stack application for uploading, analyzing, and visualizing chemical equipment data with both web and desktop interfaces.

Credentials for Log in : `Username: testuser` / `Password: test123` 

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+

### 1. Backend (Django)
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
**Backend runs on:** `http://localhost:8000`



---

### 2. Web Frontend (React)
```bash
cd frontend-web
npm install
npm run dev
```
**Web app runs on:** `http://localhost:5173`

---

### 3. Desktop App (PyQt5)
```bash
cd frontend-desktop
pip install -r requirements.txt
python main.py
```

---

## 📝 Usage

1. **Login** with your credentials
2. **Upload CSV** with format:
   ```csv
   Equipment Name,Type,Flowrate,Pressure,Temperature
   Pump-1,Pump,120,5.2,110
   ```
3. **View Dashboard** with charts and statistics
4. **Download PDF** reports

---

## 🛠️ Tech Stack

- **Backend:** Django REST Framework, JWT Auth, Pandas, ReportLab
- **Web:** React 19, Vite, Chart.js, Axios
- **Desktop:** PyQt5, Matplotlib

---

## 📂 Structure

```
├── backend/         # Django API
├── frontend-web/    # React app
├── frontend-desktop/ # PyQt5 app
└── sample_equipment_data.csv
```

---

## 🔌 API Endpoints

### Authentication
- `POST /api/token/` - Login (obtain JWT access & refresh tokens)
- `POST /api/token/refresh/` - Refresh JWT token

### Datasets
- `GET /api/datasets/` - List last 5 datasets
- `POST /api/datasets/` - Upload new CSV dataset
- `GET /api/datasets/{id}/summary/` - Get dataset summary statistics
- `GET /api/datasets/{id}/report/` - Download PDF report

### System
- `GET /api/health/` - Health check endpoint

---

## 🐛 Troubleshooting

**Backend not starting?**
```bash
cd backend
venv\Scripts\activate
python manage.py migrate
```

**Frontend errors?**
- Ensure backend is running on port 8000
- Check console for API connection errors

**Desktop app issues?**
```bash
pip install --upgrade PyQt5 matplotlib requests pandas
```

---

Created for IIT Bombay Internship Application
