from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

import pandas as pd
from tqdm import tqdm
#start_page bat dau tu 1
start_page = 30
end_page = 31

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

pages = range(start_page,end_page)
# df = pd.DataFrame(columns=['product','comment'])
print("start")

for page in tqdm(pages):
    print(page)
    driver.get(f'https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A13896617011&page={page}&qid=1661959022&ref=sr_pg_2')
    items = driver.find_elements(By.CLASS_NAME,"s-product-image-container.aok-relative.s-image-overlay-grey.s-text-center.s-padding-left-small.s-padding-right-small.puis-spacing-small.s-height-equalized")
    items = [item.find_element(By.TAG_NAME,'a').get_attribute('href') for item in items]

    page_df = pd.DataFrame(columns=['product','comment'])

    for item in tqdm(items):
        driver.get(item)
        product_name = driver.find_element(By.ID,"productTitle").text
    
        cmt_link  = driver.find_elements(By.CLASS_NAME,'a-link-emphasis.a-text-bold')
        if len(cmt_link) > 0:
            driver.get(cmt_link[0].get_attribute('href'))
            while True:
                cmts = driver.find_elements(By.CLASS_NAME,'a-size-base.review-text.review-text-content')
                
                for cmt in cmts:
                    cmt = cmt.find_elements(By.TAG_NAME,'span')
                    if len(cmt)>0:
                        # print(cmt[0].text)
                        # df = df.append({'product':product_name,'comment':cmt[0].text},ignore_index=True)
                        page_df = page_df.append({'product':product_name,'comment':cmt[0].text},ignore_index=True)

                next_page = driver.find_elements( By.CLASS_NAME,'a-last' )
                if len(next_page) != 0:
                    if next_page[0].get_attribute('class') == 'a-last' :
                        next = next_page[0].find_element(By.TAG_NAME,'a')
                        driver.get(next.get_attribute('href'))
                    else:
                        break
                else:
                    break
    page_df.to_csv(f'comment_{page}.csv')

# df.to_csv(f'./comment_{start_page}_{end_page}.csv')
driver.close()