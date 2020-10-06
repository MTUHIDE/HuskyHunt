from django import forms
from django.forms import ModelForm

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    from profanity_check import predict, predict_prob

class ProfFiltered_ModelForm( ModelForm ):
    def __init__(self, *args, **kwargs):

        # If request.POST, request.FILES are passed to it, aka, POST rather than GET
        if(len(args) > 0):
            override_text = kwargs.pop('override_text', "Submit Anyway")
            self.profCheck = not (args[0].get( 'submit_btn' ) == override_text)
        else:
            self.profCheck = False # save() is only called on a POST form anyways

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        super().save(commit)    # if errors, should raise ValueError and skip next lines

        if not self.profCheck:
            # TODO: Raise to mod attention for real
            print("TODO: Raise for mod approval")


    def profanity_cleaner(self, target):
        value = self.cleaned_data[target]
        if value is None:
            return None

        if self.profCheck:
            tokens = value.split(' ') # there are fancier tokenizing schemes but eh, split on space works
            profane_tokens = [ t[0] for t in zip(tokens, predict(tokens)) if t[1] ]

            if len(profane_tokens) > 0:
                message = ', '.join(profane_tokens)
                raise forms.ValidationError( message,
                    code="profane",
                    params={
                        'target_label': target.replace('_', ' ').capitalize(),  # default django behavior
                        'profane_strings': profane_tokens
                    })
        return value
