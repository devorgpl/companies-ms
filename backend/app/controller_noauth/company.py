import logging

from app.domain.company_service import delete_company, find_companies, create_company, update_company


def findAll(user_id):
    logging.debug("findall(user_id=%s)", user_id)
    result = find_companies(user_id)
    logging.debug('findall():%s', str(result))
    return result


def store(user_id, company_command):
    logging.debug("findall(user_id=%s, command=%s)", user_id, company_command)
    if company_command.get('id') is None:
        result = create_company(company_command, user_id)
    else:
        result = update_company(company_command, user_id)
    logging.debug('store():%s', str(result))
    return result


def delete(user_id, company_id):
    logging.debug("findall(user_id=%s, company_id=%s)", user_id, company_id)
    result = delete_company(company_id, user_id)
    logging.debug('delete():%s', str(result))
    return result
