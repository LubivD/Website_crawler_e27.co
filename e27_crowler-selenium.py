import csv
import random
import selenium.webdriver.support.expected_conditions as EC

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, InvalidSelectorException, \
    ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

PATH = r'C:\Program Files (x86)\Google\chromedriver.exe'
driver = webdriver.Chrome(PATH)

main_link = 'https://e27.co/startups'
# main_link = 'https://e27.co/startups/?pro=0&raised_amount_min=1&raised_amount_max=50000&tab_name=recentlyupdated'

result_data = 'result_data.csv'
result_urls = 'result_urls.csv'
headers_data = ['company_name', 'request_url', 'request_company_url', 'location', 'tags',
                'founding_date', 'founders', 'employee_range', 'urls', 'emails', 'phones', 'description_short',
                'description']
header_urls = 'Result urls'
list_of_class_name = ['startup-name', 'request_url', 'startup-website', 'startup-startup_location',
                      'startup-startup_market', 'startup-date-founded', 'founders', 'employee_range',
                      'website-wrapper section-wrapper', 'e-mails', 'phones', 'startup-short-description',
                      'body-text-overflow']
amount_of_links = 250


def collect_urls():
    driver.get(main_link)
    driver.implicitly_wait(10)
    find_button = driver.find_elements_by_xpath('//*[@id="recently-updated"]/div/div/table/tbody/tr[13]')[0]
    btn = WebDriverWait(driver, 20).until(EC.visibility_of(find_button))

    startup_list_count = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'startup_list_count')))
    quantity_of_links = startup_list_count.text.split()[0].replace(',', '')
    amount = 0

    urls = []

    while amount < int(quantity_of_links):
        try:
            btn.click()
            amount += 1
            print('done', amount)
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'startup_list_count'))
            WebDriverWait(driver, 2).until_not(element_present)
        except TimeoutException:
            print('Wait for button!')
        except ElementClickInterceptedException:
            print("Page hasn't downloaded yet...")
        except ElementNotInteractableException:
            print("Page downloaded successful!")
            break

        # except Exception as e:
        #     print(f"Web-page loading was interrupted by {e}")

    table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'table')))
    amount = len(table.find_elements_by_class_name('startuplink'))
    print(amount, 'amount of link on the web-page')

    full_table = driver.find_element_by_class_name('table')
    links = full_table.find_elements_by_class_name('startuplink')[1:]

    for link in links:
        urls.append(link.get_attribute('href'))

    return urls


def write_urls_to_csv(file_name, header, data):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([header])
        for row in data:
            writer.writerow([row])
            # print(row)


def random_urls():
    with open(result_urls, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)[1:]

    random.shuffle(data)
    random_data = data[:amount_of_links]

    return random_data


def grabb_info():
    rows_with_info = []

    def grab_text_info(class_n):
        wait_for_class_info = driver.find_elements_by_class_name(class_n)[1]
        class_info = WebDriverWait(driver, 60).until(EC.visibility_of(wait_for_class_info))
        class_f = class_info.get_attribute('class')

        if class_n == class_f:
            info = class_info.text
            return info
        elif class_n != class_f:
            return ''

    def grab_site_info(class_n):
        wait_for_class_info = driver.find_elements_by_class_name(class_n)[1]
        class_info = WebDriverWait(driver, 60).until(EC.visibility_of(wait_for_class_info))
        class_f = class_info.get_attribute('class')

        if class_n == class_f:
            info = class_info.get_attribute('href')

            return info
        elif class_n != class_f:
            return ''

    def grab_description_info(class_n):
        wait_for_class_info = driver.find_element_by_class_name(class_n)
        class_info = WebDriverWait(driver, 60).until(EC.visibility_of(wait_for_class_info))
        class_f = class_info.get_attribute('class')

        if class_n == class_f:
            info = class_info.text
            return info
        elif class_n != class_f:
            return ''

    def grab_urls_info(class_n):
        class_info = driver.find_element_by_tag_name(str(class_n))
        # class_info = WebDriverWait(driver, 20).until(EC.visibility_of(wait_for_class_info))
        class_f = class_info.get_attribute("attribute name")
        print(class_f)
        if class_n == class_f:
            try:
                info = class_info.get_attribute('href')
                return info
            except InvalidSelectorException as e:
                print(e)
        elif class_n != class_f:
            return ''

    for url in random_urls():
        print(url[0])
        driver.get(url[0])
        driver.implicitly_wait(10)
        row_with_info = []

        for num, class_name in enumerate(list_of_class_name):

            # NAME
            if num == 0:
                name = grab_text_info(class_name)
                row_with_info.append(name)
                print(name)

            # REQUEST_URL
            elif num == 1:
                if class_name == 'request_url':
                    row_with_info.append(url[0])
                    print(url[0])

            # COMPANIES WEB-SITE
            elif num == 2:
                website = grab_site_info(class_name)
                row_with_info.append(website)
                print(website)

            # LOCATION
            elif num == 3:
                location = grab_text_info(class_name)
                row_with_info.append(location)
                print(location)

            # TAG
            elif num == 4:
                tag = grab_text_info(class_name)
                row_with_info.append(tag)
                print(tag)

            # DATE
            elif num == 5:
                date = grab_text_info(class_name)
                row_with_info.append(date)
                print(date)

            # FOUNDERS
            elif num == 6:
                # founders = grab_text_info(class_name)
                # row_with_info.append(founders)
                row_with_info.append('')
                print('founders')

            # EMPOLYEE_RANGE
            elif num == 7:
                team_members = driver.find_elements_by_xpath(
                    '//*[@id="startupView"]/div[2]/div[2]/div/div/div/div/div/div[3]/div[2]/div[3]/div[2]/div/div')
                amount_team_members = len(team_members)
                row_with_info.append(amount_team_members)
                print(amount_team_members)

            # URLS
            elif num == 8:
                # class_urls = ['startup-twitter', 'startup-linkedin', 'startup-facebook']
                # urls_list = []
                # for urls in class_urls:
                #     url = grab_urls_info(class_urls)
                #     urls_list = row_with_info.append(urls)
                row_with_info.append('')
                print('urls_list')

            # E_MAILS
            elif num == 9:
                # e_mails = grab_text_info(class_name)
                row_with_info.append('')
                print('e-mails')

            # PHONES
            elif num == 10:
                # phones = grab_text_info(class_name)
                row_with_info.append('')
                print('phones')

            # SHORT_DESCRIPTION
            elif num == 11:
                s_description = grab_description_info(class_name)
                r_description = row_with_info.append(s_description.replace('\n', ' '))
                print(r_description)

            # SHORT_DESCRIPTION
            elif num == 12:
                description = grab_description_info(class_name)
                r_description = row_with_info.append(description.replace('\n', ' '))
                print(r_description)

        rows_with_info.append(row_with_info)
    print(rows_with_info)
    return rows_with_info


def write_data_to_csv(file_name, header, data):
    with open(file_name, 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        writer.writerows(data)


def main():
    list_of_urls = collect_urls()
    full_data = grabb_info()
    write_urls_to_csv(result_urls, header_urls, list_of_urls)
    write_data_to_csv(result_data, headers_data, full_data)


if __name__ == "__main__":
    main()
