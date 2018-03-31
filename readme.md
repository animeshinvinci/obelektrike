# Installation
- `git clone ...`  
- `cd blogs`
- `cp main/settings.py.tmp main/settings.py`
- `virtualenv env`
- `source env/bin/activate`
- `(env)> pip install -r requirements.txt`
- `(env)> python manage.py initenv`
- `(env)> python manage.py testdb`


# DevOps structure
## Stack
- uWsgi
- Nginx
- Django

## Deployment code to production
`(env)> fab prod`

## Commands for uwsgi
### Start uwsgi
`(env)> uwsgi --ini devops/wsgi.ini`
### Kill uwsgi processes
`(env)> kill -9 $(ps aux | grep uwsgi |grep -v grep | awk '{print $2}')`
### Reload uwsgi process
`(env)> uwsgi --reload devops\wsgi.pid`


# Usefull links
## Yandex
- [Webmaster Yandex](https://webmaster.yandex.ru/site/service-plugin.xml?host=22600389&service=ORIGINALS&need_auth=false&new_site=false)  
- [Webmaster Yandex](https://webmaster.yandex.ru/site/?host=22600389)  
- [Metrika Yandex](https://metrika.yandex.ru/list/)  

## Google
- [Webmaster Google](https://www.google.com/webmasters/tools/dashboard?hl=ru&siteUrl=http://obelektrike.ru/)
- [Analytics Google](https://www.google.com/analytics/web/)
- [Adsense Google](https://www.google.com/adsense/app?hl=ru#main/home)

## Gogetlinks
- [Gogetlinks](https://gogetlinks.net/my_campaigns.php?faction=change_status)

## 2Domains
- [2Domains](https://reg.2domains.ru/domains/)
