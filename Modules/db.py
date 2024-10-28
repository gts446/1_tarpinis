import pyodbc

server = 'MSI\\SQLEXPRESS'
database = 'bibliotekos_programa'
username = 'gytis'
password = 'codeacademy'

class Database:
    def __init__(self):
        self.conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )
        try:
            self.connection = pyodbc.connect(self.conn_str)
            self.cursor = self.connection.cursor()
            print("Connection established successfully.")
        except pyodbc.Error as e:
            print("Failed to connect to the database:", e)
            self.connection = None
            self.cursor = None
            exit()
    
    def query(self, sql:str, params=None):
        if params is None:
            params = []
        try:
            print("#"*50)
            print("Executing SQL:", sql)
            print("With parameters:", params)
            print("#"*50)
            self.cursor.execute(sql, params)
            if sql.strip().upper().startswith("SELECT"):
                columns = [column[0] for column in self.cursor.description]
                result = self.cursor.fetchall()
                if len(result) == 0:
                    return None
                else:
                    return [dict(zip(columns,row)) for row in result]  # Fetch and return SELECT results as dictionaries
            else:
                self.connection.commit()  # Commit for INSERT, UPDATE, DELETE
                return None
        except Exception as e:
            self.connection.rollback()
            print("Error:", e)
            return None

    def close(self):
        """Closes the database connection."""
        self.cursor.close()
        self.connection.close()