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

# Seederlarni ishga tushurish
```bash
python3 manage.py seed
```