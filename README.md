### Install

```
git clone https://github.com/k4Y53N/forum.git
cd forum
```

### dev version
```
git clone https://github.com/k4Y53N/forum.git --branch dev
cd forum
```

### Setup
```
mkdir mount/db
mkdir mount/backend
echo "<your database name>" > secrets/db_name.txt
echo "<your database password>" > secrets/db_password.txt
echo "<your database username>" > secrets/db_username.txt
echo "<your django secret key>" > secrets/secret_key.txt
```

### Setup (dev version (windows))
```
python -m venv .venv
.venv/scripts/activate
pip install -r requirements.txt
```

### Strat Up
```
docker-compose up -d
```

### Start Up (dev version (windows))
```
# start your venv first
cd backend
python manage.py makemigtaions
python manage.py migrate --run-sync
python manage.py runserver
```
url is [127.0.0.1:8000](127.0.0.1:8000)


### ref
[https://github.com/nauvalazhar/bootstrap-4-login-page](https://github.com/nauvalazhar/bootstrap-4-login-page)  
[https://github.com/StartBootstrap/startbootstrap-clean-blog](https://github.com/StartBootstrap/startbootstrap-clean-blog)


### swagger api
[127.0.0.1:8000/swagger/](127.0.0.1:8000/swagger/)