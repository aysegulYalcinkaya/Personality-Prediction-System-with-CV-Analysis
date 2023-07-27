# Personality-Prediction-System-with-CV-Analysis
This project aims to create advanced software that can provide a legally justified and fair CV ranking system
# Prerequisites & Development Libraries
To install app you'll need pip and Git. It also uses a some Python packages (NumPy, SciPy and Matplotlib) but these should be taken care of by the installation process.

| Software | Version |
| ------ | ------ |
| Python 3 | 3.9 |
| Pandas | 0.25.1 |
| Django | 4.2.2 |
| asgiref | 3.7.2 |
| sqlparse | 0.4.4 |
| tzdata | 2023.3 |

## Installation

You can install the app by cloning the repository:

```sh
git clone https://github.com/aysegulYalcinkaya/Personality-Prediction-System-with-CV-Analysis.git
```

## Instructions

* Clone the [repository](#installation)

* Install all required libraries through requirements.txt

```sh
pip install requirements.txt
```

* Run migrations to create sqlite database

```sh
python manage.py makemigrations
python manage.py migrate
```

* Run application server

```sh
python manage.py runserver 8000
```

* In your browser open http://127.0.0.1:8000

## Components of the Application
* Registration (User)
* Login (User and Employer)
* Dashboard (User and Employer)
* Job List (User and Employer)
  ** Create new Job (Employer)
* Personality test (User)
* Job Application and CV Upload (User)
* CV analysis (Employer)
* Display Analysis Results (Employer)

## Screenshots
![](static\screenshots\login.png)

![](C:\Users\Dell\Documents\LECTURENOTES\CAPSTONE\CVAnalysis\static\screenshots\user_joblist.png)

![](C:\Users\Dell\Documents\LECTURENOTES\CAPSTONE\CVAnalysis\static\screenshots\user_jobdetail.png)

![](C:\Users\Dell\Documents\LECTURENOTES\CAPSTONE\CVAnalysis\static\screenshots\cvupload.png)

![](C:\Users\Dell\Documents\LECTURENOTES\CAPSTONE\CVAnalysis\static\screenshots\employer_dashboard.png)

![](C:\Users\Dell\Documents\LECTURENOTES\CAPSTONE\CVAnalysis\static\screenshots\create_job.png)

![](C:\Users\Dell\Documents\LECTURENOTES\CAPSTONE\CVAnalysis\static\screenshots\employer_joblist.png)

![](C:\Users\Dell\Documents\LECTURENOTES\CAPSTONE\CVAnalysis\static\screenshots\employer_editjob.png)
