# M602 Carbon Footprint Monitoring Tool

The C0<sub>2</sub> Impact generated from Personal Consumption, Waste Generation and Business Travel contributes to the overall greenhouse gas emissions - ultimately increasing global temperatures, rising sea levels with shifts in snows and rainfall patterns. The M602 Computer Programming Module aims to deliver solutions for individuals, or entities to identify their overall carbon footprint.
The CO<sub>2</sub> Monitoring tool focuses on 3 Core Elements along with their sub-elements.

### Energy Utilization
This element focuses on capturing inputs in the following areas:
1. ⚡ Electricity: The monthly residential and domestic consumption of kWh of electricity across a year.
2. 💨 Natural Gas: The monthly residential and domestic utilization of Natural Gas (LPG) sources across a year.
3. 🚗 Transportation: The monthly expenditure accrued to personal transportation means (personal motorvehicles only).

### Waste Generation
Contribution to the overall waste output of the area is a critical underlying factor in the an entities' overall C0<sub>2</sub> contribution. This is attributed purchasing and consuming non-biodegradable content, which, in turn, leads to solid waste incineration. The section receives to major components:
1. 🗑️ Waste Generation: Monthly Waste produced personally in kilograms across a year.
2. ♻️ Percentage Recycled: What is the percentage of overall waste generated consequently composted or recycled across a year.

### Business Travel
The last section of the CO<sub>2</sub> Monitoring tool looks at business and professional travel contributions to the overall individual's carbon footprint:
1. 🌍 Total Travel: Monthly residential and domestic travel contributions (in Kms) across a year.
2. ⛽ Fuel Efficiency: Respective Fuel Efficiency (on average) for each month across a year (in L/100 km).

## Introduction

The application is developed on the [Flask framework](https://flask.palletsprojects.com/en/3.0.x/) - A python web-development library to enable Backend and Frontend Web application creation using python, HTML and CSS. This is due to the utilization of the [JINJA2](https://jinja.palletsprojects.com/en/2.11.x/templates/) template engine allowing data to utilize python expressions and variables to manipulate and manage front-end templates.

<p align="center">
  <img src="https://github.com/SHA-15/M602-Carbon-Footprint-Monitoring-Tool/blob/main/readme_content/ScreenRecording2024-03-22at16.08.56-ezgif.com-video-to-gif-converter.gif">
</p>

## Installation
To clone the repository using HTTPS

```bash
git clone https://github.com/SHA-15/M602-Carbon-Footprint-Monitoring-Tool.git
```

This will install the required project dependencies to run the project

```bash
pip install -r requirements.txt
```

Move to the project's root directory and perform the following command

```python
python3 main.py
```

Output:
```
* Serving Flask app 'website'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

Use 
```
Cmd + Click
```
to run the website server
















