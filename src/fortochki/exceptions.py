


class InvalidAuthError(Exception):
    message = 'Неудачная авторизации.'

class UnexpectedResponseError(Exception):
    message = 'Неожиданный ответ от сервера.'

class UnsuccessfullySeriesOfRequests(Exception):
    message = 'Неудачная серия попыток сделать запрос.'

class HTTPError500(Exception):
    message = 'Сервер вернул 5хх-й статус.'

class UnexpectedStatusError(Exception):
    message = 'Неожиданный статус ответа от сервера.'