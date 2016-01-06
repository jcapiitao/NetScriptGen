NetScriptGen
=============
[![Build Status](https://travis-ci.org/JoelCapitao/NetScriptGen.svg?branch=master)](https://travis-ci.org/JoelCapitao/NetScriptGen)
[![Build status](https://ci.appveyor.com/api/projects/status/vd6tkdiwitdnlsrd?svg=true)](https://ci.appveyor.com/project/JoelCapitao/netscriptgen)
[![Coverage Status](https://coveralls.io/repos/JoelCapitao/NetScriptGen/badge.svg?branch=master&service=github)](https://coveralls.io/github/JoelCapitao/NetScriptGen?branch=master)
[![Documentation Status](https://readthedocs.org/projects/netscriptgen/badge/?version=latest)](http://readthedocs.org/docs/netscriptgen/en/latest/?badge=latest)

Overview
---------

NetScriptGen is a Python tool which generates script for network equipment. The scripts are generated from parsing an Excel Workbook and a global template.
NetScriptGen needs:

- An excel Workbook with structured network data and sub-templates
- A global template with variables to be filled in

NetScriptGen read the global template and attempt to fill out the variable by finding a relationship between the variable and the data contained into the Excel workbook. This is how a template with variable looks like:

```
hostname {{hostname}}
username {{general_data!user:name:1}} privilege 15 secret {{general_data!user:name:1}}
!
interface Vlan {{VLAN#ADMIN}}
description {{VLAN!((VLAN#ADMIN)):description}}
ip address {{VLAN!((VLAN#ADMIN)):subnet}} {{VLAN!((VLAN#ADMIN)):mask}}
no shutdown
!
!
banner motd @
{{Text:banner}}
@
end
```


What is NetScriptGen good for?
----------------------------------

Let's suppose you are working on a fresh network project and need to prepare thousand
of equipments for the access layer. After diving yourself on the design, you write
a global script that can suits for every equipments except a few values which are
specific for each equipment (hostname, VLAN IDs, VTP, SNMP and so on).
With NetScripGen, it's really easy... you transform the global script into a global
template, and put all the data within an Excel workbook and then run the process.



NetScripGen is universal
----------------------------------

All the intelligence is based on the global template and the sub-templates, NetScripGen only fill
it with the specific data provided on the Excel workbook. Therefore, NetScripGen works with all
the equipment providers as:

- Cisco (Cisco IOS, Cisco Nexus, Cisco IOS-XR, Cisco IOS-XE, Aironet OS, Cisco ASA, Cisco CatOS)
- Juniper (Junos)
- HP Switches
- Force 10 Switches
- Dell PowerConnect Switches
- Extreme Networks



NetScriptGen 0.1.0, the current version
---------------------------

The first version 0.1.0 includes:

- NetScriptGen is tested to work under python 3.x
- The Microsoft Excel spreadsheet file must use the XLSX format. This format uses the Open XML format that makes it easy for other programs, such as OpenOffice, to read XLSX files.

