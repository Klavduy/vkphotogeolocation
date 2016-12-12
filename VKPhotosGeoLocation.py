import vk
import time

print('Vk photos geo location')

# Авторизуем сессию с помощью access token
session = vk.Session('6320d6c84cd67fe2f4814434057aba0a2db4464a73f21c9da31cf117b8f1242c40d3e1ad888eb33d6222c')

# или с помощью id приложения и данных авторизации пользователя
# session = vk.auth_session(app_id='5772300', user_login='89381146850', user_password='klava1234xz')

# Создаем объект API
api = vk.API(session)

# Запрашиваем список всех друзей
friends = api.friends.get()

print(len(friends))
print(friends)

# Получаем список всех друзей
friends = api.friends.get()

# Получаем информацию о всех друзьях
friends_info = api.users.get(user_ids=friends)

# Выведим список друзей в удобном виде
for friend in friends_info:
    print('ID: %s Имя: %s %s' % (friend['uid'], friend['first_name'], friend['first_name']))

# Здесь будут храниться геоданные
geolocation = []

count = 0

# Получим геоданные всех фотографий каждого друга
# Цикл перебирающий всех друзей
for id in friends:
    print('Получаем данные пользователя: %s' % id)
    # Получаем все альбомы пользователя, кроме служебных
    try:
        albums = api.photos.getAlbums(owner_id=id)
        print('\t...альбом %s...' % len(albums))
        # Цикл перебирающий все альбомы пользователя
        for album in albums:
            # Обрабатываем исключения для приватных альбомов/фот
            # Получаем все фотографии из альбома
            photos = api.photos.get(owner_id=id, album_id=album['aid'])
            print('\t\t...обрабатываем фотографии альбома... ')
            # Цикл перебирающий все фото в альбоме
            for photo in photos:
                # Если в фото имеются геоданные, то добавим их в список geolocation
                if 'lat' in photo and 'long' in photo:
                    count += 1
                    geolocation.append((photo['lat'], photo['long']))
            print('\t\t...найдено %s фото...' % len(photos))
            # Задержка между запросами photo.get
        if count >=50:
            break
        time.sleep(0.5)
    except:
        pass
    # Задержка между запросами photo.getAlbums
    time.sleep(0.5)

# Здесь будет хранится сгенерированный JavaScript код
js_code = ""

# Проходим по всем геоданным и генерируем JS команду добавления маркера
for loc in geolocation:
    js_code += 'new google.maps.Marker ({position:{lat: %s,lng: %s}, map: map}); \n' % (loc[0], loc[1])

# Считываем из файла-шаблона html данные
html = open('map.html').read()
# Заменяем placeholder на сгенирированый код
html = html.replace('/* PLACEHOLDER */', js_code)

# Записываем данные в новый файл
f = open('VKPhotosGeoLocation.html', 'w')
f.write(html)
f.close()
