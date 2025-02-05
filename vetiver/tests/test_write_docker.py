import pytest
import os
import sys
import vetiver

# Load data, model
X_df, y = vetiver.get_mock_data()
model = vetiver.get_mock_model().fit(X_df, y)

def test_vetiver_write_app_no_rspm():
    py_version = str(sys.version_info.major) + "." + str(sys.version_info.minor)
    file = "Dockerfile"
    vetiver.vetiver_write_docker(rspm_env=False, path = "./")
    contents = open(file).read()
    os.remove(file)
    assert(contents == f"""# # Generated by the vetiver package; edit with care
#
FROM python:{py_version}

#
WORKDIR /code

#
COPY vetiver_requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY app.py /code/app

#
CMD ["uvicorn", "app.app:api", "--host", "0.0.0.0", "--port", "80"]
""")

def test_vetiver_write_app_rspm():
    file = "Dockerfile"
    vetiver.vetiver_write_docker(rspm_env=True, path = "./")
    contents = open(file).read()
    os.remove(file)
    py_version = str(sys.version_info.major) + "." + str(sys.version_info.minor)

    assert(contents == f"""# # Generated by the vetiver package; edit with care
#
FROM python:{py_version}

#
WORKDIR /code

#
COPY vetiver_requirements.txt /code/requirements.txt

#
RUN pip config set global.index-url https://colorado.rstudio.com/rspm/pypi/latest/simple
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY app.py /code/app

#
CMD ["uvicorn", "app.app:api", "--host", "0.0.0.0", "--port", "80"]
""")
