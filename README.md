# Referral System (Реферальная система)

Позволяет реализовать реферальную систему между пользователями. Каждый пользователь получает личный инвайт-код,
которым н может делиться с другими пользователями, в качестве реферальной ссылки.

## Для установки и запуск проекта:

    1. Клонировать проект в локальный репозиторий: `git clone git@github.com:Mishka1994/referral_system.git`
    
    2. Создать виртуальное окружение внутри проекта: `python3 -m venv env`

    3. Запустить проект с помощью команды: `docker-compose up --build`

## Конечные точки проекта:

1. POST ***api/create/***

Регистрирует и активирует пользователя по номеру телефона и отправляет код для активации пользователя.
Активация происходит при повторном запросе к адресу с указанием кода активации и номера телефона.

Пример кода для запроса на создание:

### Важно!

___Символ %2B распознается curl как знак сложения (+). Поэтому в запросах с curl нужно использовать именно такую
конструкцию!___

`curl POST --data "phone=%2B79998887766" http://localhost:8001/api/create/`

Пример кода для запроса на авторизацию:

`curl POST --data "phone=%2B79998887766&authorization_code=AAAA" http://localhost:8001/api/create/`

| Параметр строки запроса | Обязательный\ Не обязательный | Описание                                                              | тип данных |
|-------------------------|-------------------------------|-----------------------------------------------------------------------|------------|
| phone                   | Обязательный                  | Телефон пользователя, <br/> Макса ввода телефона:<br/>+7 ХХХ ХХХ ХХХХ | String     |
| authorization_code      | Необязательный                | Код для активации пользователя                                        | String     |

### Инструкция по авторизации и активации пользователя:

- В первом запросе нужно указать номер телефона. При успешном выполнении запроса, в терминале появляется 4-х значный
  код активации.
- Во втором запросе на этот же адрес добавьте появившейся код активации в поле *authorization_code* и повторите запрос.
  Если все выполнено верно, ответом будет словарь со значением **Вы авторизованы!**.

Примеры ответов:

- Если пользователь впервые делает запрос:

```
{"result": "Пользователь создан. Но нужно авторизоваться, введите код: ХХХХ при повторной отправке формы!"}
```

- При успешной авторизации:

```
{
"result": "Вы авторизованны!",
"data": {"user_phone": "+79998887766", "is_active": "True", "invite_code": qwe123"}
}
```

- При повторной авторизации:

```
{'result': f'Введите код: ХХХХ при повторной отправке формы'}
```

2. GET ***api/profile/***

Получает данные о профиле пользователя.

Пример кода для запроса на вывод информации о пользователе:

`curl -G -d "phone=%2B79998887766" http://localhost:8001/api/profile/`

| Параметр строки запроса | Обязательный/Не обязательный | Описание                                                              | Тип данных |
|-------------------------|------------------------------|-----------------------------------------------------------------------|------------|
| phone                   | Обязательный                 | Телефон пользователя, <br/> Макса ввода телефона:<br/>+7 ХХХ ХХХ ХХХХ | String     |

### Инструкция по получению личной информации пользователя

- Для получения данных о профиле пользователя нужно указать номер телефона при запросе в переменной _phone_.

Прим. __В этом случае параметр 'phone' является обязательным!__

Примеры ответов:

- При успешном запросе на профиль пользователя:

```
{'result': 'Ваш профиль:',
     'profile_data': {
                'phone': +79998887766,
                'activation_status':True,
                'personal_invite_code': q1w2e3,
                'someone_invite_code': a1s2d3,
                'referral_users': +79134568796,
                                          +79564521974                 
                }
```

#### Таблица с описанием пунктов ответа

| Пункт ответа         | Описание                                                  | Тип данных |
|----------------------|-----------------------------------------------------------|------------|
| phone                | Номер телефона                                            | String     |
| activation_status    | Статус пользователя                                       | Boolean    |
| personal_invite_code | Личный инвайт-код пользователя                            | String     |
| someone_invite_code  | Инвайт-код, введенный пользователем                       | String     |
| referral_users       | Список пользователей, который использовали ваш инвайт-код | String     |

3. PATCH ***api/input-code/***

Также позволяет отправлять и регистрировать реферальный инвайт-код другого пользователя для текущего пользователя.

Пример запроса при регистрации инвайт-кода:

`curl PATCH -d 'phone=%2B79998887766&someone_invite_code=q1w2e3' http://localhost:8001/api/invite-code/`

| Параметр строки запроса | Обязательный/Не обязательный | Описание                                                              | Тип данных |
|-------------------------|------------------------------|-----------------------------------------------------------------------|------------|
| phone                   | Обязательный                 | Телефон пользователя, <br/> Макса ввода телефона:<br/>+7 ХХХ ХХХ ХХХХ | String     |
| someone_invite_code     | Обязательный                 | 6-значный инвайт-код                                                  | String     |

### Инструкция для ввода инвайт-кода 


- Для ввода инвайт-кода, в запросе нужно передать телефон пользователя в переменной _phone_ и сам код в переменной _someone_invite_code_.

Прим. __В этом случае оба параметра являются обязательными.__

Примеры ответов:

- При успешном вводе инвайт-кода

```
{''result': 'Инвайт-код принят!'}
```

- В случае, если инвайт-код уже был введён

```
{'result': 'Вы уже вводили инвайт-код: ХХХХХХ'}
```

- В случае, если инвайт-код не существует

```
{'result': 'Инвайт-код не существует!'}
```

