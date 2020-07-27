# Anomaly Viewer
Anomaly Viewer helps you find anomalous data points in csv files.

## Dependencies
This project depends on scikit-learn, pandas and bokeh.
```batch
pip3 install sklearn
pip3 install pandas
pip3 install bokeh
```

## How to get Anomaly Viewer
```batch
git clone https://github.com/arturmiller/anomaly_viewer.git
```

## Create example datasets
The Anomaly Viewer has to fed with a dataset in csv format. Two example datasets have been made available, Boston housing prices and digits. The original datasets are provided by scikit-learn.  
You get the Boston house price dataset by running following executable:

```batch
python3 boston.py
```

The Boston house price dataset doesn't show the feature, that data points can link to files with further information. The digits dataset shows the digits as images if you click at the "show selected" button.

```batch
python3 digits.py
```

## Run Anomaly Viewer
```batch
bokeh serve --show  anomaly_viewer.py --args boston.csv
```
