# Start
 - [Get Started](#install)
 - [Custom commands](#commands)
    - [App yaratish](#makeapp)
    - [Seeder](#seeder)
    - [Cacheni tozalash](#clearcache)
    - [Factory](#factory)
    - [Generate Secret key](#secret)
    - [Folders](#folders)


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



# <a name='secret'>Generate Secret key</a>
```bash
python3 manage.py secret
```

# <a name='folders'>Folders</a>
 - common
 - * env.py `Enviromendagi malumotlar uchun`
 - config
   - conf
     - `Tashqi kutubxonalar sozlamalari uchun papka`
   - settings
      - production.py `Productionda ishlashi kerak bo'lgan settings fayli`
      - local.py `Localda ishlashi kerak bo'lgan settings fayli`
      - common.py `Umumiy sozlamalar`
 - core
   - apps`Shaxsiy applar`
   - console `Consolni app`
   - enums `Enums uchun papaka yani Choices model uchun`
   - exceptions
   - http `Base app barcha kerakli default functiyalar`
   - middlewares
   - services
   - utils
 - deployments `Deploy uchun example`
 - docs `Documentatsiya fayillarini saqlash uchun papka`
 - locale
 - logs `Project loglari uchun papka`
 - media `Media fayillar uchun papka`
 - nginx `Docker + nginx uchun kerakli fayillar`
 - requirements `Project requirements papkasi`
 - resources `Frontend ko'dlari uchun papka css,js,html`
 - routes `asosiy routing fayillari`
 - scripts `Kerakli scriptlar`
 - stubs `Factory va seeder uchun stub fayil yani shablon fayil`
 - tests
 - * .env
 - * .env.example
 - * .gitignore
 - * .gitlab-cli.yml `Gitlab uchun ci/cd`
 - * docker-compose.yml
 - * Dockerfile
 - * generate_secret.py `Django secret key generatsiya qilish`
 - * install
 - * Makefile
 - * manage.py
 - * packages.jscon
 - * pyproject.toml
 - * pytest.ini
 - * tailwind.config.js
 - * vite.config.js
 - * ViteDockerfile

