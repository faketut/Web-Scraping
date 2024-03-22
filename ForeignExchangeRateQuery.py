from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import Select
# 第一题 网页抓取题目--外汇牌价查询
# 这是中国银行外汇牌价网站：https://www.boc.cn/sourcedb/whpj/
# 请使用python3 和 selenium库写一个程序，实现以下功能：
# 输入：日期、货币代号
# 输出：该日期该货币的“现汇卖出价” /html/body/div/div[4]/table/tbody/tr[2]/td[4]
# 示例：python3 yourcode.py 20211231 USD
# 输出：636.99
# 该日期有很多个价位，只需要输出任意一个时间点的价位即可。
# 货币代号为USD、EUR这样的三位英文代码，请参考这里的标准符号：
# https://www.11meigui.com/tools/currency
# 要求：
# 1.将selenium爬到的数据打印到一个result.txt 文件里；
# 2.代码规范，注释清晰，变量命名合理易读，无不必要的冗余；
# 3.有适当的异常处理。

class FetchPage():
    def setUp(self, date, currency):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.date = date
        self.currency = currency

    def GetChineseSymbol(self):
        driver = self.driver
        driver.get("https://www.11meigui.com/tools/currency")
 
        try:
            page_src = driver.page_source
            #print(page_src)  # Print out the page source for debugging
            soup = BeautifulSoup(page_src, 'html.parser')
            elt = soup.find_all('td', string=lambda string: string.strip() == self.currency if string else False)[0]
            if elt:
                second_td_before_elt = elt.find_previous_siblings('td')[2]
                if second_td_before_elt:
                    return second_td_before_elt.text.strip()
                else:
                    print("Second <td> element before the currency symbol not found.")
                    return None
            else:
                print("Currency symbol not found.")
                return None
        except NoSuchElementException:
            print("An error occurred while fetching the currency symbol.")
            return None
    
    def FetchPrice(self):
        driver = self.driver
        chinese_symbol = self.GetChineseSymbol()
        driver.get('https://www.boc.cn/sourcedb/whpj/')
        start_date = driver.find_element(By.XPATH, '//*[@id="historysearchform"]/div/table/tbody/tr/td[2]/div/input')
        end_date = driver.find_element(By.XPATH, '//*[@id="historysearchform"]/div/table/tbody/tr/td[4]/div/input')
        select_currency = Select(driver.find_element(By.XPATH, '//*[@id="pjname"]'))
        submit_btn = driver.find_element(By.XPATH,'//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input')

        # fill out fields
        select_currency.select_by_value(chinese_symbol)
        
        start_date.clear()
        start_date.send_keys(self.date)
        end_date.clear()
        end_date.send_keys(self.date)
        
        submit_btn.click()
        # fetch the desried price
        price_elt = driver.find_element(By.XPATH,'/html/body/div/div[4]/table/tbody/tr[2]/td[4]')
        price = price_elt.text

        # write price to file
        with open("result.txt", "w") as f:
            f.write(price)



if __name__ == "__main__":
    test = FetchPage()
    inp = input()
    date = inp.split()[0]
    currency = inp.split()[1]
    # date = 20211231
    # currency = 'USD'
    test.setUp(date, currency)
    test.FetchPrice()