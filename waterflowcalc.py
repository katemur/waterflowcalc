from cs50 import SQL
import numpy as np
import pandas as pd
import pdfkit as pdf
import os, sys
db = SQL("sqlite:///tables.db")
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
   # gets alpha if the search for input NP gave only 1 result 
    res_alpha = result[0].get("alpha")
  return res_alpha
# a function for splitting the input into 5 variables and returning it as a dict
def custom_split(str):
  item, n_tot, n_hot, u, shifts = str.split(" ")
  return {"item": float(item), "n_tot": int(n_tot), "n_hot": int(n_hot), "u": int(u), "shifts": int(shifts)}
def table_pdf(df, status):
  df.to_html('f.html')
  if status == 'tot':
    output = 'table_tot.pdf'
  elif status == 'cold':
    output = 'table_cold.pdf'
  else:
    output = 'table_hot.pdf'
  pdf.from_file('f.html', output)
class Consumer:
  def __init__(self, item, n_tot, n_hot, u, shift):
    # item from a2 table
    self.item = item
    #total number of devices 
    self.n_tot = n_tot
    self.n_hot = n_hot
    self.u = u
    self.shift = shift
    #get info from the database
    res = db.execute("SELECT Consumer, measure, TotAdvDay, HotAdvDay, TotMaxHour, HotMaxHour, TotDevSec, HotDevSec, TotDevHour, HotDevHour, Hours FROM a2 WHERE item = ?", item)
    self.consumer = res[0]['consumer']
    self.measure = res[0]['measure']
    self.tot_adv_day = res[0]['TotAdvDay']
    self.hot_adv_day = res[0]['HotAdvDay']
    self.tot_max_hour = res[0]['TotMaxHour']
    self.hot_max_hour = res[0]['HotMaxHour']
    self.tot_dev_sec = res[0]['TotDevSec']
    self.hot_dev_sec = res[0]['HotDevSec']
    self.tot_dev_hour = res[0]['TotDevHour']
    self.hot_dev_hour = res[0]['HotDevHour']
    self.hours = res[0]['Hours']
    self.p_tot = self.u * self.tot_max_hour / (3600 * self.tot_dev_sec * self.n_tot)
    self.p_hot = self.u * self.hot_max_hour / (3600 * self.hot_dev_sec * self.n_hot)
    self.p_cold =  self.u * (self.tot_max_hour - self.hot_max_hour) / (3600 * self.hot_dev_sec * self.n_tot)
    self.np_tot = self.p_tot * self.n_tot
    self.np_hot = self.p_hot * self.n_hot
    self.np_cold = self.p_cold * self.n_tot
    self.alpha_tot = interpolation(self.np_tot)
    self.alpha_hot = interpolation(self.np_hot)
    self.alpha_cold = interpolation(self.np_cold)	
    self.q_sec_tot = 5 * self.alpha_tot * self.tot_dev_sec
    self.q_sec_hot = 5 * self.alpha_hot * self.hot_dev_sec
    self.q_sec_cold = 5 * self.alpha_cold * self.hot_dev_sec
    self.p_tot_hr = 3600 * self.tot_dev_sec * self.p_tot/self.tot_dev_hour
    self.p_hot_hr = 3600 * self.hot_dev_sec * self.p_hot/self.hot_dev_hour
    self.p_cold_hr = 3600 * self.hot_dev_sec * self.p_cold/self.hot_dev_hour
    self.np_tot_hr = self.p_tot_hr * self.n_tot
    self.np_hot_hr = self.p_hot_hr * self.n_hot
    self.np_cold_hr = self.p_cold_hr * self.n_tot
    self.alpha_tot_hr = interpolation(self.np_tot_hr)
    self.alpha_hot_hr = interpolation(self.np_hot_hr)
    self.alpha_cold_hr = interpolation(self.np_cold_hr)
    self.q_hr_tot = 0.005 * self.alpha_tot_hr * self.tot_dev_hour
    self.q_hr_hot = 0.005 * self.alpha_hot_hr * self.hot_dev_hour
    self.q_hr_cold = 0.005 * self.alpha_cold_hr * self.hot_dev_hour
    self.q_day_tot = self.u * self.tot_adv_day /1000 
    self.q_day_hot = self.u * self.hot_adv_day / 1000 
    self.q_day_cold = self.u *(self.tot_adv_day - self.hot_adv_day) / 1000 
    self.q_hr_mid_tot = self.q_day_tot / (shift * self.hours)
    self.q_hr_mid_hot = self.q_day_hot / (shift * self.hours)
    self.q_hr_mid_cold = self.q_day_cold / (shift * self.hours)
  def __str__(self):
    return f'total \n U: {self.u} N tot: {self.n_tot} P tot: {self.p_tot} alpha tot: {self.alpha_tot} q sec tot: {self.q_sec_tot} \n P tot hr:{self.p_tot_hr} alpha tot hr: {self.alpha_tot_hr} q hr tot: {self.q_hr_tot} \n q day tot: {self.q_day_tot} hours: {self.hours}'
def main():  
  input_info = []
  print("Usage: Item Ntot Nhot U Shifts")
  #getting user's input until he enters an empty line
  while True:
    inp = input("Consumer: ")
    if inp == "":
      break
    #checking for correct number and type of arguments
    try:
      split_inp = custom_split(inp)
    except ValueError:
      sys.exit("Incorrect arguments")
      break
    # checking if the user gave an item that exists in a2 table
    item_check = db.execute("SELECT * FROM a2 WHERE item = ?", split_inp.get("item"))
    if not item_check:
      sys.exit("Incorrect item")
    # add 1 input to a list of inputs
    input_info.append(inp)
  #  create a list of Consumer objects
  consumers = []
  # creating objects using input info and adding them to a list
  for cons in input_info:
    res = custom_split(cons)
    item = res.get("item")
    n_tot = res.get("n_tot")
    n_hot = res.get("n_hot")
    u = res.get("u")
    shifts = res.get("shifts")
    consumers.append(Consumer(item, n_tot, n_hot, u, shifts))
  # creating lists if all data to export
  item_res=[]
  u_res = []
  n_tot_res = []
  alpha_tot_res = []
  q_sec_tot_res = []
  p_tot_hr_res = []
  alpha_tot_hr_res = []
  q_hr_tot_res = []
  q_day_tot_res = []
  n_hot_res = []
  alpha_hot_res = []
  q_sec_hot_res = []
  p_hot_hr_res = []
  alpha_hot_hr_res = []
  q_hr_hot_res = []
  q_day_hot_res = []
  alpha_cold_res = []
  q_sec_cold_res = []
  p_cold_hr_res = []
  alpha_cold_hr_res = []
  q_hr_cold_res = []
  q_day_cold_res = []
  for i in range(len(consumers)):
    item_res.append(consumers[i].item)
    u_res.append(consumers[i].u)
    n_tot_res.append(consumers[i].n_tot)
    alpha_tot_res.append(consumers[i].alpha_tot)
    q_sec_tot_res.append(consumers[i].q_sec_tot)
    p_tot_hr_res.append(consumers[i].p_tot_hr)
    alpha_tot_hr_res.append(consumers[i].alpha_tot_hr)
    q_hr_tot_res.append(consumers[i].q_hr_tot)
    q_day_tot_res.append(consumers[i].q_day_tot)
    n_hot_res.append(consumers[i].n_hot)
    alpha_hot_res.append(consumers[i].alpha_hot)
    q_sec_hot_res.append(consumers[i].q_sec_hot)
    p_hot_hr_res.append(consumers[i].p_hot_hr)
    alpha_hot_hr_res.append(consumers[i].alpha_hot_hr)
    q_hr_hot_res.append(consumers[i].q_hr_hot)
    q_day_hot_res.append(consumers[i].q_day_hot)
    alpha_cold_res.append(consumers[i].alpha_cold)
    q_sec_cold_res.append(consumers[i].q_sec_cold)
    p_cold_hr_res.append(consumers[i].p_cold_hr)
    alpha_cold_hr_res.append(consumers[i].alpha_cold_hr)
    q_hr_cold_res.append(consumers[i].q_hr_cold)
    q_day_cold_res.append(consumers[i].q_day_cold)
  # creating a resulting dataframe
  df_hot = pd.DataFrame.from_dict(dict([("Item", item_res), ("U", u_res), ("N", n_hot_res), ("alpha", alpha_hot_res), ("Q sec", q_sec_hot_res), ("P hr", p_hot_hr_res), ("alpha hr", alpha_hot_hr_res), ("Q hr", q_hr_hot_res), ("Q day", q_day_hot_res)]))
  table_pdf(df_hot, "hot")
  df_tot = pd.DataFrame.from_dict(dict([("Item", item_res), ("U", u_res), ("N", n_tot_res), ("alpha", alpha_tot_res), ("Q sec", q_sec_tot_res), ("P hr", p_tot_hr_res), ("alpha hr", alpha_tot_hr_res), ("Q hr", q_hr_tot_res), ("Q day", q_day_tot_res)]))
  table_pdf(df_tot, "tot")
  
  df_cold = pd.DataFrame.from_dict(dict([("Item", item_res), ("U", u_res), ("N", n_tot_res), ("alpha", alpha_cold_res), ("Q sec", q_sec_cold_res), ("P hr", p_cold_hr_res), ("alpha hr", alpha_cold_hr_res), ("Q hr", q_hr_cold_res), ("Q day", q_day_cold_res)]))
  table_pdf(df_cold, "cold")
      
if __name__== "__main__":
  main()