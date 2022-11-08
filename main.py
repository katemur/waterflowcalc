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
class Consumer:
	def __init__(self, item, n_tot, n_hot, u, shift):
			# item from B2 table 
		self.item = item
			#total number of devices 
		self.n_tot = n_tot
		self.n_hot = n_hot
		self.u = u
		self.shift = shift
		self.consumer, self.measure, self.tot_adv_day, self.hot_adv_day, self.tot_max_hour, self.hot_max_hour, self.tot_dev_sec, self.hot_dev_sec, self.tot_dev_hour, self.hot_dev_hour, self.hours = db.execute("SELECT * FROM a2 WHERE item = ?", item)
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
	
def main():
  n= int(input("N:"))
  interpolation(n)

main()