from rest_framework import serializers


class FillingNotOutTwoFieldsValidator:
    """ Валидатор проверят, что одновременно не заполнены 2 поля """

    def __init__(self, first_field, second_field, message=None):
        self.message = message
        self.first_field = first_field
        self.second_field = second_field

    def __call__(self, value):
        if dict(value).get(self.first_field) and dict(value).get(self.second_field):
            if not self.message:
                self.message = f'Недопустимо одновременно указывать "{self.first_field}" и "{self.second_field}"'
            raise serializers.ValidationError(self.message)
