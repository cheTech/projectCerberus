import psycopg2


class DatabaseApi(object):

    def __init__(self, credentials):
        conn = psycopg2.connect(dbname=credentials["dbname"], user=credentials[
                                "dbuser"], password=credentials["dbpass"], host=credentials["dbhost"])  # подключаемся к базе данных
        cursor = conn.cursor()
        print("Successful DatabaseApi initialization.")

    def getNames():  # запрос
        cursor.execute("SELECT * FROM " +
                       credentials["table_name"] + " ORDER BY id")  # выполняем запрос по таблице с данными пользователей с сортировкой по идентификатору
        db = cursor.fetchall()  # парсим ответ
        listdb = [list(x) for x in db][:]  # преобразуем db в type list

        return []

    def getEncodings():
        return []
