from cs50 import SQL
def interpolation(n):
  # accessing the database
  db = SQL("sqlite:///tables.db")
  #trying to find alpha without interpolation
  result = db.execute("SELECT alpha FROM b2 WHERE np=?;", n)
  #if not succesfull
  if not result:
    #getting two closest to input np values as 2 dicts
    more, less = db.execute("SELECT np, alpha FROM b2 ORDER BY ABS(? - np) LIMIT 2;", n)
    l_alpha = float(less.get("alpha"))
    l_np = float(less.get("np"))
    m_alpha = float(more.get("alpha"))
    m_np = float(more.get("np"))
    res_alpha = l_alpha + (n - l_np)/(m_np - l_np) * (m_alpha - l_alpha)
  else:
    res_alpha = result[0].get("alpha")
  print (res_alpha)
  
def main():
  n= int(input("N:"))
  interpolation(n)

main()