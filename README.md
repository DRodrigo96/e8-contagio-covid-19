# Perú: Contagio COVID-19

---

## Description
Un mapa interactivo de contagiados por COVID-19 a nivel distrital usando la información del portal de datos abiertos de Perú.

---

## Fuentes
* `COORDENADAS_DISTRITAL.csv`: coordendas distritales para Perú ([fuente](https://www.geogpsperu.com/2014/03/base-de-datos-peru-shapefile-shp-minam.html)).
* `positivos_covid.csv`: dataset con casos de COVID-19 ([fuente](https://www.datosabiertos.gob.pe/dataset/casos-positivos-por-covid-19-ministerio-de-salud-minsa)).
* Snippets: [Vadim Gremyachev](https://stackoverflow.com/users/1375553/vadim-gremyachev), [InLaw](https://stackoverflow.com/users/7084278/inlaw).

---

## Ejecución
Se recomienda instalar el gestor `conda` y ejecutar los siguientes comandos.
```bash
conda create -n venv python=3.9
conda activate venv
pip3 install -r requirements.txt
jupyter-notebook
```

---

La ejecución del notebook fue revisada hasta la fecha: September 5th, 2021.
