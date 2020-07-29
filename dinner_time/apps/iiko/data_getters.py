from django.conf import settings


def send_dishes_data(kwargs):
    dinners = kwargs.dinners.all()
    company = kwargs.company.company_data
    user = kwargs.company

    phone_number = f"{user.phone.country_code}{user.phone.national_number}"
    guid_restaurant = settings.IIKO_ORGANIZATION_ID

    data = {
        "organization": guid_restaurant,
        "customer": {
            "name": user.get_full_name(),
            "phone": phone_number
        },
        "order": {
            "phone": phone_number,
            "isSelfService": "false",
            "items": [],
            "address": {
                "city": company.city,
                "street": company.street,
                "home": company.house,
                "housing": company.house_building if company.house_building else "",
                "apartment": company.apartment,
            }
        }
    }
    for dinner in dinners:
        data['order']['date'] = dinner.date_action_begin.strftime('%Y-%m-%d %H:%M:%S')
        for dish in dinner.dishes.all():
            data['order']['items'].append(
                {
                    "id": dish.upid,
                    "name": dish.name,
                    "code": dish.code,
                    "amount": 1,
                    "sum": dish.cost,
                }
            )

    return data
