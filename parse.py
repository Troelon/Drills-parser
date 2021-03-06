from asyncio import tasks
import requests, lxml
from bs4 import BeautifulSoup
import json
import time



product_lst = {} #список для json документа

def get_data():
    i = 2  #счетчик страниц
    while True:
        url = f"https://www.vseinstrumenti.ru/instrument/shurupoverty/setevye/page{i}/#goods"
        res = requests.get(url = url).text
        soup = BeautifulSoup(res, "lxml")
            # создание объекта(представителя) bs
        catalog = soup.find("div", attrs = {"class":"listing-grid -rows"})
            #Нахождение div блока с товарами
        if soup.find("h2", attrs = {"class":"error-title"}) == None:
            product_lst[f"{i}"] = []        #создание списка под страницу
        else:
            print("Парсер завершил работу")
            break
        for el in catalog:        
            if el.name != None and el.attrs["class"][0] != "ad-fox-banner": #проверка на пустой тег с баннером
                prehash = {} #хэш массив для создания json документа
                article = el.find("span", attrs = {"itemprop":"description"})
                if article != None:
                    article_replaced = article.text.replace(" ", "")
                    prehash["article"] = article_replaced
                        #удаление пробела
                        #Получение артикула
                name = el.find("span", attrs = {"itemprop":"name"})
                if name != None:
                    name_replaced = name.text
                    name_replaced = name_replaced[2:-2]
                        #удаление пробелов при помощи срезов
                    prehash["name"] = name_replaced
                        #получение имени товара
                atributes = el.find("div", attrs = {"class":"features"})
                if atributes != None:
                    atributes_lst = atributes.find_all("p")
                    for atribute_iter in atributes_lst:
                        work_lst = atribute_iter.text.split(":")
                            #получение списка с атрибутами первого p тега
                        firt_atribute = work_lst[0]
                        second_atribute = work_lst[1]
                        firt_atribute = firt_atribute.replace(' ', '', 1)
                        if firt_atribute[-1] == " ":
                            firt_atribute = firt_atribute[0:-1]
                        second_atribute = second_atribute[1:-1]
                            #удаление пробелов у атрибута
                        prehash[firt_atribute] = second_atribute
                            #получение атрибутов товара
                price_soup = el.find("div", attrs = {"class":"price"})
                if price_soup != None:
                    price = price_soup.text[0:-3]
                    price = price.replace(" ","")
                        #удаление пробелов и приписки р. для удобства взятия данных
                    prehash["price"] = price
                        #получение цены
                    
                product_lst[f"{i}"].append(prehash)
        

        i+=1
        print("обработана {} страница".format(i-1))

def get_first_page():
    url = "https://www.vseinstrumenti.ru/instrument/shurupoverty/setevye/#goods"
    req = requests.get(url = url)
    soup = BeautifulSoup(req.text, "lxml")
    product_lst["1"] = []        #создание списка под 1 страницу
    # создание объекта(представителя) bs
    catalog = soup.find("div", attrs = {"class":"listing-grid -rows"})
    #Нахождение div блока с товарами
    for el in catalog:
        prehash = {} #хэш массив для создания json документа
        if el.name != None and el.attrs["class"][0] != "ad-fox-banner": # Проверка на пустой тег
            article = el.find("span", attrs = {"itemprop":"description"})
            if article != None:
                article_replaced = article.text.replace(" ", "")
                prehash["article"] = article_replaced
                #удаление пробела
                #Получение артикула
            name = el.find("span", attrs = {"itemprop":"name"})
            if name != None:
                name_replaced = name.text
                name_replaced = name_replaced[2:-2]
                #удаление пробелов при помощи срезов
                prehash["name"] = name_replaced
                #получение имени товара
            atributes = el.find("div", attrs = {"class":"features"})
            if atributes != None:
                atributes_lst = atributes.find_all("p")
                for atribute_iter in atributes_lst:
                    work_lst = atribute_iter.text.split(":")
                    #получение списка с атрибутами первого p тега
                    firt_atribute = work_lst[0]
                    second_atribute = work_lst[1]
                    firt_atribute = firt_atribute.replace(' ', '', 1)
                    if firt_atribute[-1] == " ":
                        firt_atribute = firt_atribute[0:-1]
                    second_atribute = second_atribute[1:-1]
                    #удаление пробелов у атрибута
                    prehash[firt_atribute] = second_atribute
                    #получение атрибутов товара
            price_soup = el.find("div", attrs = {"class":"price"})
            if price_soup != None:
                price = price_soup.text[0:-3]
                price = price.replace(" ","")
                #удаление пробелов и приписки р. для удобства взятия данных
                prehash["price"] = price
                #получение цены
            
            product_lst["1"].append(prehash)
    print("Обработана 1 страница")     



def main():
    get_first_page()
    get_data()
    with open("data.json","w",encoding="utf8") as f:
        json.dump(product_lst,f, indent= 4 ,ensure_ascii= False)
    

if __name__ == "__main__":
    main()