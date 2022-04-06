from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        print(f"ВЫВОД из data {data}")
        print(f' {self.context["request"].user.id}')
        count_adver= Advertisement.objects.filter(creator=self.context["request"].user.id, status="OPEN")


        i = 0
        for _ in count_adver:
            i+=1

        print(f"У ВАС {i} открытых обьявлений" )
        if i > 9:
            raise ValidationError(f"У ВАС {i} ОТКРЫТЫХ  ОБЬЯВЛЕНИЙ")



        # TODO: добавьте требуемую валидацию

        return data
