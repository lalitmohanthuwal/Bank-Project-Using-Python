# Customer Details
from DB import db_query, mydb  # Add these essential imports

class Customer:
    def __init__(self, username, password, name, age, city, account_number):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__age = age
        self.__city = city
        self.__account_number = account_number

    def createuser(self):
        try:
            # Using parameterized query to prevent SQL injection
            query = """
                INSERT INTO customers 
                (username, password, name, age, city, balance, account_number, status) 
                VALUES (%s, %s, %s, %s, %s, 0, %s, 1)
            """
            values = (
                self.__username,
                self.__password,
                self.__name,
                self.__age,
                self.__city,
                self.__account_number
            )
            
            cursor = mydb.cursor()
            cursor.execute(query, values)
            mydb.commit()
            return True
        except Exception as e:
            print(f"Database error: {e}")
            mydb.rollback()
            return False