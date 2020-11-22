# TODO: соединить две функции "check_oversupply_tariff" и "create_companies_structure" вместе, чтобы упростить сложность
def check_oversupply_tariff(serializer_data, search_key, return_key, for_admin=False, query_params=False):
    # Function to calculate the monthly exceedance of the limit for the employees of the company, as well
    # as exceedance of the limit of the entire order of the company for the administrator

    oversupply_tariff = 0

    if query_params:
        for tariff in serializer_data:
            oversupply_tariff += tariff.get(search_key, 0)

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

    dinners_data = dinner_data['data']
    full_oversupply_tariff = dinner_data.get('full_oversupply_tariff')

    for data in dinners_data:
        company_structure = {'order_number': data['id'], 'company': data['company'], 'company_department': list()}
        date_action_begin = None

        for information in data['dinners']:
            department_address = {"full_address": None, "data": list()}
            department_structure = {"department_name": None, "information": None}

            department_information = dict()

            department_name = information['user']['group']['name']
            delivery_information = information['user']['group']['address_for_delivery']

            if not department_information.get(department_name):
                department_information[department_name] = list()

            department_information.get(department_name).append({
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
                    "oversupply_tariff": information.get('oversupply_tariff', 0),
                }
            })

            date_action_begin = information['date_action_begin']

            for name, information in department_information.items():
                department_structure['department_name'] = name
                department_structure['information'] = information

                department_address['full_address'] = delivery_information['full_address']
                department_address['data'].append(department_structure)

            if not company_structure['company_department']:
                company_structure['company_department'].append(department_address)

            else:
                for department in company_structure['company_department']:
                    if department['full_address'] == delivery_information['full_address']:
                        department['data'].append(department_structure)

                    else:
                        company_structure['company_department'].append(department_address)

        company_structure["dinners_oversupply_tariff"] = data['dinners_oversupply_tariff']
        company_structure['full_oversupply_tariff'] = full_oversupply_tariff
        company_structure['full_cost'] = data['full_cost']
        company_structure['send_iiko'] = data['send_iiko']
        company_structure['date_action_begin'] = date_action_begin

        structure.append(company_structure)

    return structure


# TODO: переписать логику на уровне бд, очень ресурсно затраный запрос получился
def create_structure_by_dishes(serializer_data):
    # Function to create the structure of dishes, we get the name of the dishes and their quantity

    structure = list()

    for dinner in serializer_data:
        full_dishes = dict()

        for dishes in dinner['dinner_to_dish']:
            dish_name = dishes['dish']['name']
            dish_count = dishes['count_dish']
            category_dish = dishes['dish']['category_dish']['name']

            if not full_dishes.get(dish_name):
                full_dishes.update({
                    dish_name: {"count_dish": dish_count, "category_dish": category_dish}
                })

            else:
                full_dishes[dish_name]["count_dish"] += dish_count

        for dish_name, information in full_dishes.items():
            structure.append({
                "dish_name": dish_name, "count_dish": information['count_dish'],
                "category_name": information['category_dish']
            })

    structure_category = list()
    category = dict()

    for information in structure:
        category_name = information['category_name']

        if category.get('category_name') is not None and category.get('category_name') != category_name:
            append_category = True
            for category_dict in structure_category:
                if category_dict.get('category_name') == category_name:
                    category_dict.get('data').append(
                        {"count_dish": information['count_dish'], "dish_name": information['dish_name']})

                    append_category = False

            if append_category:
                structure_category.append(category)

                category = dict()

                category['category_name'] = category_name
                category['data'] = [{"count_dish": information['count_dish'], "dish_name": information['dish_name']}]

        elif category.get('category_name') != category_name:
            category['category_name'] = category_name
            category['data'] = [{"count_dish": information['count_dish'], "dish_name": information['dish_name']}]

        else:
            category['data'].append({"count_dish": information['count_dish'], "dish_name": information['dish_name']})

    structure_category.append(category)

    return structure_category
