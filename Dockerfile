FROM bitnami/spark:3.5.0

USER root

RUN pip install pandas
RUN pip install scikit-learn
RUN pip install mysql-connector-python