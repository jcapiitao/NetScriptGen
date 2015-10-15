================================================
NetScriptGen Tutorial
================================================

In this tutorial, we will decribe first how to store the data in an Excel Workbook, and secondly, how to write the template.
Finally, you will find some practical examples for more understanding.

The Excel Workbook
------------------------
The Excel Workbook has to be built in a specific way in order to allow NetScriptGen to be able to identify the data in a structured manner.
The Excel Workbook will contains:

* A global sheet named 'Global': this is the main sheet, it contains equipments per row, and the features per column 
* A sheet per feature: this is the sheet which contains the data of the specified feature (VLAN, VTP, DNS, and so on) 


.. note:: The Excel workbook must contain a least the global sheet named as ``Global``, otherwise NetScriptGen will throw an error.

test

The global sheet
~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: _static/global_sheet.png
   :width: 600px
   :alt: global sheet overview
   :align: left

   Figure 1, An Example of a global sheet

As you can see above, each line is an equipment. Each of these equipments will have a configuration different from one another based on the values of the features.

