from bson import ObjectId

from app.utils.ApiError import ApiError
from app.utils.db_utils import companies_collection, userselection_collection


def find_companies(user_id):
    selection_collection = userselection_collection()
    selected_item = selection_collection.find({'user_id': user_id})
    selected = ''
    if selected_item is not None:
        selected = selected_item['company_id']
    collection = companies_collection()
    result = collection.find({"$and": [{'access_users': user_id}, {'deleted': False}]})
    ret_result = []
    for x in result:
        company_id = str(x['_id'])
        is_default = company_id == selected
        obj = {
            'id': company_id,
            'name': x.get('name'),
            'address': x.get('address'),
            'taxId': x.get('taxId'),
            'is_default': is_default,
        }
        ret_result.append(obj)
    return {
        'default_selection': selected,
        'companies': ret_result
    }


def create_company(company, user_id):
    collection = companies_collection()
    print(company)
    company_to_store = {
        'name': company.get("name"),
        'address': company.get("address"),
        'taxId': company.get("taxId"),
        'deleted': False,
        "access_users": [user_id],
        "creator": user_id,
    }
    ret = collection.insert_one(company_to_store)
    print("ret")
    print(ret)
    return str(ret.inserted_id)


def update_company(company, user_id):
    company_to_store = {'$set': {
        "name": company.get('name'),
        "address": company.get('address'),
        "taxId": company.get('taxId')
    }
    }
    _do_update(company_to_store, user_id, company.get('id'))


def delete_company(id, user_id):
    company_to_store = {'$set': {
        "deleted": True,
    }
    }
    return _do_update(company_to_store, user_id, id)


def update_selected_company(company_id, user_id):
    collection = userselection_collection()
    collection.update_one({'user_id': user_id}, {'$set': {'user_id': user_id, 'company_id': company_id}})
    pass


def find_selected_company(user_id):
    collection = userselection_collection()
    ret = collection.find({'user_id': user_id})
    return ret['company_id']


def _do_update(company_to_store, user_id, object_id):
    collection = companies_collection()
    ret = collection.update_one(
        {"$and": [{'access_users': user_id}, {'deleted': False}, {"_id": ObjectId(object_id)}]},
        company_to_store)
    if ret.matched_count != 1:
        raise ApiError({"code": "not_updated",
                        "description":
                            "Not updated. "
                            "Company was not updated"}, 500)

    return ret.matched_count
