from django.template import loader
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import ClearableFileInput


class PreviewImageWidget(ClearableFileInput):
    template_name = "accountant/preview_image.html"

    clear_button_label = _('Reset')
    default_width = 150
    default_height = 150
    defaultPictureURL = 'https://www.mtu.edu/mtu_resources/images/download-central/social-media/gold-name.jpg'

    def clear_button_name(self, name):
        return name + '-clear'

    def clear_button_id(self, name):
        return name + '_id'

    def preview_image_name(self, name):
        return name + '-preview'

    def preview_image_id(self, name):
        return name + '_id'

    def reset_check_name(self, name):
        return name + '-reset'

    def reset_check_id(self, name):
        return name + '_id'

    # def format_value:

    def get_context(self, name, value, attrs):
        width = attrs.get('width', self.default_width)
        height = attrs.get('height', self.default_height)

        button_name = self.clear_button_name(name)
        button_id = self.clear_button_id(button_name)
        preview_name = self.preview_image_name(name)
        preview_id = self.preview_image_id(preview_name)
        reset_check_name = self.reset_check_name(name)
        reset_check_id = self.reset_check_id(reset_check_name)

        context = super().get_context(name, value, attrs)
        some_unneeded_fields = ['checkbox_name', 'checkbox_id', 'clear_button_label', 'is_initial', 'initial_text']
        for i in some_unneeded_fields:
            context.pop(i, None)

        context['widget'].update({
            # 'value':  #presumably passed up in the ModelForm
            'defaultPictureURL': self.defaultPictureURL,

            'button_name': button_name,
            'button_id': button_id,
            'clear_button_label': self.clear_button_label,

            'reset_check_id': reset_check_id,
            'reset_check_name': reset_check_name,

            # name, attrs -- inherited
            'id': (name + '_id'),

            'preview_text': "Uploaded Image",
            'preview_id': preview_id,
            'preview_width': width,
            'preview_height': height,
        })

        return context

    def value_from_datadict(self, data, files, name):
        return files.get(name)
