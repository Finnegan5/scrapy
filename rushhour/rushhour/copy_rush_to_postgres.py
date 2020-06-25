import psycopg2

connection = psycopg2.connect(user="ngdtmjgwzsnfjz",
                              password="b5a3543cbd153c8b7af3943b27d28010d127d6c7b1a9c863e773ae8932cbe8b5",
                              host="ec2-54-247-79-178.eu-west-1.compute.amazonaws.com",
                              port="5432",
                              database="ddb39dfrett3dc")

cursor = connection.cursor()
copy_sql = """
           COPY rushhour_records("artist", "title", "price", "label", "release", "created_at", "updated_at") FROM stdin WITH CSV HEADER
           DELIMITER as ','
           QUOTE as '"'
           """
with open('rushhour_out.csv', 'r') as f:
    next(f) # Skip the header row.
    cursor.copy_expert(sql=copy_sql, file=f)

connection.commit()
cursor.close()
