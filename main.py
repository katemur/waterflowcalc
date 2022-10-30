from lib2to3.pgen2.token import LESS
from cs50 import SQL
def interpolation(n):
  # accessing the database
  db = SQL("sqlite:///tables.db")
  #trying to find alpha without interpolation
  result = db.execute("SELECT alpha FROM b2 WHERE np=?;", n)
  #if not succesfull
  if not result:
    #getting two closest to input np values as 2 dicts
    clo_1st, clo_2nd  = db.execute("SELECT np, alpha FROM b2 ORDER BY ABS(? - np) LIMIT 2;", n)
    if clo_1st.get("np") < clo_2nd.get("np"):
        less = clo_1st
        more = clo_2nd
    else:
        less = clo_2nd
        more = clo_1st
    l_alpha = float(less.get("alpha"))
    l_np = float(less.get("np"))
    m_alpha = float(more.get("alpha"))
    m_np = float(more.get("np"))
    res_alpha = round(l_alpha + (n - l_np)/(m_np - l_np) * (m_alpha - l_alpha), 3)
  else:
    res_alpha = result[0].get("alpha")
  print (res_alpha)
  
def main():
  n= int(input("N:"))
  interpolation(n)

main()