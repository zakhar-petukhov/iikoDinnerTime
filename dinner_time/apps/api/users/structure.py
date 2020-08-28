from apps.api.company.models import Company


def get_tariff_structure(serializer_data):
    structure = dict()
    companies = dict()

    for data in serializer_data:
        if not data['company']:
            continue

        company_id = data['company']

        if not companies.get(company_id):
            company = Company.objects.get(pk=company_id)
            companies[company_id] = company.company_name

        if not structure.get(companies[company_id]):
            structure[companies[company_id]] = list()

        structure.get(companies[company_id]).append({
            "id": data['id'],
            "name": data['name'],
            "max_cost_day": data['max_cost_day'],
            "description": data['description'],
            "is_blocked": data['is_blocked'],
        })

    return structure
