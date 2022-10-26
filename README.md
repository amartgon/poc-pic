# Prueba de Concepto PIC


### Script de carga de datos
* Script de carga de datos [load_data.py](load_data.py)


### Código para prueba de rendimiento de consultas
* [mongolocust/](mongolocust), basado en [https://github.com/sabyadi/mongolocust](https://github.com/sabyadi/mongolocust)
* Para instalar las bibliotecas de Python requeridas:
```shell
cd mongolocust
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Consultas calientes
```shell
./run_distributed_locust_warm.sh
```

### Consultas frías

* Para ejecutar la prueba de carga de consultas frías:
```shell
locust -f load_test_archive.py
```
* Consulta de intervalo de 1 mes:
```shell
locust -f load_test_archive_30d.py
```
* Consulta de intervalo de 3 meses:
```shell
locust -f load_test_archive_90d.py
```

