import pycurl
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode


c = pycurl.Curl()
c.setopt(c.URL, 'https://localhost:9000/www/SQL/sql3.php')
fw = open(r"sql_test_results.txt", "w+")
with open('sql_test.txt') as f:
    for line in f:
        if line != "" or line != "\n":
            post_data = {'number': f'{line}', "submit": "Submit"}
            postfields = urlencode(post_data)
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(c.POSTFIELDS, postfields)
            c.perform()
            # HTTP response code, e.g. 200.
            print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
            if c.getinfo(c.RESPONSE_CODE) == 200:
                fw.write(line.strip() + " | RESULT: " + str(c.getinfo(c.RESPONSE_CODE)) + "\r\n")
            # if c.getinfo(c.RESPONSE_CODE) == 500:
            # Elapsed time for the transfer.
            print('Time: %f' % c.getinfo(c.TOTAL_TIME))

fw = open(r"sql_short_pw_results.txt", "w+")
with open('sql_short_pw.txt') as f:
    for line in f:
        if line != "" or line != "\n":
            post_data = {'number': f'{line}', "submit": "Submit"}
            postfields = urlencode(post_data)
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(c.POSTFIELDS, postfields)
            c.perform()
            # HTTP response code, e.g. 200.
            print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
            if c.getinfo(c.RESPONSE_CODE) != 200:
                fw.write(line.strip() + " | RESULT: " + str(c.getinfo(c.RESPONSE_CODE)) + "\r\n")
            # if c.getinfo(c.RESPONSE_CODE) == 500:
            #     exit(1)
            # Elapsed time for the transfer.
            print('Time: %f' % c.getinfo(c.TOTAL_TIME))
            print('Time: %s' % line)

fw = open(r"sql_test_false_positives_results.txt", "w+")
with open('sql_test_false_positives.txt') as f:
    for line in f:
        if line != "" or line != "\n":
            post_data = {'number': f'{line}', "submit": "Submit"}
            postfields = urlencode(post_data)
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(c.POSTFIELDS, postfields)
            c.perform()
            # HTTP response code, e.g. 200.
            print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
            if c.getinfo(c.RESPONSE_CODE) != 200:
                fw.write(line.strip() + " | RESULT: " + str(c.getinfo(c.RESPONSE_CODE)) + "\r\n")
            # if c.getinfo(c.RESPONSE_CODE) == 500:
            #     exit(1)
            # Elapsed time for the transfer.
            print('Time: %f' % c.getinfo(c.TOTAL_TIME))
            print('Time: %s' % line)


c.close()
