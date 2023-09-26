#importamos las librerias necesarias
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import time
import streamlit as st
import matplotlib.pyplot as plt
    

#aca comienza la visualizacion con streamlit
import streamlit as st 

# lectura de los datos y carga a la variable data_mk
data_mk1 = pd.read_csv("marketing_AB.csv")

# titulo y encabezado
st.title("A/B Estudio De Marketing 📈")
st.subheader(" _Herramientas: Python y Streamlit_")
st.write("Realizamos un estudio A/B, que es un proceso de experimentaición aleatorio en el que dos o más versiones de una variable (página web, elemento de página, banner, etc.) se muestran a diferentes segmentos de personas al mismo tiempo para determinar qué versión. deja el máximo impacto e impulsa las métricas comerciales. Se buscó responder las preguntas como, ¿tuvo éxito la campaña? Y si tuvo éxito, ¿cuanto de ese éxito es por anuncios?. La idea fue analizar los grupos, encontrar si los anuncios tuvieron éxito y si la diferencia entre los grupos es significativa.")


st.sidebar.header("Elegí las opciones:")


# confianza del sidebar
confianza_costado = st.sidebar.radio('Elegí el grado de confianza:', [0.95, 0.99, 0.90])

# muestra del sidebar
max_filas=data_mk1.shape[0]
muestra_costado = st.sidebar.slider("Elegí el tamaño de la muestra", min_value=0, max_value=max_filas)
data_mk = data_mk1.sample(n = muestra_costado, replace = True)


if confianza_costado == 0.99:
    alphavalor = 0.01
elif confianza_costado == 0.95:
    alphavalor = 0.05
else:
    alphavalor = 0.10

st.sidebar.metric(label="Alpha", value=alphavalor)           

st.sidebar.caption("El dataset utilizado cuenta con Licencia CCO Public Domain.")
st.sidebar.markdown("[Consulta el DataSet](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing?resource=download)")

# grafico psa y ad
tipo_converted=data_mk.groupby(by=["test group"]).count()["user id"]
array_datos= np.array(tipo_converted)
llaves_etiquetas=tipo_converted.keys()


fig, ax = plt.subplots(figsize=(30,6))
ax.pie(tipo_converted, labels=llaves_etiquetas, autopct='%1.1f%%', colors=["grey","purple"],shadow=True)

col1, col2 = st.columns(2)
with col1:
    st.write("Realizamos un gráfico de torta: donde ad=son las personas que vieron el anuncio, y psa= solo vieron el anunico público.")
    st.pyplot(fig, use_container_width=True)


#quienes compraron y vieron el anuncio, vamos a hacer el grafico 1.
tipo_cliente=data_mk.groupby(by=["converted","test group"])["user id"].count()
keysvar=tipo_cliente.keys()
arreylab_com = []


for llave in keysvar:
    if llave[0] == False:
        convierte = "no compro"
    else:
        convierte = "compro"    
    arreylab_com.append(convierte + "_" + llave[1])


arreydato_com = []

for dato in tipo_cliente: 
    arreydato_com.append(dato)
    


#vamos a hacer el grafico 2.
fig1, ax1 = plt.subplots(figsize=(30,6))
ax1.pie(arreydato_com, labels=arreylab_com, autopct='%1.1f%%', colors=["grey","pink"],shadow=True)

    
with col2:
    
    st.write("Hemos creado un segundo gráfico circular que muestra las distintas categorías de interacción de los usuarios con los anuncios.")
    st.pyplot(fig1, use_container_width=True)

#Renombro columnas
data_mk.rename(columns=lambda col: col.strip().replace(" ","_"),inplace=True)
data_mk["converted"] = data_mk["converted"].astype(int)

tratamiento_ad = data_mk.query('test_group == "ad"')
control_psa = data_mk.query('test_group == "psa"')

tasa_trat = str(round((tratamiento_ad['converted'].mean())*100, 0)) + "%"
tasa_controlpsa = str(round(control_psa['converted'].mean()*100, 0)) + "%"
tasa_datamk = str(round(data_mk['converted'].mean()*100, 0)) + "%"


#vamos a hacer kpi de conversion.
st.header("Tasa de conversión")
col1, col2, col3= st.columns(3)

with col1:
    st.metric('Conversión AD', tasa_trat, ) 
with col2:
    st.metric('Conversión PSA', tasa_controlpsa, ) 
with col3:
    st.metric('Conversión Total', tasa_datamk, )

st.info("¿Es la tasa de conversión ad lo suficientemente significativa respecto a la de conversión psa? Para esto realizamos la prueba de hipotesis en base a los datos seleccionados por el usuario en el lado izquierdo de la página")
st.header("Análsis A/B Final")



### Definición de hipotesis:
st.write("H0= No existen diferencias entre si vió el anuncio o no vió el anuncio.")
st.write("H1= Si existen diferencias entre si vió el anuncio y no vió el anuncio.")


con_ad=len(tratamiento_ad.query('converted == 1'))
total_vis=len(tratamiento_ad)
c_psa=len(control_psa.query('converted == 1'))
total_novis=len(control_psa) 


array_convirtio=np.array([con_ad, c_psa])
array_visualiza=np.array([total_vis, total_novis])


#calculos con ztest en ambas direcciones
pvalor= proportions_ztest(count=array_convirtio, nobs=array_visualiza)[1]
tvalor=proportions_ztest(count=array_convirtio, nobs=array_visualiza)[0]

st.write("Se deja el parametro 'alternative' que plantea por defecto probar si hay una diferencia signficativa en ambas direcciones.")

table = {
    "pvalor": pvalor,
    "tvalor": tvalor
}

st.dataframe(table)


st.subheader("Resultado del Z test")

if pvalor<alphavalor:
    st.success("Rechazo H0: se confirma que los que vieron el anuncio compraron más")
else: 
    st.warning("No rechazo H0: no existe evidencia estadistica que nos confrime que ver el anuncio impacte a que compren más")







 

