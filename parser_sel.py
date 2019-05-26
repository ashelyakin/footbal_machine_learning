from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

#получаем матрицу, в которой одна строка - все xG параметры одного матча, а последний элемент строки - исход
def parse_one_page(page):
      ind = 0
      begin1 = page.find('width_300" data-description="Количество ожидаемых пропущенных голов за 90 мин', ind)
      end1 = page.find('score-prev', begin1)
      begin2 = page.find('<div>xGA/Sh</div>', end1+10)
      end2 = page.find('score-prev', begin2)
      ind = end2 + 1
      regex_xg = re.findall(r'(<div class="table_cell">-?\d+\.?\d{0,2}</div>)', page[begin1:end1]) + re.findall(
        r'(<div class="table_cell">-?\d+\.?\d{0,2}</div>)', page[begin2:end2])
      while begin1 != -1:
          begin1 = page.find('<div>xGA/Sh</div>', ind)
          end1 = page.find('score-prev', begin1)
          begin2 = page.find('<div>xGA/Sh</div>', end1 + 10)
          end2 = page.find('score-prev', begin2)
          ind = end2 + 1
          regex_xg += re.findall(r'(<div class="table_cell">-?\d+\.?\d{0,2}</div>)', page[begin1:end1]) + re.findall(
              r'(<div class="table_cell">-?\d+\.?\d{0,2}</div>)', page[begin2:end2])
      regex_score = re.findall(r'(<div>Счет: \d+-\d+</div>)', page)
      if len(regex_xg) < len(regex_score)*16:
          return ''
      res = ''
      end = 0
      j = 0
      for i in range(len(regex_score)):
        end = 0
        while end < 16:
            res += re.findall(r'-?\d+\.?\d{0,2}', regex_xg[j])[0]
            res += ' '
            j += 1
            end += 1
        a1 = re.findall(r'\d+-', regex_score[i])[0]
        a = a1[:len(a1)-1]
        b1 = re.findall(r'-\d+', regex_score[i])[0]
        b = b1[1:]
        if (a<b) :
            res += '3'
        elif (a>b):
            res += '1'
        else:
            res += '2'
        res += '\n'
      return res

#получаем список с индексами туров
def page_info(page):
    league_ind = page.find('ul data-select-list="tournament"')
    year_ind = page.find('ul data-select-list="year"', league_ind)
    tour_ind = page.find('ul data-select-list="tour"', year_ind)
    end_ind = page.find('</ul>', tour_ind)
    league_list = re.findall(r'data-value="\d+"', page[league_ind:year_ind])
    year_list = re.findall(r'data-value="\d+"', page[year_ind:tour_ind])
    tour_list = re.findall(r'data-value="\d+"', page[tour_ind:end_ind])
    res1 = []
    res2 = []
    res3 = []
    for x in league_list:
        res1.append(int(re.findall(r'\d+', x)[0]))
    for x in year_list:
        res2.append(int(re.findall(r'\d+', x)[0]))
    for x in tour_list:
        res3.append(int(re.findall(r'\d+', x)[0]))
    return [res1, res2, res3]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
url = 'https://xscore.win/xg-statistics/view.php?country=39'
driver.get(url)
WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.CLASS_NAME, "table_cell_name")))

league_list = page_info(driver.page_source)[0]
f = open('399999Norvegia.txt', 'a')
'''
for i in tour_list:
    driver.find_elements_by_css_selector('button.btn_select.btn_gradient_border')[3].click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-value='"+str(i)+"']")))
    time.sleep(0.2)

    driver.find_element_by_xpath("//li[@data-value='"+str(i)+"']").click()
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.inner_btn")))

    driver.find_element_by_css_selector('button.inner_btn').click()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "table_cell_name")))

    f.write(parse_one_page(driver.page_source))
    print('tour ', i, ' success')


'''
try:
    for k in league_list:
        driver.find_elements_by_css_selector('button.btn_select.btn_gradient_border')[1].click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-value='" + str(k) + "']")))
        driver.find_element_by_xpath("//li[@data-value='" + str(k) + "']").click()
        print('league ', k, ' begin')
        time.sleep(0.3)
        year_list = page_info(driver.page_source)[1]
        for j in year_list:
            driver.find_elements_by_css_selector('button.btn_select.btn_gradient_border')[2].click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-value='" + str(j) + "']")))
            driver.find_element_by_xpath("//li[@data-value='" + str(j) + "']").click()
            print('year ', j, ' begin')
            time.sleep(1)
            tour_list = page_info(driver.page_source)[2]
            tour_list.pop()
            for i in tour_list:
                time.sleep(1)
                #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_select.btn_gradient_border")))
                driver.find_elements_by_css_selector('button.btn_select.btn_gradient_border')[3].click()
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-value='" + str(i) + "']")))
                time.sleep(0.2)

                driver.find_element_by_xpath("//li[@data-value='" + str(i) + "']").click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.inner_btn")))

                driver.find_element_by_css_selector('button.inner_btn').click()
                WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.CLASS_NAME, "table_cell_name")))

                f.write(parse_one_page(driver.page_source))
                print('tour ', i, ' success')
            print('year ', j, ' success')
        print('league ', k, ' success')
finally:
    f.close()
driver.quit()

