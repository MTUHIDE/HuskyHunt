import os

def export_covid_var(request):
  data = {}

  data['ENABLE_COVID_WARNING_CLASS'] = ''

  if os.environ.get('ENABLE_COVID_WARNING') is None:
    data['ENABLE_COVID_WARNING_CLASS'] = 'covid-warning-disabled'

  return data
