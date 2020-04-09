from waf.modules.sql_injection_check import sql_injection_check
from waf.modules.test import test

"""
Templates = {
    Key = path/page_url
    Value = {
            Key = form name
            Value = [functions that input a single string and return a boolean]
        }
}

Any function can be added to the template, see test.py for the most basic form
- The input will always be the value in the POST message for that particular parameter
- "" is the catch all, base security for any template-less page

"""

TEMPLATES = {
    "www/SQL/sql1.php":
        {
            "firstname": [
                sql_injection_check
            ]
        }
    ,
    "www/SQL/sql2.php":
        {
            "number": [
                # Intentionally insecure
            ]
        }
    ,
    "www/SQL/sql3.php":
        {
            "number": [
                sql_injection_check
            ]
        }
    ,
    "www/SQL/sql4.php":
        {
            "number": [
                sql_injection_check
            ]
        }
    ,
    "www/SQL/sql5.php":
        {
            "number": [
                sql_injection_check
            ]
        }
    ,
    "":
        {
            "": [
                sql_injection_check,
                test
            ]
        }
}