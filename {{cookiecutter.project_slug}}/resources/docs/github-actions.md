{% raw %}# GitHub Actions CI/CD sozlash

Bu dokumentatsiya loyihangizga GitHub Actions orqali avtomatik test va deploy qo'shishni tushuntiradi.

## Kerakli o'zgartirishlar

### 1. **Loyiha nomi (PROJECT_NAME)**
```yaml
env:
  PROJECT_NAME: service  # 👈 Bu yerda loyihangiz nomini kiriting
```
**Misol:** Agar loyihangiz `myshop` bo'lsa, `PROJECT_NAME: myshop` deb yozing.

### 2. **Docker fayl yo'li**
```yaml
- name: Build Docker image
  uses: docker/build-push-action@v5
  with:
    file: ./docker/Dockerfile.web  # 👈 Dockerfile yo'lingizni tekshiring
```
**Misol:** Agar Dockerfile asosiy papkada bo'lsa: `file: ./Dockerfile`

### 3. **Environment o'zgaruvchilari**
```yaml
- name: Run migrations and tests
  run: |
    docker run --rm \
      -e DB_HOST=localhost \
      -e DB_PORT=5432 \
      -e DB_NAME=testdb          # 👈 Test DB nomi
      -e DB_USER=postgres         # 👈 DB username
      -e REDIS_URL=redis://localhost:6379  # 👈 Redis URL (agar kerak bo'lsa)
      -e DJANGO_SETTINGS_MODULE=config.settings.test  # 👈 Settings fayl yo'li
```
**O'zgartirish:** Loyihangizda qanday env kerak bo'lsa shularni qo'shing.

### 4. **Test komandasi**
```yaml
sh -c "python manage.py migrate && pytest -v"  # 👈 Test komandangizni yozing
```
**Variantlar:**
- `python manage.py test` - Django default test
- `pytest tests/` - Pytest ma'lum papka
- `pytest --cov=.` - Coverage bilan

### 5. **GitHub Secrets qo'shish**
Repository Settings → Secrets → Actions → New repository secret:

- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password/token
- `HOST` - Server IP manzili
- `USERNAME` - Server SSH username (masalan: root, ubuntu)
- `KEY` - SSH private key matni
- `PORT` - SSH port (odatda 22)

### 6. **Deploy konfiguratsiyasi**
```yaml
- name: stack.yaml updated
  run: |
    sed -i 's|image: ${{ secrets.DOCKER_USERNAME }}/${{ env.PROJECT_NAME }}:.*|...'
    sed -i 's/return HttpResponse("OK.*"/...' config/urls.py  # 👈 Fayl yo'lini o'zgartiring
```
**O'zgartirish:** Health check endpointingiz turli joyda bo'lsa, fayl yo'lini o'zgartiring.

### 7. **Server deploy sozlamalari**
```bash
update_env \
  "CACHE_ENABLED=True" \
  "ALLOWED_HOSTS=127.0.0.1,web,botlarnionasi.jscorp.uz" \     # 👈 Domeningizni yozing
  "CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8081,https://..." \  # 👈 URL lar
  "API_URL=https://botlarnionasi.jscorp.uz"                   # 👈 API URL
```
**O'zgartirish:** Production environment o'zgaruvchilaringizni kiriting.

### 8. **Docker stack nomi**
```bash
docker stack deploy -c stack.yaml ${{ env.PROJECT_NAME }}  # 👈 Stack nomi
```
Stack nomi `PROJECT_NAME` bilan bir xil bo'ladi.{% endraw %}

{% raw %}
---

## CI/CD jarayoni vizualizatsiyasi{% endraw %}

{% raw %}```
┌─────────────────────────────────────────────────────────────┐
│  1. TRIGGER: main branchga push/merge qilinadi              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  2. CHECKOUT: Kod yuklanadi                                 │
│     • actions/checkout@v4                                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  3. SERVICES ISHGA TUSHADI                                  │
│     ┌──────────────┐           ┌──────────────┐            │
│     │  PostgreSQL  │           │    Redis     │            │
│     │  Port: 5432  │           │  Port: 6379  │            │
│     └──────────────┘           └──────────────┘            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  4. DOCKER IMAGE BUILD                                      │
│     • .env.example → .env nusxalash                         │
│     • Docker image yaratish                                 │
│     • Tag: PROJECT_NAME:test                                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  5. TEST RUNNING                                            │
│     • Migration qilish (migrate)                            │
│     • Testlarni ishga tushirish (pytest)                    │
│     ❌ Xato bo'lsa → JARAYON TO'XTAYDI                      │
│     ✅ Muvaffaqiyatli → Davom etadi                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  6. DOCKER HUB GA PUSH                                      │
│     • Login (DOCKER_USERNAME, DOCKER_PASSWORD)              │
│     • Tag: username/PROJECT_NAME:latest                     │
│     • Tag: username/PROJECT_NAME:123 (run number)           │
│     • Docker Hub ga push                                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  7. FAYLLARNI YANGILASH                                     │
│     • stack.yaml → yangi image version                      │
│     • config/urls.py → yangi commit hash                    │
│     • Git commit va push                                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  8. SERVERGA DEPLOY (SSH orqali)                            │
│     ┌────────────────────────────────────────────────────┐ │
│     │ • Loyiha papkasini tekshirish/yaratish             │ │
│     │ • Git clone/pull (yangi kod olish)                 │ │
│     │ • .env faylni yangilash                            │ │
│     │ • docker stack deploy ishga tushirish              │ │
│     └────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│  ✅ DEPLOY TUGADI                                           │
│     Yangi versiya serverda ishlamoqda                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

1. `.github/workflows/ci.yml` faylini yarating va workflow kodini joylashtiring
2. `PROJECT_NAME` ni o'zgartiring
3. GitHub Secrets qo'shing (Settings → Secrets → Actions)
4. `main` branchga push qiling
5. Actions tabda jarayonni kuzating

---

## Muhim eslatmalar

- **Commit message `[CI SKIP]`** bo'lsa, workflow ishlamaydi
- **Test fail bo'lsa** deploy qilinmaydi
- **Docker Hub credentials** xato bo'lsa, push bo'lmaydi  
- **SSH key** formatini to'g'ri kiriting (private key matni)
- **Server** `/opt/projects/` papkasi bo'lishi kerak yoki avtomatik yaratiladi

---

## Troubleshooting

### Test fail bo'lsa
```bash
# Lokal testlarni tekshiring
docker-compose run --rm web pytest -v
```

### SSH ulanmasa
```bash
# SSH key formatini tekshiring
cat ~/.ssh/id_rsa  # Private key shu formatda bo'lishi kerak
```

### Docker push fail bo'lsa
```bash
# Docker Hub credentials tekshiring
docker login -u YOUR_USERNAME
```


## Misol

```yaml
name: Build and Push to Docker Hub

on:
  push:
    branches:
      - main

env:
  PROJECT_NAME: project_name

permissions:
  contents: write

jobs:
  build-test-push:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Copy env
        run: |
          cp .env.example .env

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./docker/Dockerfile.web
          push: false
          load: true
          tags: ${{ env.PROJECT_NAME }}:test

      - name: Run migrations and tests
        run: |
          docker run --rm \
            --network host \
            -e DB_HOST=localhost \
            -e DB_PORT=5432 \
            -e DB_NAME=testdb \
            -e DB_USER=postgres \
            -e REDIS_URL=redis://localhost:6379 \
            -e DB_PASSWORD=postgres \
            -e DJANGO_SETTINGS_MODULE=config.settings.test \
            ${{ env.PROJECT_NAME }}:test \
            sh -c "python manage.py migrate && pytest -v"

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Tag and push to Docker Hub
        run: |
          docker tag ${{ env.PROJECT_NAME }}:test ${{ secrets.DOCKER_USERNAME }}/${{ env.PROJECT_NAME }}:latest
          docker tag ${{ env.PROJECT_NAME }}:test ${{ secrets.DOCKER_USERNAME }}/${{ env.PROJECT_NAME }}:${{ github.run_number }}
          docker push ${{ secrets.DOCKER_USERNAME }}/${{ env.PROJECT_NAME }}:latest
          docker push ${{ secrets.DOCKER_USERNAME }}/${{ env.PROJECT_NAME }}:${{ github.run_number }}
          echo "SUCCESS TAGS: latest, ${{ github.run_number }}"

      - name: stack.yaml updated
        run: |
          sed -i 's|image: ${{ secrets.DOCKER_USERNAME }}/${{ env.PROJECT_NAME }}:.*|image: ${{ secrets.DOCKER_USERNAME }}/${{ env.PROJECT_NAME }}:${{ github.run_number }}|' stack.yaml
          sed -i 's/return HttpResponse("OK.*"/return HttpResponse("OK: #${{ github.sha }}"/' config/urls.py

      - name: Commit and push updated version
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "🔄 image to ${{ github.run_number }} [CI SKIP]" || echo "No changes"
          git pull origin main --rebase
          git push origin main

      - name: Execute remote SSH commands using SSH key
        uses: appleboy/ssh-action@v1.2.2
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.KEY }}
          port: ${{ secrets.PORT }}
          script: |
            PROJECTS=/opt/projects/
            DIR=/opt/projects/${{ env.PROJECT_NAME }}/
            
            if [ -d "$PROJECTS" ]; then
              echo "projects papkasi mavjud"
            else
              mkdir -p $PROJECTS
              echo "projects papkasi yaratildi"
            fi

            if [ -d "$DIR" ]; then
              echo "loyiha mavjud"
            else
              cd $PROJECTS
              git clone git@github.com:${{ github.repository }}.git ${{ env.PROJECT_NAME }}
              echo "Clone qilindi";
            fi

            cd $DIR
            git fetch origin main
            git reset --hard origin/main
            cp .env.example .env

            update_env() {
                local env_file=".env"
                cp .env.example "$env_file"

                # argumentlar orqali key=value olish
                for kv in "$@"; do
                    local key="${kv%%=*}"
                    local value="${kv#*=}"
                    sed -i "s|^$key=.*|$key=$value|" "$env_file"
                done
            }

            # Funksiyani chaqirish misoli
            update_env \
              "MONGO_URL=${{ secrets.MONGO_URL }}" \
              "DB_ENGINE=django_prometheus.db.backends.postgresql" \
              "CACHE_ENABLED=True" \
              "ALLOWED_HOSTS=127.0.0.1,web,botlarnionasi.jscorp.uz" \
              "CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8081,https://botlarnionasi.jscorp.uz" \
              "BOT_TOKEN=${{ secrets.BOT_TOKEN }}" \
              "API_URL=https://botlarnionasi.jscorp.uz" \

            docker stack deploy -c stack.yaml ${{ env.PROJECT_NAME }} 
```{% endraw %}
