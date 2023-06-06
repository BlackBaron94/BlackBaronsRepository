import sqlite3
from sqlite3 import Error
import datetime
import random

today = datetime.date.today()
today_string = "{0}/{1}/{2}".format(today.day, today.month, today.year)


class Challenge:
    def __init__(self, player1, player2, accept=False):
        self.player1 = player1
        self.player2 = player2
        self.accept = accept
        Challenge.requirements(self)

    def requirements(self):
        # Έλεγχος αν υπάρχουν τα ονόματα στο ranking
        if empty_check(self.player1):
            print(f"Δεν υπάρχει παίκτης στη θέση #{self.player1}")
            return
        elif empty_check(self.player2):
            print(f"Δεν υπάρχει παίκτης στη θέση #{self.player2}")

        # Υπολογισμός της διαφοράς των θέσεων που μπορεί να γίνει μια πρόκληση. Συγκεκριμένα για τις θέσεις 1 - 9
        # η διαφορά μπορεί να είναι μέχρι 3 θέσεις, ενώ για τις θέσεις απο 9 - ...  μέχρι 4 θέσεις.
        k5 = 4 if self.player1 > 9 else 3  # Αντί για   if player1 <= 9 ....

        if self.player1 - self.player2 > k5:
            print(f"Ο παίκτης που προκαλείται βρίσκεται {k5} θέσεις πάνω από τον παίκτη που προκαλεί."
                  f" Η πρόκληση είναι άκυρη.")
        elif self.player1 - self.player2 < 0:
            print(f"Ο παίκτης που προκαλείται είναι κάτω από τον παίκτη που προκαλεί. Η πρόκληση είναι άκυρη.")
        elif self.player1 == self.player2:
            print("Λάθος καταχώρηση.")
            return exit

        print("Η πρόκληση είναι αποδεκτή.")
        answer = input(f"Νίκησε ο παίκτης στη θέση #{self.player1} που έκανε την πρόκληση;").upper()

        while answer not in ('ΝΑΙ', 'ΟΧΙ'):
            answer = input(f"Νίκησε ο παίκτης στη θέση #{self.player1} που έκανε την πρόκληση; "
                           f"Παρακαλώ απαντήστε 'Ναί' ή 'Όχι'. ").upper()

        if answer == 'ΝΑΙ':
            win(self.player1, self.player2)
        if answer == 'ΟΧΙ':
            print("Καμία αλλαγή στην κατάταξη.")


def dbconnect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


# Δημιουργία ΔΒ + Πίνακα
def create_table():
    # Δημιουργία πίνακα με Position, Name, Surname, Wins, Loses, Control_Date όπου Control_Date τελευταία μέρα
    # που έπαιξε αγώνα, ημέρα ένταξης στο club ή τελευταία φορά που υπέστη decay. Position = Primary key
    my_conn = dbconnect('tennis_club.db')  # Δημιουργεί ΔΒ
    # my_conn = dbconnect(':memory:')
    sql_query = "CREATE TABLE IF NOT EXISTS ranking (Position INTEGER PRIMARY KEY, Name VARCHAR(128)," \
                " Surname VARCHAR(128), Wins INTEGER, Loses INTEGER, Control_Date TEXT);"
    c = my_conn.cursor()

    c.execute(sql_query)  # Δημιουργία Πίνακα με τη Θέση ως Primary Key
    my_conn.commit()
    my_conn.close()


# Αρχικοποίηση κατάταξης
def initialization(players, today_string=today_string):
    # Δέχεται λίστα με όνομα και επίθετο χωρισμένα με κενό και την εκχωρεί στον πίνακα
    random.shuffle(players)
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    for i, player in enumerate(players):
        entry = (i + 1, players[i][0], players[i][1], 0, 0, today_string)
        c.execute("INSERT INTO ranking VALUES {0}".format(entry))
    my_conn.commit()
    my_conn.close()
    print('Οι παίκτες καταχωρήθηκαν τυχαία στην κατάταξη.')


# Δημιουργία τυχαίας κατάταξης για δοκιμές
def test():
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    c.execute("INSERT INTO ranking VALUES ('1', 'Κώστας', 'Παπαδόπουλος', '5', '1', '27/2/2023');")
    c.execute("INSERT INTO ranking VALUES ('2', 'Γιάννης', 'Ιωάννου', '4', '2', '21/5/2023');")
    c.execute("INSERT INTO ranking VALUES ('3', 'Γιώργος', 'Θεοδώρου', '3', '1', '14/5/2023');")
    c.execute("INSERT INTO ranking VALUES ('4', 'Νίκος', 'Παπαδημητρίου', '3', '2', '24/4/2023');")
    c.execute("INSERT INTO ranking VALUES ('5', 'Αντώνης', 'Διαμαντής', '3', '2', '12/4/2023');")
    c.execute("INSERT INTO ranking VALUES ('6', 'Χρήστος', 'Χατζής', '3', '3', '21/4/2023');")
    c.execute("INSERT INTO ranking VALUES ('7', 'Βλαδίμιρος', 'Δεβεροβοριάς', '2', '3', '31/1/2023');")
    c.execute("INSERT INTO ranking VALUES ('8', 'Δημήτρης', 'Ανδρεάδης', '2', '3', '29/5/2023');")
    c.execute("INSERT INTO ranking VALUES ('9', 'Λουκάς', 'Παπακώστας', '2', '3', '1/5/2023');")
    c.execute("INSERT INTO ranking VALUES ('10', 'Ισίδωρος', 'Μπίκος', '2', '3', '2/5/2023');")
    c.execute("INSERT INTO ranking VALUES ('11', 'Τρύφωνας', 'Χατζησάββας', '2', '4', '9/5/2023');")
    c.execute("INSERT INTO ranking VALUES ('12', 'Ανδρέας', 'Τσίνιος', '2', '4', '1/5/2023');")
    c.execute("INSERT INTO ranking VALUES ('13', 'Περικλής', 'Αυλωνίτης', '1', '3', '2/5/2023');")
    c.execute("INSERT INTO ranking VALUES ('14', 'Χαράλαμπος', 'Φωτιάδης', '1', '2', '7/5/2023');")
    c.execute("INSERT INTO ranking VALUES ('15', 'Φώτης', 'Χαραλαμπίδης', '0', '3', '2/4/2023');")
    my_conn.commit()
    my_conn.close()
    print('Δημιουργήθηκε τυχαία κατάταξη επιτυχώς.')


# Τύπωση ranking σε μορφή tuples
def print_ranking():
    # Raw SQL Printing
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    result = c.execute("SELECT * FROM ranking;")
    for rec in result.fetchall():
        print(rec)
    my_conn.close()


# Print όλη την κατάταξη
def print_():
    if empty_check(1):
        print('Η κατάταξη δεν περιέχει παίκτες!')
    else:
        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()
        print("{:<7}  {:<13}   {:<23}  {:<7}  {:<7}".format('Θέση', 'Όνομα', 'Επίθετο', 'Νίκες', 'Ήττες'))
        print('*' * 64)
        result = c.execute("SELECT * FROM ranking;")

        for rec in result.fetchall():
            print("{:<7}  {:<13}   {:<23}  {:<7}  {:<7}".format(*rec))  # *rec αντί για ξεχωριστό indexing
        print('*' * 64)
        my_conn.close()


# Εισαγωγή παίκτη στο τέλος της κατάταξης, προεπιλεγμένες τιμές για Wins & Loses = 0,
# Control_Date σήμερα ως ημέρα ένταξης

def insert_bottom(name='', surname='', wins=0, loses=0, Control_Date=today_string):
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    flag = empty_check(1)
    # Καταχώρηση νέας τελευταίας θέσης
    new_last_place = 1 if flag else c.execute("SELECT Position FROM ranking;").fetchall()[-1][0] + 1

    entry = (new_last_place, name, surname, wins, loses, today_string) # Πλειάδα στοιχείων παίκτη
    c.execute("INSERT INTO ranking VALUES (?);", entry) # Εκχώρηση παίκτη σε αυτή τη θέση
    print(f'Ο {name} {surname} τοποθετήθηκε στη θέση #{new_last_place}')

    my_conn.commit()
    my_conn.close()


# Εισαγωγή παίκτη σε επιλεγμένη θέση στην κατάταξη, προεπιλεγμένες τιμές για Wins & Loses = 0
def insert_place(rank, name='', surname='', wins=0, loses=0, Control_Date=today_string):
    # Προσπάθεια εισαγωγής παίκτη σε θέση πάνω από την οποία δεν υπάρχει άλλος παίκτης
    if empty_check(rank - 1) and rank != 1:
        print(f"Δεν υπάρχει άλλος παίκτης πριν τη θέση που προσπαθείτε να καταχωρήσετε τον παίκτη {name} {surname}.")
    else:
        if not empty_check(1):  # Αν η λίστα έχει παίκτες
            my_conn = dbconnect('tennis_club.db')
            c = my_conn.cursor()

            # Query για να πάρουμε την τελευταία θέση απο τον πίνακα της κατάταξης σε φθίνουσα σειρά
            # περιορίζοντας τα αποτελέσματα σε 1 σειρά
            last_place = c.execute("SELECT Position FROM ranking ORDER BY Position DESC LIMIT 1;").fetchone()[0]
            my_conn.close()

            update_positions_down(rank, last_place)

        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        info = (rank, name, surname, wins, loses, today_string)
        # Εισαγωγή στην κατάταξη είτε η λίστα έχει παίκτες, είτε δεν έχει και ο χρήστης διάλεξε θέση 1
        c.execute("INSERT INTO ranking VALUES (?);", info)
        print(f'Ο παίκτης {name} {surname} τοποθετήθηκε επιτυχώς στη θέση #{rank} με {wins} νίκες και {loses} ήττες.')

        my_conn.commit()
        my_conn.close()


# Διαγράφει τον παίκτη στη θέση που δίνεται από το index και μετακινεί τους κατώτερους παίκτες μία θέση πάνω,
# καλύπτοντας το κενό που δημιουργείται
def delete_player(index):
    if empty_check(index):  # Έλεγχος αν η θέση περιέχει άτομο
        print(f"Δεν υπάρχει παίκτης στη θέση που προσπαθείτε να κάνετε διαγραφή.")
    else:
        my_conn = dbconnect('tennis_club.db')
        c = my_conn.cursor()

        c.execute("DELETE FROM ranking WHERE Position=?;", (index,))  # Διαγραφή παίκτη
        c.execute("UPDATE ranking SET Position = Position - 1 WHERE Position > ?;", (index,))  # Ανανέωση λίστας

        my_conn.commit()
        my_conn.close()

        print(f'Ο παίκτης στη θέση #{index} διαγράφηκε επιτυχώς.')


# Καταγραφή νίκης με παραμέτρους τις θέσεις τους ΠΡΙΝ την αλλαγή κατάταξης
def win(winner_index, loser_index):
    """ Εισάγετε την έως τώρα θέση νικητή και μετά ηττημένου. Ο νικητής θα λάβει τη θέση του ηττημένου.
     Ο ηττημένος και όλοι οι παίκτες μεταξύ των δύο θέσεων θα μετακινηθούν μία θέση κάτω."""
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    # +1 Wins σε νικητή και ανανέωση Control_Date ως ημέρα παιχνιδιού
    c.execute("UPDATE ranking SET Wins = Wins + 1, Control_Date = ? WHERE Position = ?;", (today_string, winner_index))
    # +1 Loses σε ηττημένο και ανανέωση Control_Date ως ημέρα παιχνιδιού
    c.execute("UPDATE ranking SET Loses = Loses + 1, Control_Date = ? WHERE Position = ?;", (today_string, loser_index))

    sql_query = "SELECT * FROM Ranking WHERE Position= ?;".format(winner_index)  # Προσωρινή αποθήκευση νικητή
    x = c.execute(sql_query, (winner_index,))
    y = x.fetchall()  # Επιστρέφει λίστα, με το y[0] να είναι πλειάδα στοιχείων του νικητή

    ############
    # c.execute("DELETE FROM ranking WHERE Position = ?;", (winner_index,))  # Διαγραφή νικητή από προηγούμενη θέση

    entry = (loser_index, y[0][1], y[0][2], y[0][3], y[0][4], y[0][5])  # Νέα πλειάδα για αλλαγή "Position"

    my_conn.commit()
    my_conn.close()

    # Κλήση συνάρτησης ανακατάταξης που κατεβάζει τους παίκτες κατά μία θέση
    # από το winner_index μέχρι ΚΑΙ το loser_index

    ###########
    # update_positions_down(loser_index, winner_index)

    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    # Εισαγωγή νικητή στη θέση ηττημένου

    ###########
    # c.execute("INSERT INTO ranking(Position, Name, Surname, Wins, Loses, Control_Date) VALUES {0};".format(entry))

    my_conn.commit()
    my_conn.close()

    print('Το παιχνίδι καταγράφηκε επιτυχώς και η κατάταξη ανανεώθηκε!')


# Μεταθέτει όλα τα Positions κατά ένα κάτω αρχίζοντας από το big_num --> big_num+1 μέχρι ΚΑΙ το small_num-->small_num+1
def update_positions_down(small_num, big_num):
    """ Μετακινεί όλες τις Positions κατά μία κάτω αρχίζοντας από το big_num.
     Προεπιλογή big_num (αν δεν υπάρχει κενό) πρέπει να είναι η τελευταία θέση.
     Το small_num θα είναι το Position που θα είναι κενό μετά την κλήση. """
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    counter = big_num + 1  # Μετρητής τιμής Position που θέλουμε να θέσουμε
    # Πρώτα το big_num γίνεται big_num+1 για να μην έχουμε σύγκρουση Primal Keys
    for p in range(big_num, small_num - 1, -1):
        # Το p είναι μετρητής τρέχουσας θέσης για το WHERE και μειώνεται σε κάθε loop
        c.execute('UPDATE ranking SET Position = {0} WHERE Position={1}'.format(counter, p))
        counter -= 1  # Μείωση counter για σωστή εισαγωγή Position

    my_conn.commit()
    my_conn.close()


# Μεταθέτει τον παίκτη που υπόκειται σε decay λόγω αδράνειας μία θέση κάτω ανεβάζοντας τον κάτω στη θέση του
def rank_decay(index, today_string=today_string):
    """ Ο παίκτης της θέσης index πέφτει μία θέση λόγω αδράνειας και ο κάτω του ανεβαίνει στη θέση του."""
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()

    x = c.execute("SELECT Position FROM ranking;")
    last_place = x.fetchall()[-1][0]  # λήψη τελευταίας θέσης

    # Η Control Date ανανεώνεται ως τελευταία ημέρα τροποποίησης ώστε να μην υπόκειται σε decay ξανά πχ αύριο
    x = c.execute("SELECT * FROM ranking WHERE Position = ?;", (index,))
    inactive_player = x.fetchall()  # Αποθήκευση στοιχείων του παίκτη που υπόκειται σε rank decay

    if last_place == inactive_player[0][0]:  # Έλεγχος για την περίπτωση που ο παίκτης είναι τελευταίος
        print("Ο παίκτης {0} {1} είναι ήδη στην τελευταία θέση και δεν πέφτει περαιτέρω.".format(
            inactive_player[0][1], inactive_player[0][2]))
        c.execute("UPDATE ranking SET Control_Date = ? WHERE Position = ?;", (today_string, index))

    if last_place != inactive_player[0][0]:
        c.execute("DELETE FROM ranking WHERE Position = ?;", (index,))  # Διαγραφή του παίκτη
        # Μετακίνηση του κάτω παίκτη στην πλέον κενή θέση
        c.execute("UPDATE ranking SET Position = ? WHERE Position = ?;", (index, index + 1))
        entry = (
            inactive_player[0][0] + 1, inactive_player[0][1], inactive_player[0][2], inactive_player[0][3],
            inactive_player[0][4], today_string)
        # Εισαγωγή decaying παίκτη στην πλέον κενή θέση του από κάτω παίκτη
        c.execute("INSERT INTO ranking VALUES (?);", (entry,))

    my_conn.commit()
    my_conn.close()


# Απαραίτητο για τις υπόλοιπες εσωτερικές λειτουργίες συναρτήσεων
def empty_check(index):
    """Ελέγχει αν ο πίνακας έχει παίκτη στη θέση που καταχωρείται και επιστρέφει μια μεταβλητή τύπου bool"""
    my_conn = dbconnect('tennis_club.db')
    c = my_conn.cursor()
    c.execute("SELECT Position FROM ranking WHERE Position = ?;", (index,))
    empty_check = c.fetchall()
    flag = len(empty_check) == 0
    my_conn.close()
    return flag


# Quick create_dump_print
def go():
    """Calls create table, dump info, print"""
    test()
    print_()


def check_ranking_for_decay(today=today):
    """Ελέγχει αν υπάρχουν παίκτες που υπόκεινται σε decay στην κατάταξη"""
    conn = dbconnect('tennis_club.db')
    cursor = conn.cursor()

    decay_list = []  # Λίστα με παίκτες που θα υποστούν decay
    cursor.execute("SELECT Position, Control_Date FROM ranking;")
    ranking = cursor.fetchall()

    for index, date in ranking:
        x = date.split(sep='/')  # Διαχωρίζει το string
        last_play_date = datetime.date(int(x[2]), int(x[1]), int(x[0]))  # Μετατροπή του string σε datetime object
        days_since_last_play = (today - last_play_date).days
        if days_since_last_play > 30:
            decay_list.append(index)

    conn.commit()
    conn.close()

    if decay_list:
        print('Οι παίκτες', decay_list, 'έπεσαν μία θέση λόγω αδράνειας και η κατάταξη ανανεώθηκε.')
        print(f"Οι παίκτες {decay_list}, έπεσαν μία θέση λόγω αδράνειας και η κατάταξη ανανεώθηκε.")
        for i in decay_list[::-1]:
            rank_decay(i)
    else:
        print("Δεν υπάρχει κανένας παίκτης που να υπόκειται σε μείωση θέσης λόγω αδράνειας.")


# Main Menu
while True:
    create_table()
    print("-" * 20)
    print("1. Αρχικοποίηση κατάταξης")
    print("2. Προσθήκη παίκτη")
    print("3. Αφαίρεση παίκτη")
    print("4. Έλεγχος και καταγραφή αποτελέσματος πρόκλησης")
    print("5. Έλεγχος κατάταξης για αδρανείς παίκτες")
    print("6. Εμφάνιση κατάταξης")
    print("7. Έξοδος")
    print("0. Δημιουργία table για δοκιμές")
    print("-" * 20)
    try:
        choice = int(input("Δώστε την επιλογή σας: "))

        if choice == 1:
            flag = empty_check(1)
            if not flag:
                print("Ο πίνακας κατάταξης περιέχει ήδη παίκτες και δεν μπορεί να αρχικοποιηθεί τυχαία. "
                      "Παρακαλώ, διαγράψτε όλους τους παίκτες ή προσθέστε παίκτες "
                      "χρησιμοποιώντας κάποια από τις επιλογές.")
                continue

            players = []
            while True:
                x = input("Δώστε όνομα και επίθετο παίκτη που θέλετε να εισάγετε ή 0 για τερματισμό: ")
                if x == '0':
                    break

                player = x.split(sep=' ')
                if len(player) != 2:
                    print("Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό.")
                    continue

                players.append(player)

            if players:
                initialization(players)
            else:
                print("Δε δημιουργήθηκε κατάταξη καθώς δεν εισάγατε ονόματα.")

        elif choice == 2:
            answer = input("Θέλετε να εισάγετε τον παίκτη σε συγκεκριμένη θέση; ").upper()
            while answer not in ('ΝΑΙ', 'ΟΧΙ'):
                answer = input("Παρακαλώ απαντήστε με Ναι ή Όχι. "
                               "Θέλετε να εισάγετε τον παίκτη σε συγκεκριμένη θέση; ").upper()

            while True:
                x = input("Δώστε όνομα και επίθετο παίκτη που θέλετε να εισάγετε: ")
                player = x.split(sep=' ')
                if len(player) != 2:
                    print("Παρακαλώ εισάγετε όνομα και επίθετο χωρισμένα με ένα κενό.")
                    continue
                break

            name, surname = player[0], player[1]
            if answer == 'ΝΑΙ':
                try:
                    rank = int(input("Δώστε τη θέση κατάταξης του παίκτη που θέλετε να προσθέσετε: "))
                    insert_place(rank, name, surname)
                except ValueError:
                    print("Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.")
            elif answer == 'ΟΧΙ':
                insert_bottom(name, surname)

        elif choice == 3:
            try:
                index = int(input("Δώστε τη θέση κατάταξης του παίκτη που θέλετε να αφαιρέσετε: "))
                delete_player(index)
            except ValueError:
                print("Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.")

        elif choice == 4:
            try:
                p1 = int(input("Δώστε τη θέση κατάταξης του παίκτη που προκαλεί: "))
                p2 = int(input("Δώστε τη θέση κατάταξης του παίκτη που προκαλείται: "))
                p = Challenge(p1, p2)
            except ValueError:
                print("Παρακαλώ, εισάγετε ακέραιο αριθμό για τη θέση κατάταξης.")

        elif choice == 5:
            check_ranking_for_decay()

        elif choice == 6:
            print_()

        elif choice == 7:
            break

        elif choice == 0:
            go()

        else:
            print("Λάθος επιλογή. Παρακαλώ επιλέξτε από το μενού (1-5)")

    except ValueError:
        print("Παρακαλώ εισάγετε μόνο ακεραίους (από το 1-5)")
