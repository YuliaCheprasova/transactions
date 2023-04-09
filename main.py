import psycopg2

def show_table(name):
    """function of a request to show data from a table named as 'name' """

    print(f"\nTable {name}")
    show_table_q = f"SELECT * FROM {name};"
    cursor.execute(show_table_q)
    for tuple in cursor.fetchall():
        print(tuple)
    print("----------------------------------")
    enter = input("\nPress enter to continue, please\n")

def insert_tickets():
    """function of a request to insert data into table tickets"""

    records=[]
    while True:
        session = int(input("Enter the number of session\n"))
        seat = int(input("Enter the number of seat\n"))
        records.append((session, seat))
        switch = int(input("1. Insert another one\n2. Finish entering\n"))
        match switch:
            case 1:
                continue
            case 2:
                insert_tickets_q = "INSERT INTO tickets (session_id, seat_id) VALUES (%s, %s);"
                cursor.executemany(insert_tickets_q, records)
                connection.commit()
                print("\nValues are added in table tickets")
                enter = input("\nPress enter to continue, please\n")
                break


def insert_bookings():
    """function of a request to insert data into table bookings using transactions"""

    while True:
        # start of transaction
        date = input("Enter the date of booking in the Y-M-D H-M-S format, for example 2023-02-25 10:23:54\n")
        ticket = int(input("Enter the number of ticket\n"))
        insert_bookings_q = "INSERT INTO bookings (book_date, ticket_id) VALUES (%s, %s);"
        cursor.execute(insert_bookings_q, (date, ticket))
        find_book_id = "SELECT book_id FROM bookings WHERE ticket_id = %s"
        cursor.execute(find_book_id, (ticket, ))
        book_id = cursor.fetchone()
        update_book_id_tickets_q1 = "UPDATE tickets " \
                                    "SET book_id= %s " \
                                    "WHERE ticket_id= %s; "
        cursor.execute(update_book_id_tickets_q1, (book_id, ticket))
        # end of transaction
        connection.commit()
        print("\nValues are added in table bookings")
        switch = int(input("1. Insert another one\n2. Finish entering\n"))
        match switch:
            case 1:
                continue
            case 2:
                enter = input("\nPress enter to continue, please\n")
                break


def update_tickets():
    """function of a request to update table tickets: you can create a query that the program offers
     or you can write your own if you need something more complex"""

    switch = int(input("1. Update certain ticket\n2. Enter SQL query\n"))
    match switch:
        case 1:
            ticket = int(input("Enter ticket_id you would like to update\n"))
            switchin = int(input("What would you like to update?\n1. session_id\n2. seat_id\n3. book_id\n"))
            match switchin:
                case 1:
                    # update session_id
                    value = int(input("Enter new session_id\n"))
                    update_q = "UPDATE tickets SET session_id = %s WHERE ticket_id = %s;"
                    cursor.execute(update_q, (value, ticket))
                    connection.commit()
                case 2:
                    # update seat_id
                    value = int(input("Enter new seat_id\n"))
                    update_q = "UPDATE tickets SET seat_id = %s WHERE ticket_id = %s;"
                    cursor.execute(update_q, (value, ticket))
                    connection.commit()
                case 3:
                    # update book_id (transaction too)
                    update_b_q1 = "UPDATE bookings SET ticket_id = NULL WHERE ticket_id = %s;"
                    cursor.execute(update_b_q1, (ticket,))
                    value = int(input("Enter new book_id\n"))
                    update_t_q1 = "UPDATE tickets SET book_id = NULL WHERE book_id = %s;"
                    cursor.execute(update_t_q1, (value,))
                    update_t_q2 = "UPDATE tickets SET book_id = %s WHERE ticket_id = %s;"
                    cursor.execute(update_t_q2, (value, ticket))
                    update_b_q2 = "UPDATE bookings SET ticket_id = %s WHERE book_id = %s;"
                    cursor.execute(update_b_q2, (ticket, value))
                    connection.commit()
        case 2:
            # own query
            update_q = input()
            cursor.execute(update_q)
            connection.commit()
    print("\nTable is updated")
    enter = input("\nPress enter to continue, please\n")


def update_bookings():
    """function of a request to update table bookings using transactions: you can create a query that the program offers
    or you can write your own if you need something more complex"""

    switch = int(input("1. Update certain booking\n2. Enter SQL query\n"))
    match switch:
        case 1:
            booking = int(input("Enter book_id you would like to update\n"))
            switchin = int(input("What would you like to update?\n1. book_date\n2. ticket_id\n"))
            match switchin:
                case 1:
                    # update book_date
                    value = input("Enter new book_date in the Y-M-D H-M-S format, for example 2023-02-25 10:23:54\n")
                    update_q = "UPDATE bookings SET book_date = %s WHERE book_id = %s;"
                    cursor.execute(update_q, (value, booking))
                    connection.commit()
                case 2:
                    # update ticket_id (transaction too)
                    update_t_q1="UPDATE tickets SET book_id = NULL WHERE book_id = %s;"
                    cursor.execute(update_t_q1, (booking, ))
                    value = int(input("Enter new ticket_id\n"))
                    update_b_q1 = "UPDATE bookings SET ticket_id = NULL WHERE ticket_id = %s;"
                    cursor.execute(update_b_q1, (value, ))
                    update_b_q2 = "UPDATE bookings SET ticket_id = %s WHERE book_id = %s;"
                    cursor.execute(update_b_q2, (value, booking))
                    update_t_q2="UPDATE tickets SET book_id = %s WHERE ticket_id = %s;"
                    cursor.execute(update_t_q2, (booking, value))
                    connection.commit()
        case 2:
            # own query
            update_q = input()
            cursor.execute(update_q)
            connection.commit()
    print("\nTable is updated")
    enter = input("\nPress enter to continue, please\n")


def delete_tickets():
    """function of a request to delete data from table tickets: you can create a query that the program offers
    or you can write your own if you need something more complex"""

    switch = int(input("1. Delete certain ticket\n2. Enter SQL query\n"))
    match switch:
        case 1:
            ticket = int(input("Enter ticket_id you would like to delete\n"))
            delete_q = "DELETE FROM tickets WHERE ticket_id=%s;"
            cursor.execute(delete_q, (ticket, ))
            connection.commit()
        case 2:
            delete_q = input()
            cursor.execute(delete_q)
            connection.commit()
    print("\nTicket is deleted")
    enter = input("\nPress enter to continue, please\n")

def delete_bookings():
    """function of a request to delete data from table bookings: you can create a query that the program offers
    or you can write your own if you need something more complex"""

    switch = int(input("1. Delete certain booking\n2. Enter SQL query\n"))
    match switch:
        case 1:
            book = int(input("Enter book_id you would like to delete\n"))
            delete_q = "DELETE FROM bookings WHERE book_id=%s;"
            cursor.execute(delete_q, (book,))
            connection.commit()
        case 2:
            delete_q = input()
            cursor.execute(delete_q)
            connection.commit()
    print("\nBooking is deleted")
    enter = input("\nPress enter to continue, please\n")

# connection to an exist database
try:
    connection = psycopg2.connect(
        user="postgres",
        password="22424",
        host="127.0.0.1",
        port="5432",
        database="myfirstbase"
    )
    connection.autocommit = False
    with connection.cursor() as cursor:
        while(1):
            switch=int(input("Select case you need, write only its number:\n1. Read table tickets\n2. Read table bookings\n"
                  "3. Insert into table tickets\n4. Insert into table bookings(transaction)\n5. Update table tickets\n"
                  "6. Update table bookings\n7. Delete from tickets"
                  "\n8. Delete from bookings\n9. Exit\n"))
            match switch:
                case 1:
                    show_table("tickets")
                case 2:
                    show_table('bookings')
                case 3:
                    insert_tickets()
                case 4:
                    insert_bookings()
                case 5:
                    update_tickets()
                case 6:
                    update_bookings()
                case 7:
                    delete_tickets()
                case 8:
                    delete_bookings()
                case 9:
                    break


except Exception as _ex:
    print("Error while working with PostgreSQL: ", _ex)
    connection.rollback()
finally:
    if connection:
        connection.close()
        print("PostgreSQL connection closed")
