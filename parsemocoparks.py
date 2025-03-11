def write(parks):
    with open("parks.csv", mode="w") as f:
        f.write("parkname, parkaddress\n")
        f.write("\n".join([f"{p[0]},{'N/A' if p[1] is None else p[1]}" for p in parks]))

def parse_html(html_content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    htmlparks = soup.select("article.single-park")
    logger.info("%s parks on this page", len(htmlparks))
    parks = []
    for p in htmlparks:
        parkname = p.h2.text
        parkaddress = p.address.text.replace(", "," ").replace(",","").replace("\n"," ") if p.address else None
        park = parkname, parkaddress
        logger.debug(parkname)
        parks.append(park)
    return parks

def test():
    with open("Parks, Trails & Facilities Directory - Montgomery Parks.html", encoding="utf-8", mode="r") as f:
        html_content = f.read()
    parks = parse_html(html_content)
    write(parks)

def main():
    import requests
    parks = []
    logger.info("Starting GET from Parks Directory")
    for n in range(1,35):
        logger.debug("Page %s",n)
        r = requests.get(f"https://montgomeryparks.org/parks-directory/page/{n}/")
        if r.status_code==200:
            html_content = r.content
            singlepageparks = parse_html(html_content)
            parks.append(singlepageparks)
        else:
            raise Exception("Bad GET")
    write(parks)


if __name__ == "__main__":
    import logging
    logfile = "parse_moco_parks.log"
    logging.basicConfig(filename=logfile, filemode="w", 
                        format="%(asctime)s|%(levelname)s|%(name)s|%(message)s", 
                        datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.DEBUG)

    logger = logging.getLogger("parsemocoparks") # or __name__

    logger.info("Start")
    test()
    logger.info("All Done")
