# AGENTS.md

Bu hujjat JST Django template asosida yaratilgan loyihalarda ishlaydigan AI agentlar va contributorlar uchun umumiy contract. Maqsad: domain-neutral, xavfsiz, testlanadigan va maintain qilish oson backend kod yozish.

Har bir loyiha o'z domen app'lari va optional integratsiyalariga ega bo'lishi mumkin. Avval mavjud repo strukturasi, app patternlari, `README.MD`, `Makefile`, `pyproject.toml`, settings va testlarni o'rganing; keyin shu kontekstga mos, kichik va review qilish oson o'zgarish qiling.

## Architecture Boundaries

Yangi kod mavjud app ichidagi qatlamlarga mos joylashishi kerak:

- `models/` - database schema, modelga yaqin invariantlar, `__str__`, constraints va indexes.
- `serializers/` - request/response shape, input validation va object mapping.
- `views/` - DRF routing, permissions, queryset scope, serializer tanlash va schema metadata.
- `services/` - business logic, state transition, hisob-kitob, integration orchestration.
- `tasks/` - async yoki retry qilinadigan ishlar.
- `signals/` - faqat kichik model lifecycle hooklar.
- `permissions/`, `filters/`, `validators/` - reusable API boundary logic.
- `tests/` - real behavior, permission, ownership va failure path testlari.

View ichida katta business logic qoldirmang. Serializer ichida uzoq ishlaydigan side-effect boshlamang. Integration chaqiriqlari service yoki task orqali o'tishi kerak.

## Service Layer Rules

Service layer explicit domain operationlarni ushlab turadi. Yangi service yozilganda:

- Input va output contract aniq bo'lsin.
- Bir nechta DB o'zgarishi bitta operation bo'lsa `transaction.atomic()` ishlatilsin.
- State transitionlar idempotency, rollback va double-submit xavfini hisobga olsin.
- External calllar timeout, retry/failure strategy va structured logging bilan o'ralsin.
- Sensitive qiymatlar logga yozilmasin.
- Service testlari view yoki serializerdan mustaqil tekshirilsin.

Service class yoki function tanlashda repo ichidagi mavjud stylega ergashing. Faqat real murakkablikni kamaytirsa abstraction qo'shing.

## Signal Rules

Signal faqat sodda, tez va deterministic hook bo'lishi kerak. Quyidagilar signal ichida bajarilmasin:

- Payment, deploy, webhook, bot/SMS/email yoki storage kabi external side-effect.
- Uzoq ishlaydigan yoki retry talab qiladigan ish.
- Katta orchestration, multi-step state transition yoki user-visible workflow.
- Recursion xavfi bor `save()` chainlari.

Signal kerak bo'lsa, recursion va duplicate side-effectdan himoya qiling. Og'ir ishni explicit service yoki taskga chiqarib, testda signal importlari app startupda ishlashini tekshiring.

## API and Serializer Rules

- Endpoint ownership/user/project/tenant scope bilan cheklansin.
- Public, authenticated va admin/internal endpoint permissions aniq ajratilsin.
- `get_queryset()` user-scoped resource uchun hech qachon global queryset qaytarmasin.
- Router basename, URL name va response wrapper mavjud contractni sababsiz buzmasin.
- drf-spectacular ishlatilsa, yangi endpoint uchun request/response va muhim error response schema yangilansin.
- Serializer validation DRF `ValidationError` bilan qaytsin; external side-effect serializerdan tashqarida bajarilsin.

## Optional Integration Boundaries

Optional paket yoki integration faqat loyiha tanlagan bo'lsa aktiv contractga kiradi:

- Payment-like flow: signature/callback verification, idempotency key, double-submit protection, DB transaction, audit trail va failure testlari bo'lishi shart.
- Bot/SMS/Email: tokenlar env/secret orqali olinadi, rate limit va retry strategy aniq bo'ladi, provider response loglari sensitive data chiqarmaydi.
- Webhook: authentication yoki signature verification, replay protection, payload schema validation va safe error response kerak.
- Storage/File: file type, size, path traversal, ownership va lifecycle cleanup tekshirilsin.
- WebSocket/SSE: auth middleware, user scope, event schema va disconnect behavior aniq bo'lsin.
- Infra deploy/Kubernetes/Docker: namespace/env/secret ajratilsin, cleanup idempotent bo'lsin, production secret repo ichiga kirmasin.
- NoSQL/search/cache: query sanitization, tenant/user scope va stale data invalidation contracti yozilsin.

## Testing Quality Bar

Yangi behavior uchun testlar kamida quyidagilarni qamrasin:

- Happy path real DB/API behavior bilan.
- Validation yoki invalid input failure path.
- Permission/authentication va ownership isolation.
- Muhim state transitionlarda double-submit, rollback yoki expired/invalid token/code holati.
- External side-effectlar mock qilinib, muhim argumentlar tekshirilsin.

`assert True`, bo'sh `pass`, kommentga olingan test yoki faqat status code bilan cheklangan yuzaki test finished code emas. Endpoint nomlari uchun `reverse()` ishlating.

## Security Checklist

- `.env`, private key, token, password, production dump yoki real credential commit qilinmasin.
- `DEBUG=False`, `ALLOWED_HOSTS`, HTTPS/secure cookie settings productionda tekshirilsin.
- Admin/debug/schema/profiling/metrics route'lari productionda ochiq qolmasin.
- Webhook va callback endpointlar auth/signature bilan himoyalansin.
- User inputdan kelgan path, URL, query, filter, callback va token validatsiyasiz ishlatilmasin.
- Sensitive qiymatlar logging, exception detail yoki API responsega chiqmasin.
- Public key ham faqat aniq xavfsizlik modeli bo'lsa repo ichida saqlansin.

## Small Project Mode

Kichik loyihalarda ham qatlamlar saqlanadi, lekin optional featurelar majburan yoqilmaydi:

- Celery/task faqat async/retry zarur bo'lsa ishlatiladi.
- Channels/WebSocket, cacheops, storage, rich editor, bot yoki payment code tanlanmagan loyihaga qo'shilmaydi.
- Service layer kichik function bo'lishi mumkin; lekin business logic view ichida semirib ketmasin.
- Global dependency qo'shishdan oldin feature optionalmi yoki core requirementmi aniqlansin.

## Before Handoff

Har bir o'zgarishdan keyin kamida eng kichik zarur check ishlating:

```bash
make check
```

Agar Docker ishlamayotgan bo'lsa, lokal muqobil commandlarni ishga tushiring:

```bash
python -m pytest -q
python -m flake8 .
python -m pyright
```

Natijada qaysi fayllar o'zgargani, nima uchun o'zgargani va qaysi checklar ishlaganini qisqa yozing.
