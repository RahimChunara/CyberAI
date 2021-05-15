import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from googlesearch import search
import whois
from datetime import date, datetime
import time
from dateutil.parser import parse as date_parse


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def non_empty(iterable):
    iterator = iter(iterable)
    try:
        yield next(iterator)  # explicitly check first item
    except StopIteration:
        raise LookupError(f'{iterable} is empty') from None
    yield from iterator       # forward iteration of later items


def generate_data_set(url):

    data_set = []

    if not re.match(r"^https?", url):
        url = "http://" + url

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        response = ""
        soup = -999

    domain = re.findall(r"://([^/]+)/?", url)[0]
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")
    whois_response = whois.whois(domain)

    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
        "name": domain
    })

    try:
        global_rank = int(re.findall(
            r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        global_rank = -1

    # 1.having_IP_Address
    # print("Testttttt")
    txt = re.search(
        '^http[s]?:\/\/((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])', url)
    # print(txt)
    if(txt):
        data_set.append(-1)
    else:
        data_set.append(1)

    # 2.URL_Length
    if len(url) < 54:
        data_set.append(1)
    elif len(url) >= 54 and len(url) <= 75:
        data_set.append(0)
    else:
        data_set.append(-1)

    # 3.Shortining_Service
    import urlexpander
    if urlexpander.is_short(url):
        # print("short")
        data_set.append(-1)
    else:
        # print("test")
        data_set.append(1)

    # 4.having_At_Symbol
    sym1 = '@'
    if sym1 not in url:
        data_set.append(1)
    else:
        print("@")
        data_set.append(-1)

    # 5.double_slash_redirecting
    sym2 = '//'
    stripUrl = url.replace("http://", "")
    stripUrl = stripUrl.replace("https://", "")

    if sym2 not in stripUrl:
        data_set.append(1)
    else:
        print("doublehash")
        data_set.append(-1)

    # requisite
    from urllib.parse import urlparse

    parsedDomain = urlparse(url).netloc
    print(parsedDomain)

    # # 6.Prefix_Suffix
    sym3 = "-"
    print("this is a domain" + parsedDomain)
    if sym3 not in parsedDomain:
        print("jskfhdgklhsfdg")
        data_set.append(1)
    else:
        data_set.append(-1)

    # # 7.having_Sub_Domain
    # Check again if needed
    urlparsed = urlparse(url)
    subdomain = urlparsed.hostname.split('.')
    if len(subdomain) == 3:
        data_set.append(1)
    elif len(subdomain) == 4:
        data_set.append(0)
    else:
        data_set.append(-1)

    # # 8.SSLfinal_State
    httpsURL = "https://"
    try:
        if httpsURL in url:
            data_set.append(1)
    except:
        data_set.append(-1)

    # 9.Domain_registeration_length
    expiration_date = whois_response.expiration_date
    registration_length = 0
    try:
        expiration_date = min(expiration_date)
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        registration_length = abs((expiration_date - today).days)

        if registration_length / 365 <= 1:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(-1)

    # 10.Favicon
    # icon_link = soup.find("link", rel="shortcut icon")
    # print('iconnnn')
    # print(icon_link)
    # icon = urllib.urlopen(icon_link['href'])
    # print("edfjiofoijde")
    # print(icon)
    if soup == -999:
        print("soup999")
        data_set.append(-1)
    else:
        try:
            icon_link = soup.find("link", rel="shortcut icon")
            if url in icon_link or domain in icon_link:
                data_set.append(1)
            else:
                data_set.append(-1)
        except:
            data_set.append(-1)

    # 11. port
    try:
        port = domain.split(":")[1]
        if port:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # 12. HTTPS_token
    httpURL = "http://"
    if httpURL in url and httpsURL in url:
        data_set.append(-1)
    else:
        data_set.append(1)

    # # 13. Request_URL
    i = 0
    success = 0
    if soup == -999:
        data_set.append(-1)
    else:
        for img in soup.find_all('img', src=True):
            dots = [x.start(0) for x in re.finditer('\.', img['src'])]
            if url in img['src'] or domain in img['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for audio in soup.find_all('audio', src=True):
            dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
            if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for embed in soup.find_all('embed', src=True):
            dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
            if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for iframe in soup.find_all('iframe', src=True):
            dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
            if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                success = success + 1
            i = i+1
        try:
            percentage = 1 - (success/float(i) * 100)
            if percentage < 22.0:
                data_set.append(1)
            elif((percentage >= 22.0) and (percentage < 61.0)):
                data_set.append(0)
            else:
                data_set.append(-1)
        except:
            data_set.append(1)

    # 14. URL_of_Anchor               #Issue
    percentage = 0
    i = 0
    unsafe = 0
    if soup == -999:
        data_set.append(-1)
    else:
        for a in soup.find_all('a', href=True):
            # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and :: might not be
            # there in the actual a['href']
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href'] or '/' not in a['href'][0]):
                # Href issue  - Fixed
                unsafe = unsafe + 1
            i = i + 1
        try:
            URLpercentage = unsafe / float(i) * 100
            print(URLpercentage)
            if URLpercentage < 31.0:
                data_set.append(1)
            elif ((URLpercentage >= 31.0) and (URLpercentage < 67.0)):
                data_set.append(0)
            else:
                data_set.append(-1)
        except:
            data_set.append(1)

    # 15. Links_in_tags
    i = 0
    success = 0
    if soup == -999:
        data_set.append(-1)
        # data_set.append(0)
    else:
        # print(soup)
        for link in soup.find_all('link', href=True):
            # print(link)
            dots = [x.start(0) for x in re.finditer('\.', link['href'])]
            # print(dots)
            if url in link['href'] or domain in link['href'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for script in soup.find_all('script', src=True):
            dots = [x.start(0) for x in re.finditer('\.', script['src'])]
            if url in script['src'] or domain in script['src'] or len(dots) == 1:
                success = success + 1
            i = i+1
        try:
            linkPercentage = 1 - (success / float(i) * 100)
            print(linkPercentage)
            if linkPercentage < 17.0:
                data_set.append(1)
            elif((linkPercentage >= 17.0) and (percentage < 81.0)):
                data_set.append(0)
            else:
                data_set.append(-1)
        except:
            data_set.append(1)

        # 16. SFH
        if len(soup.find_all('form', action=True)) == 0:
            data_set.append(1)
        else:
            for form in soup.find_all('form', action=True):
                if form['action'] == "" or form['action'] == "about:blank":
                    data_set.append(-1)
                    break
                elif url not in form['action'] and domain not in form['action'] and '/' not in form['action'][0]:
                    # print(form['action'][0])
                    data_set.append(0)
                    break
                else:
                    data_set.append(1)
                    break

    # 17. Submitting_to_email
    # print("emailllll")
    try:
        for script in non_empty(soup.find_all('script', src=True)):
            if "mail" in script['src'] or "mailto" in script['src']:
                data_set.append(-1)
            else:
                print("insideee")
                data_set(1)
    except:
        print(("exception"))
        data_set.append(1)

    # 18. Abnormal_URL                #Fix this
    if response == "":
        print("empty reponse")
        data_set.append(-1)
    else:
        data_set.append(-1)
        # print("abnornal")
        # print(domain)
        # if response.text == whois_response:
        #     print("response")
        #     print(response.text)
        #     data_set.append(1)
        # else:
        #     data_set.append(-1)

    # 19. Redirect         #Issue
    if response == "":
        data_set.append(-1)
    else:
        print(url)
        # print(response.history)
        if len(response.history) <= 1:
            data_set.append(1)
        elif len(response.history) <= 4:
            data_set.append(0)
        else:
            data_set.append(-1)

    # 20. on_mouseover
    if response == "":
        data_set.append(-1)
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            data_set.append(-1)
        else:
            data_set.append(1)

    # 21. RightClick
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            data_set.append(-1)
        else:
            data_set.append(1)

    # # 22. popUpWidnow
    if response == "":
        data_set.append(-1)
    else:
        if re.findall(r"alert\(", response.text):
            data_set.append(-1)
        else:
            data_set.append(1)

    # 23. Iframe
    if response == "":
        data_set.append(-1)
    else:
        try:
            for iframe in non_empty(soup.findAll('iframe')):
                if iframe:
                    data_set.append(-1)
                else:
                    data_set.append(1)
        except:
            data_set.append(1)

    # 24. age_of_domain
    if response == "":
        data_set.append(-1)
    else:
        try:
            registration_date = re.findall(
                    r'Registration Date:</div><div class="df-value">([^<]+)</div>', whois_response.text)[0]
            if diff_month(date.today(), date_parse(registration_date)) >= 6:
                data_set.append(1)
            else:
                data_set.append(-1)
        except:
            data_set.append(1)

    # 25. DNSRecord
    # dns = 1
    try:
        d = whois.whois(domain)
        data_set.append(1)
    except:
        data_set.append(-1)
    #     dns = -1
    # if dns == -1:
    #     data_set.append(-1)
    # else:
    #     print(registration_length)
    #     if registration_length / 365 <= 1:
    #         data_set.append(-1)
    #     else:
    #         data_set.append(1)

    # 26. web_traffic
    try:
        rank = BeautifulSoup(urllib.request.urlopen(
            "http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        rank = int(rank)
        if (rank < 100000):
            # print(rank)
            data_set.append(1)
        else:
            data_set.append(0)
    except :
        data_set.append(-1)

    # 27. Page_Rank
    try:
        if global_rank > 0 and global_rank < 100000:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # 28. Google_Index
    site = search(url, 5)
    if site:
        data_set.append(1)
    else:
        data_set.append(-1)

    # 29. Links_pointing_to_page
    if response == "":
        data_set.append(-1)
    else:
        number_of_links = len(re.findall(r"<a href=", response.text))
        if number_of_links == 0:
            data_set.append(1)
        elif number_of_links <= 2:
            data_set.append(0)
        else:
            data_set.append(-1)

    # 30. Statistical_report
    url_match = re.search(
        'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', url)
    try:
        ip_address = socket.gethostbyname(domain)
        ip_match = re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                             '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                             '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                             '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                             '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                             '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42', ip_address)
        if url_match:
            data_set.append(-1)
        elif ip_match:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        print('Connection problem. Please check your internet connection')

    import csv
    file = open('gg.csv', 'w+', newline='')

    with file:
        write = csv.writer(file)
        write.writerow(['having_IP_Address', 'URL_Length', 'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 'SSLfinal_State', 'Domain_registeration_length', 'Favicon', 'port', 'HTTPS_token', 'Request_URL', 'URL_of_Anchor',
                        'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL', 'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe', 'age_of_domain', 'DNSRecord', 'web_traffic', 'Page_Rank', 'Google_Index', 'Links_pointing_to_page', 'Statistical_report', 'Result'])
        write.writerow(data_set)
#     return data_set


# if __name__ == "__main__":
#     # execute only if run as a script
#     print(generate_data_set("user-amazon.ey1.xyz"))
