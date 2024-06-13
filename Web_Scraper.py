import bs4
import requests as rq
import re
import csv
import ast

# Constants
BASE = 'https://www.lamudi.com.ph/buy/laguna/house/?sort=newest'
PAGE = '&page='
CSV_FILE = 'Properties.csv'

# Fetch page
def fetch_page(url):
    try:
        res = rq.get(url)       # get url
        res.encoding = 'utf-8'  # assign encoding
        res.raise_for_status()  # check status
        return bs4.BeautifulSoup(res.text, 'html.parser')
    except rq.RequestException:
        print(f"Failed to fetch {BASE}")    # failed to fetch
        return None

# Scroll through pages
def pagination():
    # get max pages
    soup = fetch_page(BASE + PAGE + '1')
    listings = soup.select('div.BaseSection.Pagination')
    max_pages = int(listings[0].get('data-pagination-end'))
    data = []

    # loop through pages
    for page in range(1, max_pages+1):   
        url = BASE + PAGE + str(page)  # base url + page
        soup = fetch_page(url)
        if soup:
            data.extend(scrape_listings(soup))
    return data   

# Scrape variables from listings
def scrape_listings(soup):
    # initiate selector 
    listings = soup.select('div.ListingCell-AllInfo.ListingUnit')
    # iterates through listings per page
    data = []
    for listing in listings:
        # appends data (from function calls) to dictionary
        data.append({
            'Title': get_title(listing),
            'Price_pesos': get_price(listing),
            'Barangay': get_barangay(listing),
            'Municipality': get_municipality(listing),
            'Seller': get_seller(listing),
            'Number_Bedrooms': get_beds(listing),
            'Floor_sqm': get_floor(listing),
            'Land_sqm': get_land(listing),
            'Latitude' : get_latitude(listing),
            'Longitude' : get_longitude(listing)
        })
    return data

# Write data to CSV
def write_csv(data):
    headers = data[0].keys()                      # initialize headers
    # CSV operations
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)   # dictionary to csv
        writer.writeheader()
        writer.writerows(data)
    print(f"Data successfully written to {CSV_FILE}")

# Extracting text via selectors, stripping strings
def get_text(element, selector, default = ''):
    elem = element.select_one(selector)
    return elem.text.strip() if elem else default

# LISTING TITLE
def get_title(listing):
    return get_text(listing, 'div.ListingCell-TitleWrapper > div > h3')

# PRICE
def get_price(listing):
    price_raw = get_text(listing, 'div.ListingCell-KeyInfo-PriceWrapper')
    price_regex = re.compile(r"₱([\d,]+)")
    match = price_regex.search(price_raw)
    return match.group(1).replace('₱', '').replace(',', '') if match else None      # get peso value (some have dollar equivalents), remove peso sign and commas

# ADDRESS - brgy, municipality
def get_address(listing):
    address_raw = get_text(listing, 'div.ListingCell-TitleWrapper > div > div')
    return address_raw.split(', ') if ',' in address_raw else address_raw   # if may comma, return splitted string as list, else return string

# Barangay
def get_barangay(listing):
    return get_address(listing)[0] if type(get_address(listing)) == list else ''   # if list, return index 0 as barangay, else NF

# Municipality
def get_municipality(listing):
    return get_address(listing)[1] if type(get_address(listing)) == list else get_address(listing)  # if # if list, return index 1 as city, else string

# SELLER"S NAME
def get_seller(listing):
    return get_text (listing, 'div.ListingDetail-agent-name')

# ATTRIBUTES - beds, floor, land
def get_attributes(listing, regex):
    attrib_raw = get_text(listing, 'div.ListingCell-keyInfo-details > div')
    attrib = re.sub(r'\s+', '', attrib_raw)             # remove whitespaces
    match = regex.search(attrib)                        # match search specific attribute
    return match.group(1) if match else ''

# Number of Bedrooms
def get_beds(listing):
    regex = re.compile(rf"(\d+)Bedrooms")   # values that come before 'Bedroom'
    return get_attributes(listing, regex)

# Floor Size
def get_floor(listing):
    regex = re.compile(rf"(\d+)m²Floor")
    return get_attributes(listing, regex)   # values that come before 'm²Floor'

# Land Area
def get_land(listing):
    regex = re.compile(rf"(\d+)m²Land")
    return get_attributes(listing, regex)   # values that come before 'm²Land'

# COORDINATES - latitude, longitude from div
def get_coordinates(listing):
    geo_point_raw = listing.get('data-geo-point')
    coor = ast.literal_eval(geo_point_raw) if geo_point_raw else [0,0]
    return coor

# Latitude
def get_latitude(listing):
    coor = get_coordinates(listing)
    return coor[0]      # 1st coor as latitude

# Longitude
def get_longitude(listing):
    coor = get_coordinates(listing)
    return coor[1]      # 2nd coor as longitude

if __name__ == "__main__":
    data = pagination()
    write_csv(data)