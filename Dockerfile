FROM python:3.10
COPY ./ /app/
WORKDIR /app
RUN pip install setuptools gunicorn dill evidently Flask jedi Jinja2 numba numpy pandas PyYAML requests scikit-learn scipy urllib3 xlrd
EXPOSE 7000
CMD gunicorn --workers=1 --bind 0.0.0.0:7000 --timeout 1500 app:app

