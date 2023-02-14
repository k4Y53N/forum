### Install

```
git clone https://github.com/k4Y53N/forum.git
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

### Strat Up
```
docker-compose up -d
```
url is [127.0.0.1:8000](127.0.0.1:8000)