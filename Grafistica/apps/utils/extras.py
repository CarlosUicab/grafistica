import uuid
import traceback
from django.utils import timezone
from Grafistica.core.json_reader import json_settings

settings = json_settings()


def get_cleaned_uuid():
    """
    Eliminamos guiones de los objetos tipo UUID
    :return:
    """
    uuid_ = (str(uuid.uuid1()).replace('-', ''))
    return uuid_


def days_to_active_account():
    """
    Calculamos una fecha
    :return:
    """
    return timezone.now() + timezone.timedelta(days=settings['SECURITY']['DAYS_TO_ACTIVATE_ACCOUNT'])


def format_sys_errors(user_sys, with_traceback=False):
    """
    Obtenemos una representación más clara de cualquier error surgido en el sistema.
    """
    if user_sys:
        etype, value, tb = user_sys.exc_info()
        tipo_error_name = etype.__name__
        error_args = value.args
        if with_traceback:
            mensaje = "{0} {1} {2}".format(tipo_error_name, error_args, traceback.extract_tb(tb))
        else:
            traceback.print_tb(tb)
            mensaje = "{0} {1}".format(tipo_error_name, error_args)
        return mensaje
    else:
        return ""