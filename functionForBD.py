import psycopg2

class DB(): #Взаимодействие с базой данных
    class room(): #Взаимодейтсиве с таблицей rooms
        def finder(id, cursor):
            room = []
            cursor.execute("SELECT room_name FROM rooms WHERE creator_user_id = %s;", [id])
            for row in cursor:
                room.append(row[0]+' ')
            return room
        def finder_with_name(name, id, cursor): #Поиск персонажей пользователя по имени персонажа
            cursor.execute("SELECT * FROM rooms WHERE room_name = %s AND creator_user_id = %s;", [name, id])
            character = ''
            for row in cursor:
                character = str(row)
            return character
    class character(): #Взаимодейтсиве с таблицей characters
        def finder(id, cursor): #Поиск персонажей пользователя
            character = []
            try:
                #Распаковка данных из базы данных
                cursor.execute("SELECT char_name FROM characters WHERE user_id = %s;", [id])
                for row in cursor:
                    character.append(row[0]+' ')
            except: #Если у пользователя нету персонажей
                character.append('пусто')
            return character
        def finder_with_name(name, id, cursor): #Поиск персонажей пользователя по имени персонажа
            cursor.execute("SELECT * FROM characters WHERE char_name = %s AND user_id = %s;", [name, id])
            character = ''
            for row in cursor:
                character = str(row)
            return character
        def delete_finder_with_name(name, id, cursor, conn): #Удаление персонажа по имени персонажа
            cursor.execute("SELECT * FROM characters WHERE char_name = %s AND user_id = %s;", [name, id])
            character = ''
            for row in cursor:
                character = str(row[2])
            cursor.execute("DELETE FROM characters WHERE char_name = %s AND user_id = %s;", [name, id])
            conn.commit() #Комит в базу данных
            return character
    class hierarchy():
        def changing_in_DB(id, buttonHierarchy, cursor, conn): #Изменяет в базе данных иерархию местонахождения пользователя
            buttonHierarchy.pop(len(buttonHierarchy)-1)
            buttonHierarchy = ', '.join(buttonHierarchy)
            cursor.execute("UPDATE users SET button_hierarchy = %s WHERE user_id = %s;", [buttonHierarchy, id]) #Изменяем положение пользователя в иерархии
            conn.commit() #Комит в базу данных
        def taking_from_DB(id, cursor): #Берет из базы данных иерархию местонахождения пользователя
            cursor.execute("SELECT button_hierarchy FROM users WHERE user_id = %s;", [id])
            for row in cursor:
                buttonHierarchy = str(row[0]).replace(' ', '')
            buttonHierarchy = buttonHierarchy.split(',')
            return buttonHierarchy
