# {{ cookiecutter.project_slug }} - Django Loyihasi

Django asosidagi web ilovasi. Ushbu loyiha Docker konteynerlarida ishga tushiriladi va rivojlantiriladi.

[Hujjatlar](https://docs.jscorp.uz)

## Talablar

- Docker va Docker Compose o'rnatilgan bo'lishi kerak
- Make utility (Linux/macOS da standart o'rnatilgan)

## Loyihani Ishga Tushirish

### Asosiy Commandalar

#### `make start`
Loyihani birinchi marta ishga tushirish uchun. Docker konteynerlarni ishga tushiradi va ma'lumotlar bazasini boshlang'ich ma'lumotlar bilan to'ldiradi.
```bash
make start
```

#### `make up`
Docker konteynerlarni ishga tushirish (fonda).
```bash
make up
```

#### `make down`
Ishlab turgan Docker konteynerlarni to'xtatish.
```bash
make down
```

#### `make build`
Docker imagelarni qayta build qilish.
```bash
make build
```

#### `make rebuild`
Konteynerlarni to'xtatib, qayta build qilib, ishga tushirish.
```bash
make rebuild
```

#### `make logs`
Konteynerlar loglarini real-time ko'rish.
```bash
make logs
```

## Ma'lumotlar Bazasi Boshqaruvi

#### `make makemigration`
Django migratsiya fayllarini yaratish.
```bash
make makemigration
```

#### `make migrate`
Migratsiyalarni ma'lumotlar bazasiga qo'llash.
```bash
make migrate
```

#### `make makemigrate`
Migratsiya yaratish va qo'llash (bitta commandada).
```bash
make makemigrate
```

#### `make seed`
Ma'lumotlar bazasini boshlang'ich ma'lumotlar bilan to'ldirish.
```bash
make seed
```

#### `make reset_db`
Ma'lumotlar bazasini tozalash (barcha ma'lumotlarni o'chirish).
```bash
make reset_db
```

#### `make fresh`
Ma'lumotlar bazasini tozalab, migratsiyalarni qayta qo'llab, boshlang'ich ma'lumotlar bilan to'ldirish.
```bash
make fresh
```

## Deploy (Joylashtirish)

#### `make deploy`
Development muhitiga deploy qilish (konteynerlarni to'xtatish, build qilish, ishga tushirish va migratsiya qilish).
```bash
make deploy
```

#### `make deploy-prod`
Production muhitiga deploy qilish (production docker-compose faylidan foydalanib).
```bash
make deploy-prod
```

## Test

#### `make test`
Testlarni ishga tushirish (pytest yordamida).
```bash
make test
```

## Ish Jarayoni Misollari

### Loyihani birinchi marta ishga tushirish:
```bash
make start
```

### Kod o'zgarishlaridan keyin qayta ishga tushirish:
```bash
make rebuild
```

### Model o'zgarishlaridan keyin:
```bash
make makemigrate
```

### Ma'lumotlar bazasini qaytadan boshlash:
```bash
make fresh
```

### Ishlab turgan ilovaning loglarini ko'rish:
```bash
make logs
```

## Muammolarni Hal Qilish

Agar loyiha to'g'ri ishlamasa:
1. Konteynerlarni to'xtatib qayta ishga tushiring: `make rebuild`
2. Ma'lumotlar bazasini qaytadan yarating: `make fresh`
3. Loglarni tekshiring: `make logs`

## Qo'shimcha Ma'lumot

Batafsil ma'lumot uchun [hujjatlar](https://docs.jscorp.uz) sahifasiga tashrif buyuring.
