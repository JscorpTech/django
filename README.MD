# Start Project example


# .env faylidan nuxsa olish
```bash
cp .env.example .env
```

# docker image build qilish
```bash
docker compose up -d --build
```

# Docker bashga kirish
```bash
docker compose exec web bash
```

# Docker shellga kirgan holatda migrate qilish
```bash
python3 manage.py migrate
```
# App yaratish
 - default core/apps papkasiga yangi app yaratadi
 ```bash
python3 manage.py makeapp ${name}
 ```

## Seeder
 - Bazaga aniq belgilangan malumotlarni kiritib beradi masalan user 

# Seeder yaratish
```bash
python3 manage.py makeseeder ${name}
```
# Seederlarni ishga tushurish
```bash
python3 manage.py seed
```

# Cachelarni tozalash
```bash
python3 manage.py clearcache
```

## Factory
 - Bazani soxta malumotlar bilan to'ldirib beradi

# Factory yaratish
```bash
pyhon3 manage.py makefactoy ${name}
```

# Factorylarni ishga tushurish
```bash
python3 manage.py factory
```