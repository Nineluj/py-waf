from waf.modules.sql_injection_check import sql_injection_check
from waf.modules.test import test

TEMPLATES = {
    "/www/SQL/sql1.php":
        {
            "firstname": [
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