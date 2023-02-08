# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# selenium 4

# import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
from pandas import ExcelWriter


def search(word, writer):
    # Diccionario con url y precio de cada drogueria de los productos
    dictDroguertias = {'Link': [], 'Price': []}
    listLink = []
    listPrice = []
    # listDescription = []
    # Página a Scrapping
    website = 'https://www.google.com.co/search?q=' + word
    # Ruta del driver del navgador
    path = '../Drivers/msedgedriver.exe'

    service = EdgeService(executable_path=path)
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    # Abrir página (website)
    driver.get(website)

    # Mapea todos los elementos con la etiqueta div y anotación data-sokoban-container
    div_dataSokoban = driver.find_elements(By.XPATH, '//div[@data-sokoban-container]')
    for data in div_dataSokoban:
        # Lista creada a partir del string con 3 saltos de linea (cada salto de linea se convierte en la separación de cada elemnto de la lista creada) con cada uno de lo datos mapeados en la variable div_dataSokoban
        listData = str(data.text).splitlines()

        # Buscar si en la lista listData están los nombres de droguerías de interes (index 0 contiene el link de acceso a cada página (h3); index 1 contiene la url)
        if (listData[1].__contains__('cafam')) or (listData[1].__contains__('verde')) or (listData[1].__contains__('locatel')) or (listData[1].__contains__('rebaja')) or (listData[1].__contains__('farmalisto')) or (listData[1].__contains__('farmatodo')) or (listData[1].__contains__('colsubsidio')) or (listData[1].__contains__('ortopedicosfuturo')) or (listData[1].__contains__('santarosa')) or (listData[1].__contains__('farmavida')) or (listData[1].__contains__('sanjorge')) or (listData[1].__contains__('tododrogas')) or (listData[1].__contains__('farmaexpress')):
            # con la url viene información innecesaria. Se crea una nueva lista que contiene en index 0 la url limpia
            nameDrugstoreList = listData[1].split(' ')
            # url limpia
            linkDrugstore = nameDrugstoreList[0]
            listLink.append(linkDrugstore)

            # El último o penúltimo index de listData contiene el precio de cada droguería
            # Sí está en el penúltimo index (en el último index se encuentra información del navegador concerniente a la no semejanza entre lo buscado y lo encontrado caracter por caracter:
            if listData[-1].__contains__('Falta'):
                price = listData[-2].split('·')
                listPrice.append(price[0])
            # Sí está en el último index:
            else:
                price = listData[-1].split('·')
                listPrice.append(price[0])

    # Se va llenando el diccionario con la clave (url de la drpguería) y valor (precio) de cada droguería
    dictDroguertias['Link'] = listLink
    dictDroguertias['Price'] = listPrice
    print(dictDroguertias)
    # Cerrar el driver
    driver.quit()

# -------- Pandas: -------------------------------------------------------------------------------------------------------------------------------------------
    # DataFrame con el diccionario dictDroguertias
    df_drogueria = pd.DataFrame(data=dictDroguertias)
    print(df_drogueria)

    # Crear nueva sheet en el archivo excel creado (write) con nuevo producto:
    df_drogueria.to_excel(writer, sheet_name=word, index=False)
    writer.save()


# Crear archivo excel
writer = ExcelWriter('../docs_xlsx/Data.xlsx')

# Leer excel Portafolio.xlsx
df_read_portafolio = pd.read_excel('/Users/ASUS/PycharmProjects/webScrappingDroguerias/docs_xlsx/Portafolio.xlsx', index_col='i')
temp = 0
for word in df_read_portafolio["Ítems"]:
    search(word.lower(), writer)
    if temp ==4:
        break
    temp+=1


# Llamadas a la función:
# palabra = 'Erassin 50 mg X 2 Tabletas'
# palabra2 = 'Esomeprazol 20 mg X 14 Tabletas AG'
# palabra3 ='Esomeprazol 20 mg X 30 Tabletas Colmed'
# palabra4 = 'Eutirox 100 mcg X 50 Tabletas'

# search(palabra.lower(), writer)
# search(palabra2.lower(), writer)
# search(palabra3.lower(), writer)
# earch(palabra4.lower(), writer)
