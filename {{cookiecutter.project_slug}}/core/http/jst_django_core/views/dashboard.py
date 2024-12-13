def dashboard_callback(request, context):
    context.update(
        {
            "cards": (
                {
                    "color": "blue",
                    "value": 10000,
                    "title": "Shartnomalar",
                },
                {
                    "color": "primary",
                    "value": 10000,
                    "title": "Tugallangan",
                },
                {
                    "color": "orange",
                    "value": 10000,
                    "title": "Kutilmoqda",
                },
                {
                    "color": "red",
                    "value": 10000,
                    "title": "Bekor qilingan",
                },
                {
                    "color": "green",
                    "value": 10000,
                    "title": "Bajarilmoqda",
                },
                {
                    "color": "red",
                    "value": "{:,} so'm".format(10000),
                    "title": "Qarizlar",
                },
                {
                    "color": "green",
                    "value": "{:,} so'm".format(10000),
                    "title": "To'langan",
                },
                {
                    "color": "green",
                    "value": "{:,} so'm".format(10000),
                    "title": "Jami summa",
                },
            ),
        }
    )

    return context
