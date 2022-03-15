# Aggie Job Referral

## How to make the project run locally
0. Install WSL (windows only)
1. Install git, python, and pip
2. git clone https://github.com/aggie-coding-club/aggie-job-referral
3. cd aggie-job-referral
4. git checkout forum
5. pip install -r requirements.txt
6. python manage.py migrate
7. python manage.py runserver
8. Open the url 127.0.0.1:8000 (or any url returned by python prompt)

* You may need to create a .env file in  aggie-job-referral/(or AggieJobReferral/) with content like,

```
SECRET_KEY=AAAABBBBCCCCDDDD12341234=
```
where SECRET_KEY should end with =, and DO NOT share it with anyone.
Try this online key generator [CodeIgniter Encryption Keys](https://randomkeygen.com/#ci_key).

When everthing works, you should be able to see this
![](demo_screenshot.png)


## Todos
- [ ] Build dashboard for company and candidate
- [ ] Email notification
- [ ] Test deploy on heroku


## **Before Deploy on heroku**
- [ ] change LOCAL_RUNNING in AggieJobReferral/settings.py to False