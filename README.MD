# Start
 - [Get Started](#install)
 - [Custom commands](#commands)
    - [App yaratish](#makeapp)
    - [Seeder](#seeder)
    - [Cacheni tozalash](#clearcache)
    - [Factory](#factory)


## <a name='Get Started'>Install</a>
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

## Install fayli
 - install nomli fayil bu faqatgina linux uchun ishlaydi ishga tushurilganda docker composeni sozlash uchun oyda ochilari

```bash
./install
```

# Docker shellga kirgan holatda migrate qilish
```bash
python3 manage.py migrate
```


## <a name='commands'>Custom commands</a>
# App yaratish
 - default core/apps papkasiga yangi app yaratadi
 ```bash
python3 manage.py makeapp ${name}
 ```

## <a name='seeder'>Seeder</a>
 - Bazaga aniq belgilangan malumotlarni kiritib beradi masalan user 

# Seeder yaratish
```bash
python3 manage.py makeseeder ${name}
```
# Seederlarni ishga tushurish
```bash
python3 manage.py seed
```

# <a name='clearcache'>Cachelarni tozalash</a>
```bash
python3 manage.py clearcache
```

## <a name='factory'>Factory</a>
 - Bazani soxta malumotlar bilan to'ldirib beradi

# Factory yaratish
```bash
pyhon3 manage.py makefactoy ${name}
```

# Factorylarni ishga tushurish
```bash
python3 manage.py factory
```