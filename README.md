# WaterFlowCalc
#### Video Demo:  <URL HERE>
#### Description:
  My goal was to create a **command-line program** that calculates water flow for different consumers and returns the result as a table.
There could be many different water consumers in 1 building, so, the program repeatedly asks to input the info about a consumer until stopped by **EOFError**. The user should input 4-5 arguments such as:
- Item _(tells the program a type of consumer)_
- Ntot _(total number of devices that need any kind of water used by a consumer)_
- Nhot _(total numberof devices that need hot water used by a consumer)_
- U _(number of people)_ 
- Shifts _(how many shifts a day, normally 1, if not inputted)_