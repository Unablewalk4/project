import time
import mysql.connector as mcon
import re
import pandas as pd
import matplotlib.pyplot as plt
import datetime
username = ""
password = ""
my_con = None

my_con = mcon.connect(
        host='localhost',
        user='root',
        password='hello@123',
        database='hospital'
    )



mysql=my_con.cursor()

def loading():
    loadvar = 0
    movvar = ["|", "/", "-", "\\"]

    while loadvar != 15:
        print("loading please wait" + movvar[loadvar % len(movvar)], end="\r")
        time.sleep(1)
        loadvar += 1



# define a function to select a table.
def select_table():
    mysql.execute("SHOW TABLES")
    tables = mysql.fetchall()

    print("Available Tables:")
    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table[0]}")

    table_choice = int(input("Select a table (enter the number): "))

    if 1 <= table_choice <= len(tables):
        return tables[table_choice - 1][0]
    else:
        print("Invalid choice. Please select a valid table.")
        return select_table()


# define a function to show columns in a selected table.
def show_columns( table_name):
    mysql.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = mysql.fetchall()

    print(f"Columns in {table_name}:")
    for i, column in enumerate(columns, start=1):
        print(f"{i}. {column[0]}")
    clminp = input("Enter the numbers of the columns you want (comma-separated): ")
    numbers = input_str.split(',')
    number_list = []
    col_list
    for number_str in numbers:
        number = int(number_str)
        number_list.append(number)
        selected_column_names = [columns[col] for col in selected_columns]
    for i in number_list:
        [columns[col] for col in selected_columns]


# define a function to specify the WHERE condition.
def input_condition():
    condition = input("Enter the condition (e.g., 'column_name = value'): ")
    return condition



# define a function to specify the ORDER BY clause.
def input_order_direction():
    order_direction = input("Enter 'ASC' for ascending or 'DESC' for descending: ")
    order_direction = order_direction.upper()
    if order_direction not in ["ASC", "DESC"]:
        order_direction = "ASC"
    return order_direction


# define a function to perform the SELECT query.
def select_data( table_name):
    columns=show_columns( table_name)

    condition = input_condition()
    order_direction = input_order_direction()
    if condition=="" and columns=="":
        sql_query = f"SELECT * FROM {table_name} ORDER BY {order_direction};"
    elif condition=="":
        sql_query = f"SELECT {columns} FROM {table_name} ORDER BY {order_direction};"
    elif columns=="":
        sql_query = f"SELECT * FROM {table_name} WHERE {condition} ORDER BY {order_direction};"
    else:
        sql_query = f"SELECT {columns} FROM {table_name} WHERE {condition} ORDER BY {order_direction};"
    print(sql_query)

    try:
        mysql.execute(sql_query)
        result = mysql.fetchall()

        if result:
            print("Selected Data:")
            for row in result:
                print(row)
        else:
            print("No data matching the condition.")

    except mcon.Error as err:
        print(f"Error executing SELECT query: {err}")


# define a function to update data.
def update_data( table_name):
    show_columns( table_name)
    condition = input_condition()
    new_data = input("Enter the new data (e.g., 'column_name = new_value'): ")

    # Construct the SQL query
    sql_query = f"UPDATE {table_name} SET {new_data} WHERE {condition};"

    try:
        mysql.execute(sql_query)
        mysql.connection.commit()
        print("Data updated successfully.")

    except mcon.Error as err:
        print(f"Error updating data: {err}")


# define a function to delete data.
def delete_data( table_name):
    show_columns( table_name)
    condition = input_condition()

    # Construct the SQL query
    sql_query = f"DELETE FROM {table_name} WHERE {condition};"

    try:
        mysql.execute(sql_query)
        mysql.connection.commit()
        print("Data deleted successfully.")

    except mcon.Error as err:
        print(f"Error deleting data: {err}")


# define a function to create a new table.
def create_table():
    table_name = input("Enter the name of the new table: ")
    num_columns = int(input("Enter the number of columns: "))

    columns = []
    for i in range(num_columns):
        column_name = input(f"Enter name for column {i + 1}: ")
        column_type = input(f"Enter data type for column {i + 1}: ")
        columns.append(f"{column_name} {column_type}")

    # Construct the SQL query
    sql_query = f"CREATE TABLE {table_name} ({', '.join(columns)});"

    try:
        mysql.execute(sql_query)
        print(f"Table '{table_name}' created successfully.")

    except mcon.Error as err:
        print(f"Error creating table: {err}")


# define a function to delete a table.
def delete_table():
    table_name = input("Enter the name of the table to delete: ")

    # Construct the SQL query
    sql_query = f"DROP TABLE {table_name};"

    try:
        mysql.execute(sql_query)
        print(f"Table '{table_name}' deleted successfully.")

    except mcon.Error as err:
        print(f"Error deleting table: {err}")


# define a function to alter a table.
def alter_table():
    table_name = input("Enter the name of the table to alter: ")
    print("Available options for altering the table:")
    print("1. Add column")
    print("2. Modify column")
    print("3. Delete column")
    option = int(input("Enter your choice: "))

    if option == '1':
        column_name = input("Enter the name of the new column: ")
        column_type = input("Enter data type for the new column: ")

        # Construct the SQL query
        sql_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};"

    elif option == '2':
        old_column_name = input("Enter the name of the column to modify: ")
        new_column_name = input("Enter the new name for the column: ")
        new_column_type = input("Enter the new data type for the column: ")

        # Construct the SQL query
        sql_query = f"ALTER TABLE {table_name} CHANGE COLUMN {old_column_name} {new_column_name} {new_column_type};"

    elif option == '3':
        column_name = input("Enter the name of the column to delete: ")

        # Construct the SQL query
        sql_query = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"

    else:
        print("Invalid option.")
        return

    try:
        mysql.execute(sql_query)
        print(f"Table '{table_name}' altered successfully.")

    except mcon.Error as err:
        print(f"Error altering table: {err}")


def search_wildcard_in_all_tables( wildcard):
    mysql.execute("SHOW TABLES")
    tables = [table[0] for table in mysql.fetchall()]

    for table_name in tables:
        # Get a list of all columns in the table.
        mysql.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [column[0] for column in mysql.fetchall()]

        for column in columns:
            # Construct and execute a query to search for the wildcard character in the column.
            query = f"SELECT * FROM {table_name} WHERE {column} LIKE %s"
            params = (f"%{wildcard}%",)  # Add '%' before and after the wildcard character.

            mysql.execute(query, params)
            results = mysql.fetchall()

            if results:
                print(f"Table: {table_name}, Column: {column}")
                print("Matching Rows:")
                for row in results:
                    print(row)


def search_wildcard():
    wildcard = input("Enter the character you want to search for: ")

    if my_con:
        mysql = my_con.mysql()
        search_wildcard_in_all_tables( wildcard)

def ploting_func():

        print("Possible graphs:"
              "1. Comparison of prices of medicines"
              "2. Observed diseases"
              "3. Exit")
        choice = int(input("Enter your choice (1/2/3): "))

        if choice == 1:
            mysql.execute("SELECT NAME, Price FROM medication_prices")
            data = mysql.fetchall()
            if data:
                df = pd.DataFrame(data, columns=["Medication", "Price"])
                df.plot.bar(x="Medication", y="Price", title="Comparison of Medication Prices")
                plt.show()
            else:
                print("No data found for medication prices.")

        elif choice == 2:
            while True:
                lst=[]
                mysql.execute("select diseases from patients")
                y=mysql.fetchall()
                df = pd.DataFrame({"":y})
                df.columns=["diseases"]
                print(df)
                x=0
                while len(df)!=x:
                    y=df.iloc[x,0]
                    input_tuple = y
                    # Extract the string from the tuple
                    input_str = input_tuple[0]

                    # Split the string into a list of substrings using ',' as the delimiter
                    integers_as_strings = input_str.split(',')

                    # Convert each substring to an integer and print it
                    for num_str in integers_as_strings:
                        lst.append(int(num_str))
                    x += 1
                df=pd.DataFrame({"dis": lst})

                df = df['dis'].value_counts().reset_index()
                mysql.execute("SELECT scientific_name FROM disease LIMIT 10;")
                namedis=mysql.fetchall()
                # Step 8: Plot the disease names and their counts
                print(df)
                plt.bar(df['dis'],df['count'])
                plt.ylim(300)

                # Show the plot
                plt.show()
        elif choice==3:
            pass
        else:
            print("it appears the data you entered is wrong,kindly re-enter it")
# define the main function to interact with the user.
def admnpnl_func():

    while True:
        print("\nMenu:")
        print("1. View data in a table")
        print("2. Update data")
        print("3. Delete data")
        print("4. Create a new table")
        print("5. Delete a table")
        print("6. Alter a table")
        print("7. Search for wildcard character")
        print("8. Graphs")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            loading()
            table_name = select_table()
            select_data( table_name)
        elif choice == '2':
            loading()
            table_name = update_data()
            update_data( table_name)
        elif choice == '3':
            loading()
            table_name = delete_data()
            delete_data(table_name)
        elif choice == '4':
            loading()
            create_table()
        elif choice == '5':
            loading()
            delete_table()
        elif choice == '6':
            loading()
            alter_table()
        elif choice == '7':
            loading()
            search_wildcard()
        elif choice == '8':
            my_con.close()
            print("Exiting the program.")
            break
        else:
            print("it appears the data you entered is wrong,kindly re-enter it")


if __name__ == "__admnpnl_func__":
    admnpnl_func()


def doc():
    my_con = connect_to_database()

    if my_con:
        mysql = my_con.mysql()
        while True:
            print("\nMenu:")
            print("1. View data in a table")
            print("2. Update data")
            print("3. Delete data")
            print("4. Exit")

            choice = int(input("Enter your choice: "))

            if choice == '1':
                loading()
                table_name = select_table()
                select_data( table_name)
            elif choice == '2':
                loading()
                table_name = select_table()
                update_data( table_name)
            elif choice == '3':
                loading()
                table_name = select_table()
                delete_data( table_name)
            elif choice == '4':
                my_con.close()
                print("Exiting the program.")
                break
            else:
                print("it appears the data you entered is wrong,kindly re-enter it")


if __name__ == "__doc__":
    doc()




def validate_email(email):
    # A simple regular expression for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


def validate_password(password):
    # Validate password strength (e.g., minimum length)
    return len(password) >= 8


def register_user(username, password,phone):
        connect_to_database()
        mysql = mcon.cursor()

        # Check if the username (email) already exists
        mysql.execute("SELECT * FROM data WHERE username = %s", (username,))
        existing_user = mysql.fetchone()

        if existing_user:
            print("Username (email) already exists. Please choose a different one.")
        else:
            if validate_email(username) and validate_password(password):
                # Insert the new user into the database
                mysql.execute("INSERT INTO data (username, password,phone) VALUES (%s, %s,%d)", (username, password,phone))
                mcon.commit()
                print(f"User registered successfully! Welcome, {username}")
            else:
                print("Invalid email format or weak password. Please try again.")


def login_user(username, password):

        # Check if the username (email) and password match
        mysql.execute("SELECT * FROM data WHERE username = %s AND password = %s", (username, password))
        user = mysql.fetchone()

        if user:
            print(f"Welcome, {username}")
        else:
            print("Invalid username or password. Please try again.")

def login(username, password):

    if username == "":
        print("Welcome to MUHOSPITALS ,to continue kindly:")
        print("1.> sign in")
        print("2.> log in")
        print("3.>exit")
        choice = int(input(":"))
        if choice == 1 or choice==2:
            username=input("kindly enter your email id:")
            password=input("kindly enter a password")
            validate_email(username)
            validate_password(password)
            if choice==1:
                register_user(username, password)
            else:
                login_user(username, password)
        else:
            pass


def check_dis_func():
    mysql.execute("SELECT disease FROM patients WHERE id = %s", (id_,))

    # Fetch the results
    myresult = mysql.fetchall()

    # Print the diagnosed diseases and recommended medicines
    print("You have been diagnosed with the following diseases (with the names of recommended medicines):")
    for row in myresult:
        diseases = row[0].split(",")  # Split diseases if they are comma-separated
        for disease in diseases:
            disease = disease.strip()  # Remove leading/trailing spaces (like trim)
            disease_id = f"d_{disease.replace(' ', '_')}"  # Create the disease ID
            disease_id = disease_id.replace(",", "")  # Remove commas from disease ID
            # Execute a query to fetch details of the disease and recommended medicines
            mysql.execute("SELECT * FROM disease WHERE disease_id = %s", (disease_id,))
            disease_info = mysql.fetchall()

            # Print disease information
            if disease_info:
                print(f"Disease: {disease_info[0][1]}")  # f for strings and [0][1]Means first row 3rd coloumn
                print(f"Recommended Medicines: {disease_info[0][2], disease_info[0][3], disease_info[0][4]}")
                print()


# Function to display available items
def display_meds():
    mysql.execute("SELECT * FROM medication_prices")
    med = mysql.fetchall()

    print("Available medicines:")
    for item in items:
        print(f"ID: {item[3]}, Name: {item[0]}, Price: ${item[1]}, Quantity: {item[2]}")


# Function to handle the buying process
def buy_meds():
    display_items()
    mysql.execute("select uid from data where email=%s", username)
    userid = mysql.fetchall()
    item_id = int(input("Enter the ID of the med you want to buy: "))
    quantity = int(input("Enter the quantity you want to buy: "))
    dt = datetime.datetime.now()
    mysql.execute("SELECT name, price, quantity FROM medication_prices WHERE med_id = %s", (item_id,))
    item = mysql.fetchone()

    if item:
        item_name, item_price, item_quantity = item
        if item_quantity >= quantity:
            total_cost = item_price * quantity
            print(f"Item: {item_name}, Quantity: {quantity}, Total Cost: ${total_cost}")

            confirm = input("Confirm purchase (yes/no): ").strip().lower()
            if confirm == "yes":
                # Deduct the purchased quantity from the item's quantity
                mysql.execute("UPDATE medication_prices SET qty = qty - %s WHERE id = %s", (quantity, item_id))
                mysql.execute("insert into med_purchased (uid, date, med_id, qty_pur) %s,%s,%s,%s",(userid,dt,item_id,quantity))
                print("Purchase successful!")
            else:
                print("Purchase canceled.")
        else:
            print("Insufficient quantity available.")
    else:
        print("Item not found.")


def pat_func():
    my_con = connect_to_database()

    if my_con:
        mysql = my_con.mysql()
        while True:
            print("\nMenu:")
            print("1.view personal data")
            print("2.view diseases encountered by now")
            print("3.apply an appointment")
            print("4.purchase medicines")
            print("5.exit")

            choice = int(input("Enter your choice: "))
            if choice==1:
                loading()
                mysql.execute("select * from patients where email=%s",username)
            if choice == 2:
                loading()
                check_dis_func()
            if choice == 3:
                loading()
                mysql.execute("select uid from data where email=%s",username)
                userid=mysql.fetchall()
                dt = datetime.datetime.now()
                mysql.execute("insert into appointment (uid,date)",(userid,dt))
            if choice==4:
                loading()
                display_meds()
                buy_meds()
            if choice==5:
                pass
            else:
                print("it appears the data you entered is wrong,kindly re-enter it")
if __name__ == "__pat_func__":
    pat_func()
def main():
    global my_con  # Use the global my_con variable

    loading()
    login(username, password)

    # Check the user's category from the database and perform actions accordingly
    if my_con:
        mysql = my_con.cursor()
        mysql.execute("SELECT catagory FROM data WHERE email = %s", (username,))
        cat = mysql.fetchone()

        if cat and cat[0] == "admin":
            loading()
            admnpnl_func()
        elif cat and cat[0] == "doctors":
            loading()
            doc()
        elif cat and cat[0] == "user":
            loading()
            pat_func()
        else:
            print("It seems that an unexpected error has occurred. Please inform the staff about it.")

if __name__ == "__main__":
    my_con = mcon.connect(
        host='localhost',
        user='root',
        password='hello@123',
        database='hospital'
    )
    main()