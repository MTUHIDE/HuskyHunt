# Cloned from https://github.com/vzhou842/profanity-check

import pkg_resources
import numpy as np
import joblib

import warnings
_old_warn = warnings.warn
warnings.warn = lambda *args, **kwargs: None

vectorizer = joblib.load(pkg_resources.resource_filename('profanity_check', 'data/vectorizer.joblib'))
model = joblib.load(pkg_resources.resource_filename('profanity_check', 'data/model.joblib'))

warnings.warn = _old_warn

def _get_profane_prob(prob):
  return prob[1]

def predict(texts):
  return model.predict(vectorizer.transform(texts))

def predict_prob(texts):
  return np.apply_along_axis(_get_profane_prob, 1, model.predict_proba(vectorizer.transform(texts)))
