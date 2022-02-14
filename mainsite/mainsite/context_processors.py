import os


def export_covid_var(request):
    data = {'ENABLE_COVID_WARNING_CLASS': ''}

    if os.environ.get('ENABLE_COVID_WARNING') is None:
        data['ENABLE_COVID_WARNING_CLASS'] = 'covid-warning-disabled'
    elif os.environ.get('ENABLE_COVID_WARNING') == 'false':
        data['ENABLE_COVID_WARNING_CLASS'] = 'covid-warning-disabled'

    return data
