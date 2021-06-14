import psycopg2
import csv
from tabulate import tabulate


def fetch_all(cursor):
    colnames = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return [
        {colname: value for colname, value in zip(colnames, record)}
        for record in records
    ]


conn = psycopg2.connect(
    "host=127.0.0.1 port=5432 dbname=odscourse user=postgres password=secret"
)
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS adult_data (
    id SERIAL PRIMARY KEY,
    age INTEGER,
    workclass VARCHAR,
    fnlwgt INTEGER,
    education VARCHAR,
    education_num INTEGER,
    marital_status VARCHAR,
    occupation VARCHAR,
    relationship VARCHAR,
    race VARCHAR,
    sex VARCHAR,
    capital_gain INTEGER,
    capital_loss INTEGER,
    hours_per_week INTEGER,
    native_country VARCHAR,
    salary VARCHAR
)
"""
cursor.execute(query)
conn.commit()
pass

with open("adult.csv", "r") as f:
    reader = csv.reader(f)
    # Skip the header row
    next(reader)
    for Id, row in enumerate(reader):
        cursor.execute(
            "INSERT INTO adult_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [Id] + row,
        )
conn.commit()


query1 = """ select sex, count(*)  from adult_data group by sex;"""
# cursor.execute(query1)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query2 = """ select avg(age)  from adult_data 
where sex = 'Female'
group by sex;"""
# cursor.execute(query2)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query3 = """select (N1::decimal/N2::decimal) as res from (select count(*) as N1 from adult_data 
where native_country = 'Germany' ) T1,
(select count(*) as N2 from adult_data ) T2;"""
# cursor.execute(query3)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query45 = """ select salary, avg(age), STDDEV(age)  from adult_data 
group by salary;"""
# cursor.execute(query45)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query6 = """select (case when 
(exists (select distinct(education) from adult_data where salary = '>50K' AND NOT (education in ('Bachelors', 
'Prof-school', 'ssoc-acdm', 'Assoc-voc', 'Masters' , 'Doctorate'))))
then False
else True
end) as my_result; """
# cursor.execute(query6)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query7 = """select  race, sex, AVG(age), max(age)  from adult_data group by race, sex order by race, sex;"""
# cursor.execute(query7)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query8 = """select N1::decimal/N2::decimal as AMONG_MARRIED, N3::decimal/N4::decimal as AMONG_SINGLE from 

(select count(*) As N1 from adult_data 
where marital_status like 'Married%' and salary='>50K' ) T1,

(select count(*)  AS N2 from adult_data where marital_status like 'Married%' ) T2,

(select count(*) As N3 from adult_data 
where marital_status not like 'Married%' and salary='>50K' ) T3,

(select count(*)  AS N4 from adult_data where marital_status not like 'Married%' ) T4
;"""
# cursor.execute(query8)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query91 = """select max(hours_per_week) from adult_data;"""
# cursor.execute(query91)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query92 = """select count(*) from adult_data
where hours_per_week = (select max(hours_per_week) from adult_data);"""
# cursor.execute(query92)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query93 = """select (N1::decimal/N2::decimal)*100 as my_result from 
(select count(*) AS N1 from adult_data where salary = '>50K' and hours_per_week = (select max(hours_per_week) from adult_data)) T1,
(select count(*) AS N2 from adult_data where  hours_per_week = (select max(hours_per_week) from adult_data)) T2;"""
# cursor.execute(query93)
# print(tabulate(fetch_all(cursor), "keys", "psql"))

query10 = """select native_country, salary, AVG(hours_per_week) from adult_data
group by native_country, salary
order by native_country, salary;"""
# cursor.execute(query10)
# print(tabulate(fetch_all(cursor), "keys", "psql"))


query_list = [
    query1,
    query2,
    query3,
    query45,
    query6,
    query7,
    query8,
    query91,
    query92,
    query93,
    query10,
]

for each_query in query_list:
    cursor.execute(each_query)
    print(tabulate(fetch_all(cursor), "keys", "psql"))
