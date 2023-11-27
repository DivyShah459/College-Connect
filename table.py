import psycopg2


conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
cur = conn.cursor()


#cur.execute("CREATE TABLE MyColleges (College_Name text, State text, ACT_Avg int, SAT_Avg int, Enrollment int, Acceptance_Rate int, Cost int, Percent_Receiving_Aid int, National_Rank int, HS_Gpa float, Institutional_Control text )")
#cur.execute("INSERT INTO MyColleges VALUES ('college2', 'college2', 1, 2, 3, 4, 5, 6, 7, 8, 'testing2')")

cur.close()
conn.commit()


with conn.cursor() as cursor:
   cursor.execute("SELECT * from Colleges")
   for record in cursor:
       print(record)

conn.close()
