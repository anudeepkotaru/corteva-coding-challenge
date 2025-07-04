# Weather Data API - Coding Challenge

This project ingests, analyzes, and exposes weather data from multiple weather stations across the US Midwest using Django, PostgreSQL, and Django REST Framework.

## Project Structure

```
├── weather_project/           # Django project startup
│   ├── settings.py            # Add apps into INSTALLED_APPS and modify REST_FRAMEWORK
├── weather/                   # App with models, API, and logic
│   ├── models.py              # WeatherRecord and WeatherStat models
│   ├── management/commands/   # ingest_weather_data.py, compute_weather_stats.py
│   ├── views_api.py           # DRF ViewSets
│   ├── serializers_api.py     # DRF Serializers
│   ├── filters.py             # DRF Filters (station_id and date, year)
|   ├── urls.py                # API and Swagger endpoints
│   ├── tests/test_api.py      # Unit tests for ingestion and computing stats
├── manage.py                  # Main entry point to the project
├── weather_ingestion.log      # Log file created during ingestion
├── compute_stats.log          # Log file created during stats computation
├── wx_data/                   # Folder with raw .txt weather files
├── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/anudeepkotaru/corteva-coding-challenge.git
cd corteva-coding-challenge
```

### 2. Set up virtual environment

```bash
python -m venv env
env\Scripts\activate    # on Mac: source env/bin/activate 
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing:

```bash
pip install Django djangorestframework drf-yasg django-filter tqdm psycopg2
```

### 4. Configure database (PostgreSQL)

Update `settings.py` with your PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'weatherdb',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Add weather data files

Place all `.txt` station files inside the root-level folder:

```
wx_data/
├── USC00110072.txt
├── USC00110073.txt
...
```

### 7. Ingest data

```bash
python manage.py ingest_weather
```

### 8. Compute yearly stats

```bash
python manage.py compute_weather_stats
```

### 9. Run the server

```bash
python manage.py runserver
```

## API Endpoints

### Base URL: `http://localhost:8000/api/`

| Endpoint          | Description                    |
| ----------------- | ------------------------------ |
| `/weather/`       | Get daily weather records      |
| `/weather/stats/` | Get yearly station-level stats |

### Filters & Pagination

* `/weather/?station_id=USC00110072&date=1990-05-02`
* `/weather/stats/?station_id=USC00110072&year=1990`

### 📑 Swagger Documentation

* [`/swagger/`](http://localhost:8000/swagger/) – interactive docs

## Running Tests

```bash
python manage.py test weather
```

## Extra Credit (AWS Deployment)

* Use **AWS RDS** for PostgreSQL backend
* Containerize app with **Docker**
* Deploy on **AWS Elastic Beanstalk** or **ECS + Fargate**
* Schedule `ingest_weather` via **AWS Lambda + EventBridge**

---

Created for the Corteva Agriscience Geospatial Data Engineer Coding Challenge.

© 2025 Satya Anudeep Kotaru
