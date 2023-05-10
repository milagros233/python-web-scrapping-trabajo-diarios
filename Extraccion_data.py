import pandas as pd
from bs4 import BeautifulSoup
import requests



def web_scraping(nomPuesto,cantidadPaginas):
    #url de la pagina
    main_url="https://pe.trabajosdiarios.com"
    front_url="ofertas-trabajo/de-"+nomPuesto.replace(" ","-")
    lista_link_avisos= []
    nomPuesto=[]
    nomUbicacion=[]
    nomEmpresa=[]
    tipoContrato=[]
    experienciaRequerido=[]
    educacionRequerido=[]
    generoRequerido=[]
    edadRequerida=[]
    cantidadVacantes=[]
    salarioPuesto=[]
    
    #repetir el numero de paginas para realizar la extración de la información
    for pagina in range(1,cantidadPaginas+1):
        url= main_url+"/"+front_url+"?t=72&page="+str(pagina)
        
        #se le manda una solicitud y se obtiene respuesta
        agent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70.'}
        main_response=requests.get(url, headers=agent,verify=False)
        
        #se obtiene todo el contenido de la pagina
        main_content=main_response.text
        
        #BeautifulSoup en lxml para que pueda ser trabajado
        main_soup=BeautifulSoup(main_content,'lxml')
        
        #buscar todas las etiquetas a con el nombre de la clase js-o-link que existen en cada aviso
        soup_url= main_soup.find_all('a',class_='ink-secondary')
        
        #agregar una lista de todos los links de los avisos que aparecen en la pagina
        
        for link_avisos in soup_url:
            lista_link_avisos.append(main_url+link_avisos['href'])
        
    
    #iterara por cada link que se encuentran en la lista y se extraera informacion para el dataframe
    for link_aviso in lista_link_avisos:
        response=requests.get(link_aviso, headers=agent)
        content=response.text
        soup=BeautifulSoup(content,'html.parser')
            
        #puesto: nombre del puesto y ubicacion
        puesto_soup= soup.find('div',class_="col-sm-12 fondo_blanco p-3 pb-0" )
        nomPuesto.append(puesto_soup.find('h1').get_text())
        nomUbicacion.append(puesto_soup.find('div',class_='col mb-1 pb-0 ms-2 ps-3 texto_azul').get_text())
        
        #descripcion: nombre de la empresa, tipo de contrato, experiencia requerida, educacion requerida, genero, cantidad de vacantrs 
        descripcion_soup=soup.find('div',class_="row p-3 pt-1 pb-1" )
        nomEmpresa.append(descripcion_soup.find_all('dd',class_='col-sm-8')[0].get_text())
        tipoContrato.append(descripcion_soup.find_all('dd',class_='col-sm-8')[2].get_text())
        experienciaRequerido.append(descripcion_soup.find_all('dd',class_='col-sm-8')[3].get_text())
        educacionRequerido.append(descripcion_soup.find_all('dd',class_='col-sm-8')[4].get_text())
        generoRequerido.append(descripcion_soup.find_all('dd',class_='col-sm-8')[5].get_text())
        if descripcion_soup.find_all('dt',class_='col-sm-4')[6].get_text() == "Edad:": 
            edadRequerida.append(descripcion_soup.find_all('dd',class_='col-sm-8')[6].get_text())
            cantidadVacantes.append(descripcion_soup.find_all('dd',class_='col-sm-8')[7].get_text())
        else: 
            cantidadVacantes.append(descripcion_soup.find_all('dd',class_='col-sm-8')[6].get_text())
            edadRequerida.append("No especifica")
            
        #salario del puesto
        salario_soup=soup.find('div',class_="row p-3 pt-1" )
        if (salario_soup is None) == False : 
            salarioPuesto.append(salario_soup.find('dd',class_="col-sm-8").get_text())
        else:
            salarioPuesto.append("No especifica")
    
    df = pd.DataFrame({'Puesto':nomPuesto,'Empresa': nomEmpresa,'Lugar': nomUbicacion, 'Tipo contrato':tipoContrato , 'Nivel de experiencia':experienciaRequerido,
                      'Nivel de estudio':educacionRequerido, 'Genero Requerido':generoRequerido, 'Edad Requerida':edadRequerida,
                      'Salario': salarioPuesto, 'Cantidad Vacante': cantidadVacantes, 'Link del Puesto': lista_link_avisos})
    
    return df
    






