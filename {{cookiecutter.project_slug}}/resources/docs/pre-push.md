# jst pre-push o’rnatish

`pre-push vazifasi`: gitga push qilishdan avval testlarni avtomatik bajarib barcha testlardan muvofaqiyatli o’tsa push qiladi

# O’rnatish

`.git/hooks/pre-push` faylini yarating va manabu ko’dlarni fayilga yozing

```bash
#!/bin/bash

echo "🚀 Testlar ishga tushmoqda (Docker konteyner ichida)..."

docker compose run --rm -T web pytest -v

RESULT=$?

if [ $RESULT -ne 0 ]; then
  echo "❌ Testlar muvaffaqiyatsiz tugadi. Push bekor qilindi."
  exit 1
fi

echo "✅ Barcha testlar muvaffaqiyatli o‘tdi. Pushga ruxsat berildi."
exit 0

```

fayilga kerakli permissionlarni bering

```bash
sudo chmod +x .git/hooks/pre-push
```

va hammasi tayyor
