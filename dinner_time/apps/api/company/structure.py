# TODO: соединить две функции "check_oversupply_tariff" и "create_companies_structure" вместе, чтобы упростить сложность
def check_oversupply_tariff(serializer_data, search_key, return_key, for_admin=False, query_params=False):
    # Function to calculate the monthly exceedance of the limit for the employees of the company, as well
    # as exceedance of the limit of the entire order of the company for the administrator

    oversupply_tariff = 0

    if query_params:
        for tariff in serializer_data:
            oversupply_tariff += tariff[search_key]

    dinner_data = {
        return_key: oversupply_tariff,
        "data": serializer_data
    }

    if for_admin:
        return create_companies_structure(dinner_data)

    return dinner_data


def create_companies_structure(dinner_data):
    # We create our own structures, to be issued to the front.
    # Sort people by working groups and tie the lunches to them.

    structure = list()

    company_structure = {
        'company': None,
        'company_department': list()
    }

    department_structure = {
        "department_name": None,
        "information": None,
    }

    dinners_data = dinner_data['data']
    full_oversupply_tariff = dinner_data.get('full_oversupply_tariff')

    for data in dinners_data:
        company_structure['company'] = data['company']
        group = dict()

        for information in data['dinners']:
            department_name = information['user']['group']['name']

            if not group.get(department_name):
                group[department_name] = list()

            group.get(department_name).append({
                "person": {
                    "id": information['user']['id'],
                    "first_name": information['user']['first_name'],
                    "last_name": information['user']['last_name'],
                    "middle_name": information['user']['middle_name'],
                    "phone": information['user']['phone'],
                    "email": information['user']['email'],
                    "company_data": information['user']['company_data'],
                },

                "dinners": {
                    "id": information['id'],
                    "dinner_to_dish": information['dinner_to_dish'],
                    "date_action_begin": information['date_action_begin'],
                    "status": information['status'],
                    "status_name": information['status_name'],
                    "full_cost": information['full_cost'],
                    "oversupply_tariff": information['oversupply_tariff'],
                },

                "full_cost": data['full_cost'],
                "dinners_oversupply_tariff": data.get('dinners_oversupply_tariff'),
                "send_iiko": data['send_iiko'],
            })

        for key, value in group.items():
            department_structure['department_name'] = key
            department_structure['information'] = value

            company_structure['company_department'].append(department_structure)

        company_structure['full_oversupply_tariff'] = full_oversupply_tariff

        structure.append(company_structure)

    return structure


def create_structure_by_dishes(serializer_data):
    # Function to create the structure of dishes, we get the name of the dishes and their quantity

    structure = list()
    full_dishes = dict()

    for dinner in serializer_data:
        for dishes in dinner['dinner_to_dish']:
            dish_name = dishes['dish']['name']
            dish_count = dishes['count_dish']

            if not full_dishes.get(dish_name):
                full_dishes.update({
                    dish_name: dish_count
                })

            else:
                full_dishes[dish_name] += dish_count

        for dish_name, count_dish in full_dishes.items():
            structure.append({"dish_name": dish_name, "count_dish": count_dish})

    return structure
