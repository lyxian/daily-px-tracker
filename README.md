# daily-px-tracker

Description: This app will aggregate daily stock prices into excel/csv

Goals:

- Automated daily price extraction
- Visualization
- Real-time notification
- Machine Learning integration

# V1

- description :
  - usage
    - run shell script with stocks list to scrap every minute stock prices per run (daily)
  - data management
    - write to csv
  - dashboard (v1b)
    - add dropdown list to select stock/folder, day for plotting
- requirement :
  - .

# V2

- description :
  - usage
    - save csv only if market close time is found
  - data management
    - migrate to MongoDB
  - dashboard
    > volume bar chart
    - volume table
- requirement :
  - .

# V2.1

- requirement :
  - data management
    - migrate to MongoDB
  - dashboard
    - volume table

# Fixes

> skip unresponsive stock
> update dropdown with latest file
> get missing data

##Packages (list required packages & run .scripts/python-pip.sh)
dash
plotly
pandas
pendulum
requests
##Packages
