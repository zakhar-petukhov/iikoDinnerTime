from apps.api.company.models import Company


def get_tariff_structure(serializer_data):
    companies = dict()

    for data in serializer_data:
        if not data['company']:
            continue

        company_id = data['company']

        if not companies.get(company_id):
            company = Company.objects.get(pk=company_id)
            companies.update({
                company_id: {"company_name": company.company_name,
                             "company_information": list()
                             }})

        companies[company_id]['company_information'].append({
            "id": data['id'],
            "name": data['name'],
            "max_cost_day": data['max_cost_day'],
            "description": data['description'],
            "is_blocked": data['is_blocked'],
        })

    return companies.values()
