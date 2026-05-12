# AGENTS.md

Bu hujjat JST Django template asosida yaratilgan loyihalarda ishlaydigan AI agentlar uchun umumiy qo'llanma. Maqsad: template arxitekturasiga mos, xavfsiz, testlanadigan va uzoq muddat maintain qilish oson bo'lgan kod yozish.

Template turli loyihalarda har xil app va integratsiyalar bilan ishlatiladi. Shuning uchun bu qo'llanma aniq bir loyiha domeniga bog'lanmaydi. Har doim avval mavjud repo strukturasi va ishlatilayotgan app/integratsiyalarni o'rgan, keyin shu kontekstga mos harakat qil.

## Project Overview

JST Django template odatda Django/DRF backend uchun tayyor foundation beradi:

- `config/` - Django settings, urls, ASGI/WSGI, Celery entrypoint va env konfiguratsiya.
- `config/conf/` - kutubxonalar va feature configlari: apps, cache, celery, jwt, storage, logs, rest framework, spectacular, admin UI va boshqalar.
- `config/settings/` - `common.py`, `local.py`, `production.py`, `test.py`.
- `core/apps/` - loyiha app'lari. Har bir loyiha o'z domeniga qarab turli app'larga ega bo'lishi mumkin.
- `core/services/` - umumiy service/helperlar.
- `core/utils/` - reusable util funksiyalar.
- `resources/` - templates, static, media, locale, scripts va deployment layout fayllari.
- `docker/`, `docker-compose*.yml`, `stack.yaml`, `k8s/` - deployment va infra konfiguratsiyalar, agar mavjud bo'lsa.
- `Makefile` - lokal development, migration va test commandlari.

Ko'p loyihalarda Django REST Framework, Celery, Redis, PostgreSQL, drf-spectacular, django-filter, django-unfold, modeltranslation/parler, cacheops, channels, storage yoki boshqa optional paketlar bo'lishi mumkin. Faqat repo ichida real ishlatilayotganlarini hisobga ol.

## Architecture Rules

Yangi kod yozishda mavjud qatlamlarga amal qil:

- `models/` - database modeli, fieldlar, `__str__`, test data helperlari, modelga yaqin invariantlar.
- `serializers/` - input/output serializerlar, request validation, object create/update mapping.
- `views/` - DRF ViewSet/APIView, permissions, queryset, routing va schema metadata.
- `services/` - biznes logika, hisob-kitoblar, reusable domain operationlar, tashqi servis wrapperlari.
- `tasks/` - Celery yoki boshqa async ishlar.
- `signals/` - model lifecycle side-effect'lari. Faqat sodda va zarur holatda ishlat.
- `admin/` - Django admin konfiguratsiyasi.
- `filters/` - django-filter filterset yoki filter helperlari.
- `translation/` - modeltranslation/parler konfiguratsiyasi, agar loyiha tarjima ishlatsa.
- `permissions/` - reusable permission classlar.
- `validators/` - reusable validation helperlari.
- `tests/` - API, service va domain behavior testlari.

Yangi feature qaysi app'ga tegishli bo'lsa, shu app ichida parallel strukturani saqla. Agar appda `models`, `serializers`, `views`, `services`, `tasks`, `signals`, `tests` kabi papkalar mavjud bo'lsa, yangi kodni shu pattern bo'yicha joylashtir.

`__init__.py` export patterni mavjud bo'lsa, yangi modulni u yerga qo'sh. URL kerak bo'lsa app'ning `urls.py` faylida router yoki path bilan ro'yxatdan o'tkaz.

## Coding Style

- Python 3.12 va loyihadagi mavjud Django/DRF patternlaridan foydalan.
- `pyproject.toml`dagi format/lint qoidalariga amal qil. Odatda `black`, `isort`, `flake8` line length 120 ishlatiladi.
- Importlarni tartibli saqla: standard library, third-party, local imports.
- User-facing matnlar tarjima qilinadigan bo'lsa `django.utils.translation.gettext_lazy as _` ishlat.
- Mavjud naming uslubini davom ettir: model classlari, serializer nomlari, viewset nomlari va basename patternlari repo ichidagi o'xshash fayllarga mos bo'lsin.
- Umumiy biznes logika view ichida qolmasin, `services/`ga chiqarilsin.
- Tashqi API, xabar yuborish, moliyaviy operatsiya, storage, email/SMS, webhook, infra yoki boshqa integratsiya chaqiriqlari bevosita view/serializer ichida cho'zilib ketmasin; servis yoki task orqali ajrat.
- Unrelated refactor, format churn yoki fayl ko'chirish qilma.
- Yangi kodda typo qoldirma. Eski noto'g'ri nom public API yoki migrationga bog'langan bo'lsa, compatibilityni buzmasdan alohida refactor reja qil.
- `# type: ignore` faqat aniq sabab bo'lsa ishlatiladi. Yangi kodda type ignoreni default yechim sifatida qo'shma.
- `print()` o'rniga `logging` ishlat. Management commandlarda user-facing output uchun `self.stdout`, `self.stderr` yoki mavjud console patternidan foydalan.
- Bo'sh `pass`, `assert True`, kommentga olingan test va yakunlanmagan TODOlarni finished code sifatida qoldirma.

## Models and Migrations

- Agar loyihada `django_core.models.AbstractBaseModel` ishlatilayotgan bo'lsa, yangi domain modellarda ham shu patternni saqla.
- Har bir modelda ma'noli `__str__()` yoz.
- Testlar uchun repo patterniga mos fake/bakery helper qo'sh. Mavjud loyihalarda bu `_create_fake()`, `_baker()` yoki `model_bakery.baker.make()` bo'lishi mumkin.
- Agar app modellari `Meta.db_table`, `verbose_name`, `verbose_name_plural` ishlatsa, yangi modelda ham shu uslubni davom ettir.
- Relationshiplarda `related_name` kerak bo'lsa aniq va o'qilishi oson nom tanla.
- Model o'zgarsa migration yaratish majburiy.
- Eski migrationlarni qo'lda o'zgartirma, agar foydalanuvchi aniq shuni so'ramasa.
- Pul, miqdor, count, limit va quota kabi fieldlarda repo ichidagi mavjud field type patternlariga mos yur.
- Constraint kerak bo'lsa database-level constraint yoz: `UniqueConstraint`, index yoki model validation bilan cheklanib qolma.

## API and DRF Rules

- ViewSetlarda loyiha ishlatayotgan base mixin patternini saqla. JST loyihalarda ko'pincha `django_core.mixins.BaseViewSetMixin` ishlatiladi.
- Public read endpointlar, authenticated endpointlar va admin/internal endpointlar permissions bilan aniq ajratilsin.
- Userga tegishli resurslarda `get_queryset()` doim owner/user/project scope bilan filter qilinsin.
- Har bir endpoint uchun serializer tanlovi aniq bo'lsin. Agar repo patternida `action_serializer_class` ishlatilsa, shu uslubni davom ettir.
- Actionga qarab permission kerak bo'lsa `action_permission_classes` yoki mavjud permission patternidan foydalan.
- Router registratsiyasi app `urls.py` ichida barqaror `basename` bilan qilinsin.
- Custom actionlar uchun `@action(methods=[...], detail=..., url_path=..., url_name=...)` patternidan foydalan.
- Swagger/OpenAPI ishlatilsa, yangi yoki o'zgargan endpointlar uchun `drf_spectacular` schema, summary, request/response va muhim error response'larni yangila.
- Response shape mavjud API contractga mos bo'lsin. Mavjud `status/data/detail` wrapper patterni bo'lsa, uni buzma.

## Serializers

- Mavjud serializer naming patternini davom ettir. Ko'p JST loyihalarda `Base`, `List`, `Retrieve`, `Create`, `Update` serializerlar ajratiladi.
- `Base<Entity>Serializer` umumiy fieldlar uchun.
- `List<Entity>Serializer` ro'yxat response uchun.
- `Retrieve<Entity>Serializer` detail response uchun.
- `Create<Entity>Serializer` input validation va object yaratish uchun.
- `Update<Entity>Serializer` update/partial_update alohida behavior talab qilsa.
- `to_representation()` faqat response formatini ataylab o'zgartirish kerak bo'lsa override qil.
- Request user kerak bo'lsa `self.context.get("request")` orqali ol.
- Bir nechta database o'zgarishi bitta operatsiya bo'lsa `django.db.transaction.atomic` ishlat.
- Validation xatolarini DRF `serializers.ValidationError` yoki `rest_framework.exceptions.ValidationError` bilan qaytar.
- Serializer ichida uzoq ishlaydigan external side-effectlarni boshlama; bunday ishni service/taskga chiqar.

## Services, Tasks, and Signals

- Hisob-kitoblar, state transitionlar, tashqi integratsiyalar va reusable domain operationlar `services/`da bo'lsin.
- Async ishlar `tasks/` ichida bo'lsin va loyiha ishlatayotgan queue patterniga mos yozilsin.
- Tasklar idempotent bo'lishi kerak: qayta ishlasa duplicate zarar bermasin.
- Task ichida tashqi servis xatosi bo'lsa log qil, retry kerakmi-yo'qmi aniq belgilab yoz.
- Tashqi servisga ketadigan har bir operatsiya timeout, error logging va failure strategyga ega bo'lsin.
- Signal ichida og'ir ish qilma; og'ir ishni service yoki taskga chiqar.
- Signal ichida `save()` chaqirishdan oldin recursion, duplicate side-effect va transaction holatini tekshir.
- Muhim state transitionlar, masalan balans, quota, subscription, deploy, export, xabar yuborish yoki boshqa ko'p bosqichli jarayonlar transaction va idempotency bilan himoyalansin.

## Optional Integrations

Har bir loyiha turlicha integratsiyalarga ega bo'lishi mumkin. Integratsiya mavjud bo'lsa, quyidagilarga amal qil:

- Moliyaviy integratsiya mavjud bo'lsa: signature/callback verification, idempotency, double-submit protection, transaction rollback va audit trail bo'lishi kerak.
- Bot/SMS/Email: tokenlar env/secret orqali olinadi, rate limit va retry behavior o'ylanadi.
- Storage/File: file path va file type validatsiyasi bo'ladi, user ownership tekshiriladi.
- Webhook: authentication yoki signature tekshiruvi bo'ladi, request replay xavfi hisobga olinadi.
- WebSocket/SSE: auth middleware, user scope va event payload schema aniq bo'ladi.
- Kubernetes/Docker/Infra: deployment nomlari, namespace, env secretlar va cleanup idempotent bo'lishi kerak.
- MongoDB yoki boshqa NoSQL: user/project scope, collection/field validation va query sanitization bo'lishi kerak.

## Admin, Filters, and Translation

- Admin konfiguratsiyasi tegishli `admin/` modulida bo'lsin va mavjud import/export patterniga ulang.
- Filter kerak bo'lsa `filters/` ichida saqla va viewsetda `DjangoFilterBackend` bilan ulang.
- Search kerak bo'lsa DRF `SearchFilter` va `search_fields` ishlat.
- Tarjima qilinadigan model fieldlar uchun loyiha ishlatayotgan translation kutubxonasi patterniga amal qil.
- Yangi admin, translation, signal yoki task fayl qo'shilsa app startup importlari ishlashini tekshir.

## Testing Rules

- Testlar repo patterniga mos yoziladi: `pytest`, Django `TestCase`, `APIClient`, fixture yoki bakery helperlar.
- Auth kerak bo'lsa `client.force_authenticate(user)` yoki loyiha ishlatayotgan auth helperdan foydalan.
- Endpoint nomlarini hardcode qilma; `django.urls.reverse()` ishlat.
- Tashqi servis, storage, bot/SMS/email, moliyaviy integratsiya, webhook, infra, NoSQL va boshqa side-effectlarni mock qil.
- Response patternlarda mavjud loyihadagi wrapper va HTTP status kodlarni tekshir.
- Yangi behavior qo'shilsa kamida success, validation error va permission/user-scope holatlarini test qil.
- `test_update`, `test_destroy`, `test_partial_update` kabi testlar `assert True` bo'lib qolmasin. Real request yuborib, database holatini tekshir.
- Mock testlar faqat "chaqirildi"ni emas, muhim argumentlar va xatolik holatini ham tekshirsin.
- User-scope endpointlarda boshqa user ma'lumotiga kira olmaslik holatini test qil.
- State transitionlarda double-submit, insufficient quota/balance, expired/invalid token/code va rollback holatlarini test qil.

## Security and Repo Hygiene

- Private key, token, password, credential, `.env`, production dump yoki real secretlarni repo ichiga qo'shma.
- Private materiallar kerak bo'lsa `.env`, secret manager, CI secret yoki deploy secret orqali uzatiladi.
- `__pycache__/`, `.pyc`, `.pytest_cache/`, local logs, local media va generated build cache fayllarini commit qilma.
- Public key ham faqat kerak bo'lsa va xavfsizlik modeli aniq bo'lsa repo ichida saqlansin.
- User inputdan kelgan file path, webhook, URL, token, callback, query va filter qiymatlarini validatsiyasiz ishlatma.
- Admin-only schema, debug endpoint, metrics, silk/profiling route'lari productionda ochiq qolmasin.
- External webhook endpointlarida authentication/signature/token verification borligini tekshir.
- Sensitive qiymatlarni logga chiqarmang: token, password, private key, authorization header, secret key, database credential.

## Improvement Priorities

Yangi vazifa bajarayotganda imkon bo'lsa quyidagi qarzlarni kamaytir:

- Typo va naming qarzi: yangi kodda noto'g'ri nomlar takrorlanmasin. Eski nomlar public API yoki migrationga bog'langan bo'lsa, compatibilityni buzmasdan alohida refactor reja qil.
- View semizligini kamaytir: katta orchestration view ichida qolsa, uni serializer/service/task qatlamiga ajrat.
- Serializer side-effectlarini kamaytir: serializer validation va object mappingga javob bersin; tashqi servis, xabar yuborish, moliyaviy operatsiya, webhook, deploy kabi ishlar service/task orqali yursin.
- Signal side-effectlarini kamaytir: murakkab oqimlar signalda emas, explicit service yoki taskda boshqarilsin.
- Test coverage chuqurlashtir: yuzaki success testlardan tashqari error, permission, ownership, transaction rollback va external service failure testlarini qo'sh.
- Type/lint discipline: yangi kod `pyright basic`, `flake8`, `black`, `isort`ga mos yozilsin; `# type: ignore` soni oshirilmasin.
- Documentation: API behavior o'zgarsa Swagger schema va kerakli docs yangilansin.

## Quality Bar for New Code

Yangi kod "tayyor" hisoblanishi uchun:

- Feature mavjud app arxitekturasiga mos joylashgan bo'lishi kerak.
- Har bir endpointda serializer, permission, queryset ownership/scope va schema aniq bo'lishi kerak.
- DB o'zgarishi migration bilan kelishi kerak.
- Business logic view ichida cho'zilib ketmasligi kerak.
- External side-effectlar mock qilinadigan service/taskga ajratilgan bo'lishi kerak.
- Kamida tegishli happy path va muhim failure path testlari bo'lishi kerak.
- Secrets yoki generated fayllar qo'shilmagan bo'lishi kerak.
- O'zgarish unrelated fayllarni formatlamagan yoki revert qilmagan bo'lishi kerak.

## Commands

Avval repo ichidagi `Makefile`, `README` va docsni tekshir. JST loyihalarda ko'pincha quyidagi commandlar bo'ladi:

```bash
make up
make down
make makemigrate
make makemigration
make migrate
make test
```

Bevosita container ichida command ishlatish patterni:

```bash
docker compose exec web python manage.py <command>
docker compose exec web pytest -v
```

Loyiha Docker ishlatmasa yoki commandlar farq qilsa, mavjud `README`, `Makefile`, CI config va `pyproject.toml`ga tayan.

## Do

- Avval mavjud fayllarni o'qi, keyin kod yoz.
- Mavjud app va qatlam strukturasi bilan ishlagin.
- Kichik, aniq, review qilish oson o'zgarishlar qil.
- Model o'zgarsa migration qo'sh.
- API o'zgarsa serializer, view, url, schema va testlarni birga yangila.
- Tashqi side-effectlarni testlarda mock qil.
- Userga tegishli querylarda querysetni user/project/tenant scope bilan chekla.
- Tarjima qilinadigan user-facing text uchun loyiha translation patternidan foydalan.

## Don't

- Unrelated refactor qilma.
- Secrets yoki real tokenlarni commit qilma.
- `__pycache__`, `.pyc`, local cache va generated temporary fayllarni commit qilma.
- View ichiga katta biznes logika yozma.
- Serializer ichidan uzoq ishlaydigan tashqi API chaqiriqlarini bevosita qilma.
- Signal ichida murakkab yoki sekin ishlarni bajarma.
- Eski migrationlarni sababsiz tahrirlama.
- Global settingsga keraksiz dependency qo'shma.
- Mavjud response shape, router basename yoki endpoint nomlarini sababsiz o'zgartirma.
- User yozgan yoki repo ichida mavjud unrelated o'zgarishlarni revert qilma.
- Yangi kodda `assert True`, bo'sh `pass`, noaniq `except Exception: pass` yoki sababsiz `# type: ignore` qoldirma.

## Agent Workflow

1. Vazifani o'qib, tegishli app va qatlamlarni top.
2. Mavjud o'xshash model/view/serializer/service/testlarni o'rgan.
3. Loyiha qaysi optional integratsiyalarni ishlatayotganini aniqlab ol.
4. Minimal implementation rejasini tuz.
5. Kerakli fayllarnigina o'zgartir.
6. Model o'zgargan bo'lsa migration yarat.
7. Tegishli testlarni yoz yoki yangila.
8. Eng kichik zarur test to'plamini ishga tushir.
9. Natijada nima o'zgargani va qaysi testlar ishlaganini qisqa ayt.

## Pre-PR Review Checklist

Kod topshirishdan oldin agent o'zidan so'rasin:

- Bu o'zgarish mavjud JST/Django app strukturasi bilan mosmi?
- View, serializer, service, task va signal chegaralari to'g'rimi?
- User/project/tenant ownership va permission tekshiruvlari yetarlimi?
- Muhim state transitionlar transaction va idempotency bilan himoyalanganmi?
- Tashqi servis xatolari log qilinyaptimi va testda mock qilinganmi?
- Migration kerak bo'lsa qo'shildimi?
- Testlar real behaviorni tekshiryaptimi yoki faqat status code bilan cheklanyaptimi?
- Repo ichiga secret, cache, `.pyc`, private key yoki local artifact kirmadimi?
- API response shape va router nomlari sababsiz o'zgarmadimi?
- Yangi typo, `print()`, `pass`, `assert True`, sababsiz `# type: ignore` qoldimi?
