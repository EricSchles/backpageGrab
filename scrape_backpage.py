import requests
import lxml.html
import pickle
import grequests

def get_all_backpages():
    r = requests.get("http://www.backpage.com/")
    html = lxml.html.fromstring(r.text)
    backpages = html.xpath("//a/@href")
    links = []
    for i in backpages:
        if "backpage" in i:
            if not "www" in i: 
                i = str(i)
                links.append(i)

    with open("backpages","w") as f:
        pickle.dump(links,f)
    
def setup_all(index):
    backpages = pickle.load(open("backpages","rb"))
    female_escorts = []
    body_rubs = []
    strippers = []
    dominatrixes = []
    transsexual_escorts = []
    male_escorts = []
    websites = []
    adult_jobs = []
    for page in backpages:
        for i in xrange(1,index):
            if i == 1:
                female = page + "FemaleEscorts/"
                female_escorts.append(female)
                bodyrub = page + "BodyRubs/"
                body_rubs.append(bodyrub)
                stripper = page + "Strippers/"
                strippers.append(stripper)
                dominatrix = page + "Domination/"
                dominatrixes.append(dominatrix)
                transsexual = page + "TranssexualEscorts/"
                transsexual_escorts.append(transsexual)
                male = page + "MaleEscorts/"
                male_escorts.append(male)
                website = page + "Datelines/"
                websites.append(website)
                adult = page + "AdultJobs/"
                adult_jobs.append(adult)
            else:
                female = page + "FemaleEscorts/?page="+str(i)
                female_escorts.append(female)
                bodyrub = page + "BodyRubs/?page="+str(i)
                body_rubs.append(bodyrub)
                stripper = page + "Strippers/?page="+str(i)
                strippers.append(stripper)
                dominatrix = page + "Domination/?page="+str(i)
                dominatrixes.append(dominatrix)
                transsexual = page + "TranssexualEscorts/?page="+str(i)
                transsexual_escorts.append(transsexual)
                male = page + "MaleEscorts/?page="+str(i)
                male_escorts.append(male)
                website = page + "Datelines/?page="+str(i)
                websites.append(website)
                adult = page + "AdultJobs/?page="+str(i)
                adult_jobs.append(adult)
                
    all_pages = female_escorts + body_rubs + strippers + dominatrixes + transsexual_escorts + male_escorts + websites + adult_jobs
    return all_pages

#gets all the ads on a given backpage, page
def grab_ads(page):
    r = requests.get(page)
    html = lxml.html.fromstring(r.text)
    ads = html.xpath('//div[@class="cat"]/a/@href')
    final = []
    for ad in ads:
        ad = str(ad)
        final.append(ad)
    return final

def get_information_from_page(url_list,asynchronous=False):
    
    if asynchronous:
        for urls in url_list:
            rs = (grequests.get(u,stream=False) for u in urls)
            responses = grequests.map(rs)
            results = []
            for r in responses:
                result = {}
                html = lxml.html.fromstring(r.text)
                posting_body = html.xpath('//div[@class="postingBody"]')
                result["textbody"] = [i.text_content() for i in posting_body]
                result['pictures'] = html.xpath('//ul[@id="viewAdPhotoLayout"]/li/a/@href')
                result['url'] = r.url
                results.append(result)
                r.close()
        return results
            
    else:
        r = requests.get(url_list)
        html = lxml.html.fromstring(r.text)
        posting_body = html.xpath('//div[@class="postingBody"]')
        textbody = [i.text_content() for i in posting_body]
        pictures = html.xpath('//ul[@id="viewAdPhotoLayout"]/li/a/@href')
        return textbody,pictures
print "start.."
pages = setup_all(3)
print "got all the links to start scraping.."
links = []

#for testing
# page = pages[0]
# links.append(grab_ads(page))

# print get_information_from_page(links[0][0])

#for real
print "scraping all the links.."
for page in pages[:10]:
    links += grab_ads(page)

print "grabbing page data..."

#chunking requests because grequests can't handle that many at once
url_list = []
for i in xrange(0,len(links),10):
    url_list.append(links[i-10:i])

data = get_information_from_page(url_list,asynchronous=True)
print data
# data = []
# for link in links:
#     data.append(get_information_from_page(link))
