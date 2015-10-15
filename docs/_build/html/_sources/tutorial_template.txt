The Global Template
------------------------
The Excel Workbook has to be built in a specific way in order to allow NetScriptGen to be able to identify the data in a structured manner.
The Excel Workbook will contains:

* **A global worksheet named 'Global'**: this is the main worksheet, it contains equipments per row, and the variables per column 
* **A worksheet per feature**: this is the worksheet which contains the data of the specified feature (VLAN, VTP, Port-Channel, and so on) 
* **A set of worksheets**: they contain fixed common variables (DNS, banner, user and so on)


The variable
~~~~~~~~~~~~~~~~~~~~~~~