def extractDetails(web):
    #!/usr/bin/env python
    # coding: utf-8

    # In[24]:

    output_csv = []
# IP Address
    # web = "https://www.hud.ac.uk/students/"
    import re

    txt = re.search(
        '^http[s]?:\/\/((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])', web)
    if(txt):
        output_csv.append(-1)
    else:
        output_csv.append(1)

    # In[25]:

    # Long URL to Hide the Suspicious Part
    if(len(web) > 54) and (len(web) < 75):
        output_csv.append(0)
    elif((len(web) > 75)):
        output_csv.append(-1)
    else:
        output_csv.append(1)

    # In[26]:

    # Using URL Shortening Services “TinyURL”
    import urlexpander
    if urlexpander.is_short(web):
        output_csv.append(-1)
    else:
        output_csv.append(1)

    # In[27]:

    # URL’s having “@” Symbol
    sym1 = '@'
    if sym1 not in web:
        output_csv.append(1)
    else:
        output_csv.append(-1)

    # In[6]:

    # Redirecting using “//”
    sym2 = '//'
    stripUrl = web.replace("http://", "")
    stripUrl = stripUrl.replace("https://", "")

    if sym2 not in stripUrl:
        output_csv.append(1)
    else:
        output_csv.append(-1)

    # In[7]:

    from urllib.parse import urlparse

    domain = urlparse(web).netloc
    print(domain)

    # In[8]:

    # Adding Prefix or Suffix Separated by (-) to the Domain
    sym3 = "-"
    if sym3 not in domain:
        output_csv.append(1)
    else:
        output_csv.append(-1)

    # In[9]:

    url = urlparse(web)
    subdomain = url.hostname.split('.')
    if len(subdomain) < 2:
        output_csv.append(1)
    elif len(subdomain) == 2:
        output_csv.append(0)
    else:
        output_csv.append(-1)

    # In[10]:

    httpsURL = "https://"

    if httpsURL in web:
        output_csv.append(1)
    else:
        output_csv.append(-1)

    # In[11]:

    # website creation date > 1
    # import whois
    # import datetime
    # time_now = datetime.datetime.today().year
    # domain_details = whois.whois(web)

    # difference_time = time_now - domain_details.creation_date[0].year
    # if difference_time > 1:
    #     output_csv.append(-1)
    # else:
    #     output_csv.append(1)

    # In[12]:

    # Favicon

    # In[13]:

    # Non standard ports
    # import socket
    # target = socket.gethostbyname('staypocket.com')
    # print(target)
    # for port in range(1,3390):
    #         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         socket.setdefaulttimeout(1)

    #         # returns an error indicator
    #         result = s.connect_ex((target,port))
    #         if result ==0:
    #             print("Port {} is open".format(port))
    #         s.close()

    # In[14]:

    # The Existence of “HTTPS” Token in the Domain Part of the URL
    httpURL = "http://"

    if httpURL in web and httpsURL in web:
        output_csv.append(1)
    else:
        output_csv.append(0)

    # In[15]:

    # Request URL

    # In[4]:

    import requests
    from requests_html import HTMLSession

    # In[5]:

    # Request URL
    url = "https://www.google.com"
    session = HTMLSession()
    response = session.get(web)
    links = response.html.absolute_links
    domain = 'google'
    res = 0
    for key in links:
        if domain in key:
            res = res + 1

    if (len(links) - res)/len(links)*100 < 22:
        output_csv.append(1)
    elif (len(links) - res)/len(links)*100 >= 22 and (len(links) - res)/len(links)*100 < 61:
        output_csv.append(0)
    else:
        output_csv.append(-1)

    # In[6]:

    # URL of Anchor
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(response.text)

    for link in soup.findAll('a', href=True):
        if link:
            output_csv.append(1)
            break
        else:
            output_csv.append(0)
        print(link['href'])

    # In[1]:

    # Links in <Meta>, <Script> and <Link> tags
    for scripts in soup.findAll('meta', attrs={'name': 'description'}):
        print(scripts['content'])

    # In[8]:

    # Server Form Handler (SFH)
    from requests_html import HTMLSession
    from urllib.parse import urljoin

    urlsfh = 'https://indiapostgdsonline.in/gdsonlinec3p3/Registration_A.aspx'
    res = session.get(web)

    soup = BeautifulSoup(res.html.html, "html.parser")
    # print(soup)

    for sfh in soup.findAll('form'):
        action = sfh.attrs.get("action").lower()
        print(action)
    print(action[0] == '/')

    # In[9]:

    # Submitting Information to Email
    for script in soup.findAll('script'):
        #     print(script)
        mail = script.find('mail:')
        mailto = script.find('mailto:')

    if mail or mailto:
        output_csv.append(1)
    else:
        output_csv.append(0)

    # In[10]:

    # Abnormal URL

    # In[11]:

    # Website Forwarding

    # In[15]:

    # Status Bar Customization
    from requests_html import HTMLSession
    from urllib.parse import urljoin
    urlstatus = 'https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_onmouseover'
    resstatus = session.get(web)

    soupstatus = BeautifulSoup(resstatus.html.html, "html.parser")

    for statuscust in soupstatus.findAll(onmouseover=True):
        if 'window.status' in statuscust['onmouseover']:
            output_csv.append(1)
        else:
            output_csv.append(-1)

    # In[ ]:

    # Using Pop-up Window

    # In[22]:

    # IFrame Redirection
    urliframe = 'https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_iframe'
    resiframe = session.get(web)

    soupiframe = BeautifulSoup(resiframe.html.html, "html.parser")

    for iframe in soupiframe.findAll('iframe'):
        if iframe:
            output_csv.append(1)
        else:
            output_csv.append(-1)

    # In[ ]:

    # Age of domain
    import whois
    import datetime
    w = whois.whois(web)
    if type(w.creation_date) == list:
        w.creation_date.reverse()
        cre = w.creation_date[0]
    else:
        cre = w.creation_date
    now = datetime.datetime.now()
    d = (now.year - cre.year) * 12 + (now.month - cre.month)
    if d < 6:
        output_csv.append(-1)
    else:
        output_csv.append(1)

    # In[ ]:

    # Dns record
    if w is None:
        output_csv.append(-1)
    else:
        output_csv.append(1)

    # In[ ]:

    # website Traffic

    # In[ ]:

    # pagerank,google

    # In[ ]:

    # number of links towards page
    from bs4 import BeautifulSoup
    from collections import Counter
    import requests
    count = 0
    soup = BeautifulSoup(requests.get(
        web).text, "html.parser")

    foundUrls = Counter([link["href"] for link in soup.find_all(
        "a", href=lambda href: href and not href.startswith("#"))])
    foundUrls = foundUrls.most_common()

    for item in foundUrls:
        count += 1
    if count == 0:
        output_csv.append(-1)
    elif count > 0 and count <= 2:
        output_csv.append(0)
    else:
        output_csv.append(1)

    # In[ ]:

    # writing the data into the final CSV
    import csv
    file = open('gg.csv', 'w+', newline='')

    with file:
        write = csv.writer(file)
        write.writerow('having_IP_Address,URL_Length,Shortining_Service,having_At_Symbol,double_slash_redirecting,Prefix_Suffix,having_Sub_Domain,SSLfinal_State,Domain_registeration_length,Favicon,port,HTTPS_token,Request_URL,URL_of_Anchor,Links_in_tags,SFH,Submitting_to_email,Abnormal_URL,Redirect,on_mouseover,RightClick,popUpWidnow,Iframe,age_of_domain,DNSRecord,web_traffic,Page_Rank,Google_Index,Links_pointing_to_page,Statistical_report,Result')
        write.writerow(output_csv)
