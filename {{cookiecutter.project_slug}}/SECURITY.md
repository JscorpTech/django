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

## Reporting Security Issues / Xavfsizlik muammolarini xabar qilish

If you discover a security vulnerability, please email the maintainers directly instead of using the issue tracker.

Agar xavfsizlik zaifligini topsangiz, iltimos issue tracker o'rniga to'g'ridan-to'g'ri maintainerlar ga email yuboring.
