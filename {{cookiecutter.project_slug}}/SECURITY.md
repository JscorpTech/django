# Security Best Practices / Xavfsizlik bo'yicha eng yaxshi amaliyotlar

## English

### Important Security Notes

1. **Change Default Credentials**
   - Never use the default password `2309` in production
   - Change the admin phone number from the default value
   - Generate a strong SECRET_KEY for production

2. **Environment Variables**
   - Never commit `.env` file to version control
   - Keep production credentials secure and separate from development
   - Use strong passwords for database and admin accounts

3. **Database Security**
   - Change default database password in production
   - Use strong passwords for PostgreSQL
   - Restrict database access to specific IP addresses

4. **Django Security Settings**
   - Set `DEBUG=False` in production
   - Configure proper `ALLOWED_HOSTS`
   - Use HTTPS in production (`PROTOCOL_HTTPS=True`)
   - Keep `SECRET_KEY` secret and unique per environment

5. **API Security**
   - Configure proper CORS settings
   - Use CSRF protection
   - Implement rate limiting
   - Use JWT tokens with appropriate expiration times

6. **Docker Security**
   - Don't expose unnecessary ports
   - Use docker secrets for sensitive data
   - Keep Docker images updated

7. **Endpoint and Integration Boundaries**
   - Keep admin, debug, schema, metrics, and profiling routes unavailable to public production traffic unless explicitly protected
   - Verify webhook/callback authenticity with a signature, shared secret, or provider token
   - Use idempotency for payment-like, webhook, deploy, and external side-effect flows
   - Validate user-provided paths, URLs, filters, callbacks, and file metadata before use
   - Never log authorization headers, tokens, passwords, private keys, reset codes, or provider credentials

8. **Repository Hygiene**
   - Do not commit `.env.*` files, private keys, database dumps, local media, logs, caches, or generated runtime artifacts
   - Keep `.env.example` safe: sample values only, no real credentials
   - Use `.pre-commit-config.yaml` and `make check` before opening a pull request

## O'zbekcha

### Muhim xavfsizlik eslatmalari

1. **Standart parollarni o'zgartiring**
   - Production muhitida hech qachon standart parol `2309` dan foydalanmang
   - Admin telefon raqamini standart qiymatdan o'zgartiring
   - Production uchun kuchli SECRET_KEY yarating

2. **Environment o'zgaruvchilari**
   - Hech qachon `.env` faylini git repozitoriyasiga commit qilmang
   - Production ma'lumotlarini xavfsiz va developmentdan alohida saqlang
   - Ma'lumotlar bazasi va admin akkountlari uchun kuchli parollar ishlating

3. **Ma'lumotlar bazasi xavfsizligi**
   - Production muhitida standart parolni o'zgartiring
   - PostgreSQL uchun kuchli parollar ishlating
   - Ma'lumotlar bazasiga kirishni muayyan IP manzillarga cheklang

4. **Django xavfsizlik sozlamalari**
   - Production muhitida `DEBUG=False` qiling
   - To'g'ri `ALLOWED_HOSTS` sozlang
   - Production muhitida HTTPS dan foydalaning (`PROTOCOL_HTTPS=True`)
   - `SECRET_KEY` ni maxfiy va har bir muhitda noyob qiling

5. **API xavfsizligi**
   - To'g'ri CORS sozlamalarini o'rnating
   - CSRF himoyasidan foydalaning
   - Rate limiting ni amalga oshiring
   - JWT tokenlarni to'g'ri muddatda ishlating

6. **Docker xavfsizligi**
   - Keraksiz portlarni ochib qo'ymang
   - Maxfiy ma'lumotlar uchun docker secrets dan foydalaning
   - Docker imagelarni yangilab turing

7. **Endpoint va integratsiya chegaralari**
   - Admin, debug, schema, metrics va profiling routelar productionda public ochiq qolmasin, kerak bo'lsa qat'iy himoyalansin
   - Webhook/callback haqiqiyligini signature, shared secret yoki provider token orqali tekshiring
   - Payment-like, webhook, deploy va external side-effect flowlarida idempotency ishlating
   - User kiritgan path, URL, filter, callback va file metadatalarini validatsiyasiz ishlatmang
   - Authorization header, token, password, private key, reset code yoki provider credential logga yozilmasin

8. **Repo gigiyenasi**
   - `.env.*`, private key, database dump, local media, log, cache va runtime artifactlarni commit qilmang
   - `.env.example` faqat xavfsiz sample qiymatlarni saqlasin, real credential bo'lmasin
   - Pull requestdan oldin `.pre-commit-config.yaml` va `make check` ishlating

## Reporting Security Issues / Xavfsizlik muammolarini xabar qilish

If you discover a security vulnerability, please email the maintainers directly instead of using the issue tracker.

Agar xavfsizlik zaifligini topsangiz, iltimos issue tracker o'rniga to'g'ridan-to'g'ri maintainerlar ga email yuboring.
