import psycopg2
import config

conn = psycopg2.connect(dbname='users', user='postgres', password=config.DBpassword, host='localhost') #Подключение к базе данных
cursor = (conn.cursor()) #Создание экземпляра cursor

class DB(): #Взаимодействие с базой данных
    class room(): #Взаимодейтсиве с таблицей rooms
        def finder(id):
            room = []
            try:
                cursor.execute("SELECT room_name FROM rooms WHERE creator_user_id = %s;", [id])
                for row in cursor:
                    room.append(row[0]+' ')
            except: #Если у пользователя нету персонажей
                room.append('пусто')
            return room
        def finder_with_name(name, id): #Поиск персонажей пользователя по имени персонажа
            cursor.execute("SELECT * FROM rooms WHERE room_name = %s AND creator_user_id = %s;", [name, id])
            for row in cursor:
                character = str(row)
            return character
        def finder_user_isConnectedTo(id):
            room = []
            cursor.execute("SELECT room_name FROM rooms WHERE %s = ANY(player_user_id);", [id])
            for row in cursor:
                room.append(row[0]+' ')
            return room
        def connectToRoom(roomIdAndPassword, id):
            try:
                cursor.execute("SELECT room_password, room_locked, CASE WHEN (%s = ANY(player_user_id)) THEN true ELSE false END FROM rooms WHERE rooms_id = %s;", 
                                [id, int(roomIdAndPassword.split(' ')[0])])
            except:
                return "Неверный формат ввода"
            for row in cursor:
                roomPassword = row[0]
                roomIsLocked = row[1]
                alreadyInTheRoom = row[2]
            try:
                if alreadyInTheRoom:
                    return "Вы уже находитесь в данной комнате"
                else:
                    if roomPassword == roomIdAndPassword.split(' ')[1]:
                        if roomIsLocked:
                            return "Комната закрыта"
                        else:
                            cursor.execute("UPDATE rooms SET player_user_id = array_append(player_user_id, %s) WHERE rooms_id = %s", [id, roomIdAndPassword.split(' ')[0]])
                            conn.commit()
                            return "Выполнено подключение к комнате"
                    else:
                        return "Введен неверный пароль или код комнаты"
            except:
                return "Введен неверный пароль или код комнаты"
    class character(): #Взаимодейтсиве с таблицей characters
        def finder(id): #Поиск персонажей пользователя
            character = []
            try:
                #Распаковка данных из базы данных
                cursor.execute("SELECT char_name FROM character WHERE user_id = %s;", [id])
                for row in cursor:
                    character.append(row[0]+' ')
            except: #Если у пользователя нету персонажей
                character.append('пусто')
            return character
        def finder_with_name(name, id): #Поиск персонажей пользователя по имени персонажа
            cursor.execute("SELECT * FROM character WHERE char_name = %s AND user_id = %s;", [name, id])
            for row in cursor:
                character = str(row)
            return character
        def delete_finder_with_name(name, id): #Удаление персонажа по имени персонажа
            cursor.execute("SELECT * FROM character WHERE char_name = %s AND user_id = %s;", [name, id])
            for row in cursor:
                character = str(row[2])
            cursor.execute("DELETE FROM character WHERE char_name = %s AND user_id = %s;", [name, id])
            conn.commit() #Комит в базу данных
            return character
    class hierarchy():
        def change(id, buttonHierarchy): #Изменяет в базе данных иерархию местонахождения пользователя
            cursor.execute("UPDATE users SET button_hierarchy = %s WHERE user_id = %s;", [buttonHierarchy.replace(' ', '_'), id]) #Изменяем положение пользователя в иерархии
            conn.commit() #Комит в базу данных
        def receiving(id): #Берет из базы данных иерархию местонахождения пользователя
            cursor.execute("SELECT button_hierarchy FROM users WHERE user_id = %s;", [id])
            for row in cursor:
                buttonHierarchy = str(row[0]).replace(' ', '')
            buttonHierarchy = buttonHierarchy.split(',')
            return buttonHierarchy
    class user():
        def finder(id):
            cursor.execute("SELECT exists(SELECT 1 FROM users WHERE user_id = %s);", [id]) #Проверяем нету ли id пользователя в базе данных
            return bool(cursor.fetchone()[0]) #Возвращаем результат запроса
        def register(id, username):
            cursor.execute("INSERT INTO users(user_id, username) VALUES (%s, %s);", [id, username])  #Пользователь регестрируется (автоматически)
            conn.commit() #Комит в базу данных
            return "Пользователь успешно зарегистрирован"