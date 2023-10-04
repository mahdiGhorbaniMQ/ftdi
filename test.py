from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Chrome()

driver.get("https://www.ftdi.com/signin")
account = "75-2451AA"
userId = "Razi"
password = "Rugman"
metaData = {
    "crawledCount": 0,
    "lastPage": 0
}
driver.find_element(By.ID, "txtAccount").send_keys(account)
driver.find_element(By.ID,"txtUserID").send_keys(userId)
driver.find_element(By.ID, "txtPassword").send_keys(password)
btns = driver.find_elements(By.CLASS_NAME, "btn-gold")
btns.pop()
btns.pop().click()
driver.find_element(By.CSS_SELECTOR, "#bodyContentWrap a").click()
driver.find_element(By.CSS_SELECTOR, ".tile:not(.first):not(.last) a").click()

file = open("data.json", "a")
# file.write("[")


def readMetaData():
    metaDataRead = open("metaData", "r")
    metaData["crawledCount"] = int(metaDataRead.readline())
    metaData["lastPage"] = int(metaDataRead.readline())
    metaDataRead.close()
    
readMetaData()

def countLastCroawled():
    metaDataWrite = open("metaData", "w")
    print(metaData["crawledCount"])
    metaDataWrite.write(str(int(metaData["crawledCount"])+1)+"\n")
    metaDataWrite.write(str(metaData["lastPage"]))
    metaDataWrite.close()

def clearCountLastCroawled():
    metaDataWrite = open("metaData", "w")
    metaDataWrite.write("0\n")
    metaDataWrite.write(str(metaData["lastPage"]))
    metaDataWrite.close()

def writeLastPage(page):
    metaDataWrite = open("metaData", "w")
    metaDataWrite.write(str(metaData["crawledCount"])+"\n")
    metaDataWrite.write(str(page))
    metaDataWrite.close()

def printItem(item):
    print("_________________________________________________")
    print(item)
    print("_________________________________________________")
    file.write(str(item)+",")
    countLastCroawled()

    
def goNextListPage(index):
    print("next page", index)
    driver.find_element(By.ID, "MainContent_lnkNext").click()
    writeLastPage(index)
    clearCountLastCroawled()


def crawlItem(bouquet: WebElement):
    bouquet.find_element(By.CSS_SELECTOR, "a").click()
    item = {
        "image": driver.find_element(By.ID, "imgItemImage").get_attribute("src")
    }


    def findOtherImgLink(img: WebElement):
        return img.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    otherImgs = driver.find_elements(By.CLASS_NAME, "florist_other_images")
    item["otherImages"] = list(map(findOtherImgLink, otherImgs))


    withAndHeight = driver.find_elements(By.CLASS_NAME, "skudetail-attributesright")
    item["height"] = withAndHeight.pop().text
    item["with"] = withAndHeight.pop().text


    def getRecipe(recipe: WebElement):
        return {
            "c_quantity": recipe.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text,
            "color": recipe.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text,
            "description": recipe.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        }
    recipes = driver.find_elements(By.CSS_SELECTOR, ".skudetail-table:nth-child(3) tr:not(:nth-child(1))")
    item["recipe"] = list(map(getRecipe, recipes))



    def getAdditionalInformation(information: WebElement):
        return {
            "approved_recipe": information.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text,
            "color": information.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text,
            "substitution_guidance": information.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        }
    informations = driver.find_elements(By.CSS_SELECTOR, ".skudetail-table:nth-child(6) tr:not(:nth-child(1))")
    item["additional_information"] = list(map(getAdditionalInformation, informations))


    item["fulfillment_tips"] = driver.find_element(By.CSS_SELECTOR, "ul.big_text li:nth-child(1) span").text
    item["notes"] = driver.find_element(By.CSS_SELECTOR, "ul.big_text li:nth-child(2) span").text


    def getVase(vase: WebElement):
        return {
            "item": vase.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text,
            "description": vase.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text,
            "quantity": vase.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
        }
    vases = driver.find_elements(By.CSS_SELECTOR, ".skudetail-table:nth-child(10) tr:not(:nth-child(1))")
    item["vase"] = list(map(getVase, vases))
    driver.back()
    return item


def crawlBouquet(item: WebElement):
    return {
        "title": item.find_element(By.CSS_SELECTOR, "span").text,
        "id": item.find_element(By.CSS_SELECTOR, "a").text,
        "image": item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    }


def notEmpty(item: WebElement):
    return item.find_element(By.CSS_SELECTOR, "span").text != ""


def crawlList(page):
    if(page==metaData["lastPage"]):
        crawled = metaData["crawledCount"]
    else:
        crawled = 0
    all = driver.find_elements(By.CLASS_NAME, "d-bouquet")
    bouquetsLen = len(list(filter(notEmpty, all)))
    for bIndex in range(bouquetsLen - crawled):
        print("i:"+str(page))
        print("crowled:"+str(crawled))
        print("bIndex:"+str(bIndex))
        print("bouquetsLen:"+str(bouquetsLen))
        all = driver.find_elements(By.CLASS_NAME, "d-bouquet")
        bouquets = list(filter(notEmpty, all))
        bq = bouquets[bIndex + crawled]
        bouquet = crawlBouquet(bq)
        item = {
            "id": bouquet["id"],
            "title": bouquet["title"],
            "image": bouquet["image"],
            "details": crawlItem(bq)
        }
        printItem(item)



for crwaledPage in range(int(metaData["lastPage"])):
    print("next page", crwaledPage)
    driver.find_element(By.ID, "MainContent_lnkNext").click()

for page in range(int(metaData["lastPage"]), 80): 
    crawlList(page)
    goNextListPage(page)
    


 
time.sleep(5)
driver.close()  
file.write("]")
file.close()
