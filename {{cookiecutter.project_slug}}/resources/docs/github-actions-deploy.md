{% raw %}
# GitHub Actions Deploy.yaml Tushuntirish

`.github/workflows/deploy.yaml` faylidagi har bir qismning tushuntirishi:

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - main
{% endraw %}
env:
  PROJECT_NAME: {{ cookiecutter.project_slug }}  # O'ZGARTIRING: Loyihangiz nomi
{% raw %}

permissions:
  contents: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

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
          no-cache: true

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

      - name: Update stack.yaml and version
        run: |
          sed -i 's|image: ${{ secrets.DOCKER_USERNAME }}/${{ env.PROJECT_NAME }}:.*|image: ${{ secrets.DOCKER_USERNAME }}/${{ env.PROJECT_NAME }}:${{ github.run_number }}|' stack.yaml
          sed -i 's/return HttpResponse("OK.*"/return HttpResponse("OK: #${{ github.sha }}"/' config/urls.py

      - name: Commit and push updated version
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "🔄 Update image to ${{ github.run_number }} [CI SKIP]" || echo "No changes"
          git pull origin main --rebase
          git push origin main

      - name: Deploy to server via SSH
        uses: appleboy/ssh-action@v1.2.2
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          # key: ${{ secrets.KEY }}
          password: ${{ secrets.PASSWORD }}
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

                for kv in "$@"; do
                    local key="${kv%%=*}"
                    local value="${kv#*=}"
                    sed -i "s|^$key=.*|$key=$value|" "$env_file"
                done
            }

            export PORT=8000
            docker stack deploy -c stack.yaml ${{ env.PROJECT_NAME }}
```

## O'zgartirish Kerak Bo'lgan Joylar

### 1. PROJECT_NAME
```yaml
env:
  PROJECT_NAME: myproject  # Loyihangiz nomi
```

### 2. Branch nomi
```yaml
on:
  push:
    branches:
      - main  # Agar 'master' bo'lsa, o'zgartiring
```

### 3. Database test sozlamalari
```yaml
services:
  postgres:
    env:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: testdb
```

### 4. Django settings module
```yaml
-e DJANGO_SETTINGS_MODULE=config.settings.test  # Loyihangizga mos o'zgartiring
```

### 5. Domain va allowed hosts
```bash
update_env \
  "ALLOWED_HOSTS=127.0.0.1,web,yourdomain.com" \
  "CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8081,https://yourdomain.com" \
```

### 6. Server path
```bash
PROJECTS=/opt/projects/  # Serveringizdagi katalog
DIR=/opt/projects/${{ env.PROJECT_NAME }}/
```

## GitHub Secrets

Repository Settings → Secrets and variables → Actions:

- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub token
- `HOST` - Server IP
- `USERNAME` - SSH user
- `KEY` - SSH private key
- `PORT` - SSH port (22)
{% endraw %}
