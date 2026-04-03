import urllib.request, urllib.parse, http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Login
try:
    data = urllib.parse.urlencode({'password':'admin123'}).encode('utf-8')
    opener.open('http://127.0.0.1:5002/admin/login', data=data)
    resp = opener.open('http://127.0.0.1:5002/')
    print("SUCCESS")
except urllib.error.HTTPError as e:
    content = e.read().decode('utf-8')
    import re
    match = re.search(r'(jinja2\.exceptions\..*?|ValueError:.*?|TypeError:.*?|AttributeError:.*?|NameError:.*?)<', content)
    if match:
        print("ERROR FOUND:", match.group(1))
    else:
        # Search for any line containing "Exception" or "Error"
        lines = content.split('\n')
        for line in reversed(lines):
            if "Error" in line or "Exception" in line:
                print("POSSIBLE ERROR:", line.strip())
                break
        print("Could not parse exact error, saving to debug.html")
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(content)
