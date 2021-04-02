from django import forms
from django.forms import ModelForm
from profanity_check.models import ArchivedType

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    from profanity_check import predict, predict_prob

class ProfFiltered_ModelForm( ModelForm ):
    def __init__(self, *args, **kwargs):

        # If request.POST, request.FILES are passed to it, aka, POST rather than GET
        if(len(args) > 0):
            self.profCheck = True
            override_text = kwargs.pop('override_text', "Submit Anyway")
            self.profOverride = (args[0].get( 'submit_btn' ) == override_text)
        else:
            self.profCheck = False # save() is only called on a POST form anyways

        self.profResult = False

        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        retval = super().save(commit=False)

        if not hasattr(retval, 'archived'):
            return retval

        # Item has been flagged by the profanity filter.
        if self.profResult:
            # Report the item, mark it as archived, and hide it.
            retval.reported = "True"
            retval.archived = "True"
            retval.archivedType = ArchivedType.Types.HIDDEN
        # Item was previously flagged by the profanity filter and removed,
        # But no profanity was found this time.
        elif retval.archived == True and retval.archivedType == ArchivedType.Types.REMOVED:
            # Move the item's status back to hidden so it can be reviewed again.
            retval.reported = "True"
            retval.archivedType = ArchivedType.Types.HIDDEN

        if commit:
            retval.save()
        return retval


    def profanity_cleaner(self, target):
        value = self.cleaned_data[target]
        if value is None:
            return None

        if self.profCheck:
            tokens = value.split(' ') # there are fancier tokenizing schemes but eh, split on space works
            profane_tokens = [ t[0] for t in zip(tokens, predict(tokens)) if t[1] ]

            # We found some profanity.
            if len(profane_tokens) > 0:
                self.profResult = True

                if not self.profOverride:
                    message = ', '.join(profane_tokens)
                    raise forms.ValidationError( message,
                        code="profane",
                        params={
                            'target_label': target.replace('_', ' ').capitalize(),  # default django behavior
                            'profane_strings': profane_tokens
                        })
        return value
