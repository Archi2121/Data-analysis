import sqlite3
import pandas as pd

df=pd.read_csv("D:\\Data analysis\\data\\titanic_cleaned.csv")
conn = sqlite3.connect(":memory:")
df.to_sql("titanic",conn,index=False, if_exists="replace")

print("data loaded into sql.now running quries...\n")

#QUERY 1: What % of men vs women survived?
query1="""SELECT sex,AVG(Survived) AS SurvivalRate from titanic 
          GROUP BY Sex"""

result1=pd.read_sql_query(query1,conn)
print("1) survival rate by sex")
print(result1,"\n")


# QUERY 2: What % survived in each passenger class (1st/2nd/3rd)?
query2 = """
SELECT Pclass, AVG(Survived) AS SurvivalRate
FROM titanic
GROUP BY Pclass
"""
result2 = pd.read_sql_query(query2, conn)
print("2) Survival Rate by Class")
print(result2, "\n")


# QUERY 3: Show me passengers who paid more than 100 in fare
# WHERE = a filter condition, just like Excel's filter
query3 = """
SELECT Sex, Pclass, Fare
FROM titanic
WHERE Fare > 100
"""
result3 = pd.read_sql_query(query3, conn)
print("3) Passengers who paid Fare > 100")
print(result3, "\n")


# QUERY 4: What's the average fare paid in each class?
query4 = """
SELECT Pclass, AVG(Fare) AS AverageFare
FROM titanic
GROUP BY Pclass
"""
result4 = pd.read_sql_query(query4, conn)
print("4) Average Fare by Class")
print(result4, "\n")

conn.close()