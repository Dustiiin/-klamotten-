import subprocess
import mysql.connector
import time

# MySQL-Verbindung herstellen
cnx = mysql.connector.connect(
   user='root',
   password='KiArA2010!',
   host='localhost',
   database='aurumdev')


# Git-Befehl ausführen und Output erhalten
def get_git_log():
   git_log = subprocess.check_output(['git', 'log', '-1', '--pretty=%B'])
   return git_log.decode('utf-8').strip()

# Überprüfen, ob der Log-Eintrag bereits in der Datenbank vorhanden ist
def is_log_in_database(log):
   cursor = cnx.cursor()
   select_query = "SELECT COUNT(*) FROM changelog WHERE changelog_text = %s"
   cursor.execute(select_query, (log,))
   count = cursor.fetchone()[0]
   cursor.close()
   return count > 0

# Ausgabe in MySQL-Tabelle einfügen
def insert_into_mysql(log):
   cursor = cnx.cursor()
   insert_query = "INSERT INTO changelog (changelog_text) VALUES (%s)"
   cursor.execute(insert_query, (log,))
   cnx.commit()
   cursor.close()

# Periodisch ausführen und in MySQL einfügen
while True:
   log_text = get_git_log()
   if not is_log_in_database(log_text):
      insert_into_mysql(log_text)
   time.sleep(5)  # 5 Sekunden warten
