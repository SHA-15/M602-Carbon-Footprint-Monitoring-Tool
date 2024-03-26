from .models import EnergyConsumption, WasteConsumption, BusinessTravel
from flask import Blueprint, render_template, request, session, make_response
import pdfkit
import plotly.io as pio


carbon_footprint = Blueprint('carbon_footprint', __name__)

@carbon_footprint.route('/', methods=["GET", "POST"])
def home():
    '''
    Instantiate the opening section of the website for the user
   
    Returns
    _________
    The home page of the website
    '''
    
    return render_template("home.html")

@carbon_footprint.route("/energy", methods=["GET", "POST"])
def energy():
    '''
    Respond to HTTP POST request for addition and submission of form data
    
    Instantiates the EnergyConsumption() class
    Converts produced form data to a DataFrame object using .dataframeproduction() methods
    Produces Visualization of the input results using the .generate_plot() method

    HTTP REQUEST 'GET' generates home page
    '''
    if request.method == 'POST':
        #Applicable condition if first form clicked
        if "energy-button" in request.form:
            # Instantiate the EnergyConsumption class
            energy_consumption = EnergyConsumption()
            
            # Add the form data and and perform calculation
            energy_consumption.energy_calculation()

            print(type(energy_consumption.electricity), type(energy_consumption.natural_gas), type(energy_consumption.transportation))
            # Push form data onto the dataframe and setup total consumption column
            energy_df = energy_consumption.energy_data_aggregation()

            print(energy_df.head(12))

            # Identify the overall contribution of electricity, gas and fuel for the year
            elec_gas_impact = energy_df['electricity_consumption'].sum() + energy_df['natural_gas_consumption'].sum()

            fuel_impact = energy_df['transport_utilization'].sum()

            overall_impact = energy_df['total_energy'].sum()

            # Capture Max values and months to find opportunities for improvement
            max_fuel, max_fuel_month, max_elec, max_elec_month, max_gas, max_gas_month = energy_consumption.max_outputs(energy_df)

            # Capture Max Carbon Impact across the Energy Consumption and their respective Elec, Fuel and Gas contribution
            max_carbon_impact = energy_consumption.max_carbon_impact(energy_df)
            max_carbon_impact_month = energy_consumption.max_month(energy_df)
            max_carbon_elec = energy_df.loc[energy_consumption.max_id(energy_df), 'electricity_consumption']
            max_carbon_gas = energy_df.loc[energy_consumption.max_id(energy_df), 'natural_gas_consumption']
            max_carbon_fuel = energy_df.loc[energy_consumption.max_id(energy_df), 'transport_utilization']

            # Plotting given values against each DataFrame Relationship     
            fig1 = energy_consumption.generate_plot(['electricity_consumption', 'natural_gas_consumption'], energy_df, "Electricity & Natural Gas Utilization",['Electricity Consumption', 'Natural Gas Consumption'], ['cyan', 'yellow'])

            fig2 = energy_consumption.generate_plot(["transport_utilization"], energy_df, "Fuel Utilization Summary",["Transport Fuel Consumption"], ['white'])
        
            fig3 = energy_consumption.generate_plot(['total_energy'], energy_df, "Overall Energy Consumption Impact", ["Summation of Electricity, Natural Gas and Fuel Utlization"],['magenta'])

            # Figures to Vector Format Conversion
            svg1 = pio.to_image(fig1, format="svg")
            svg_fig1 = svg1.decode("UTF-8")
            svg2 = pio.to_image(fig2, format="svg")
            svg_fig2 = svg2.decode("UTF-8")
            svg3 = pio.to_image(fig3, format="svg")
            svg_fig3 = svg3.decode("UTF-8")

            session['elec_gas_impact'] = round(elec_gas_impact, 2)
            session['fuel_impact'] = round(fuel_impact, 2)
            session['overall_impact'] = round(overall_impact, 2)
            session['max_elec'] = round(max_elec, 2)
            session['max_elec_month'] = max_elec_month.capitalize()
            session['max_gas'] = round(max_gas, 2)
            session['max_gas_month'] = max_gas_month.capitalize()
            session['max_fuel'] = round(max_fuel, 2)
            session['max_fuel_month'] = max_fuel_month.capitalize()
            session['max_carbon_impact'] = round(max_carbon_impact, 2)
            session['max_carbon_impact_month'] = max_carbon_impact_month.capitalize()
            session['max_carbon_elec'] = round(max_carbon_elec, 2)
            session['max_carbon_gas'] = round(max_carbon_gas, 2)
            session['max_carbon_fuel'] = round(max_carbon_fuel, 2)             
            session['months'] = energy_consumption.months
            session['svg_fig1'] = svg_fig1
            session['svg_fig2'] = svg_fig2
            session['svg_fig3'] = svg_fig3

            return render_template("data.html")

    render_template("home.html")

@carbon_footprint.route("/waste-generation", methods=["GET", "POST"])
def waste():
    '''
    Respond to HTTP POST request for addition and submission of form data
    
    Instantiates the WasteConsumption() class
    Converts produced form data to a DataFrame object using .dataframeproduction() methods
    Produces Visualization of the input results using the .generate_plot() method

    HTTP REQUEST 'GET' generates home page
    '''
    if request.method == 'POST':
        if "waste-button" in request.form:
            
            waste_generation = WasteConsumption()

            waste_generation.waste_accumulation()

            waste_df = waste_generation.waste_data_aggregation()

            print(waste_df.head(12))

            #Provides the total yearly Carbon Footprint impact from waste management and recycling in KgCO2
            waste_impact = round(waste_df['total_waste'].sum(), 2)

            # Find maximum waste production month, its efficiency and value using Carbon Footprint Helper Methods
            max_waste = round(waste_generation.max_carbon_impact(waste_df), 2)
            max_month = waste_generation.max_month(waste_df)
            max_efficiency = round(waste_generation.max_efficiency(waste_df), 0)

            # Identify Overall efficiency for Second Plot and capture trend in efficiency
            optimum_efficiency, optimum_month = waste_generation.optimum_efficiency(waste_df)

            # Identify waste differentials across each impact
            waste_df['impact_differential'] = waste_df['total_waste'].diff()
            waste_df['waste_differential'] = waste_df['waste_generation'].diff()
            waste_df['eff_differential'] = waste_df['waste_recycling_percentage'].diff()

            waste_df['impact_differential'][0] = 0
            waste_df['waste_differential'][0] = 0
            waste_df['eff_differential'][0] = 0

            max_differential = waste_df['impact_differential'].max()
            max_diff_id = waste_df['impact_differential'].idxmax()
            max_diff_month = waste_df.loc[max_diff_id, 'month']
            max_diff_waste = waste_df.loc[max_diff_id, 'waste_differential']
            max_diff_eff = waste_df.loc[max_diff_id, 'eff_differential']
            
            min_differential = waste_df['impact_differential'].min()
            min_diff_id = waste_df['impact_differential'].idxmin()
            min_diff_month = waste_df.loc[min_diff_id, 'month']
            min_diff_waste = waste_df.loc[min_diff_id, 'waste_differential']
            min_diff_eff = waste_df.loc[min_diff_id, 'eff_differential']


            print(waste_df.head(12))

            # Plot each graph element for the relationships within the dataframe
            fig1 = waste_generation.generate_plot(["waste_generation"], waste_df, "Overall Waste Generation From Consumption",['Waste Production'], ['purple'])

            fig2 = waste_generation.generate_plot(["waste_recycling_percentage"], waste_df, "Waste Composting and Recyclability",["Waste Recycling Effectiveness"], ['orange'])
        
            fig3 = waste_generation.generate_plot(['total_waste'], waste_df, "Overall Waste Contribution", ["Overall Waste Impact"], ['yellow'])

            svg1 = pio.to_image(fig1, format="svg")
            svg_fig1 = svg1.decode("UTF-8")
            svg2 = pio.to_image(fig2, format="svg")
            svg_fig2 = svg2.decode("UTF-8")
            svg3 = pio.to_image(fig3, format="svg")
            svg_fig3 = svg3.decode("UTF-8")

            # Setting up session variables to plot within HTML templates
            session['waste_impact'] = waste_impact
            session['svg_fig1'] = svg_fig1
            session['svg_fig2'] = svg_fig2
            session['svg_fig3'] = svg_fig3
            session['max_waste'] = max_waste
            session['max_month'] = max_month.capitalize()
            session['max_efficiency'] = max_efficiency
            session['optimum_efficiency'] = round(optimum_efficiency, 0)
            session['optimum_month'] = optimum_month.capitalize()
            session['max_differential'] = round(max_differential, 2)
            session['max_diff_month'] = max_diff_month
            session['max_diff_waste'] = round(max_diff_waste, 2)
            session['max_diff_eff'] = round(max_diff_eff, 2)
            session['differential'] = round(max_differential, 2) - round(min_differential, 2)
            session['min_diff_month'] = min_diff_month
            session['diff_waste'] = round(max_diff_waste, 2) - round(min_diff_waste, 2)
            session['diff_eff'] = round(max_diff_eff, 2) - round(min_diff_eff, 2)

            return render_template("waste.html")
        
    return render_template("home.html")

@carbon_footprint.route("/business-travel", methods=["GET", "POST"])
def travel():
    ''' 
    Respond to HTTP POST request for addition and submission of form data
    
    Instantiates the BusinessTravel() class
    Converts produced form data to a DataFrame object using .dataframeproduction() methods
    Produces Visualization of the input results using the .generate_plot() method

    HTTP REQUEST 'GET' generates home page
    '''
    if request.method == "POST":
        if "business-button" in request.form:
            # Instantiate the Business Travel Class
            business_travel = BusinessTravel()
            # Receive all datapoints from the web form on to the objects attributes
            business_travel.transportation_impact()
            # Mapp all data onto the dataframe
            travel_df = business_travel.transport_data_aggregation()
            # Terminal Test print
            print(travel_df.head(12))
            print(type(travel_df['business_travel'][0]), type(travel_df['fuel_efficiency'][0]),type(travel_df['total_travel'][0]))

            # Identify total impact of business travel and corresponding contributors to the max value
            total_travel_impact = round(travel_df['total_travel'].sum(), 2)
            total_travel_month = travel_df.loc[business_travel.max_id(travel_df), 'month']
            total_travel_distance = travel_df.loc[business_travel.max_id(travel_df), 'business_travel']
            total_travel_efficiency = travel_df.loc[business_travel.max_id(travel_df), 'fuel_efficiency']

            # Calculate Max Efficiency achieve and corresponding values across dataframe
            max_fuel_efficiency = travel_df['fuel_efficiency'].max()
            max_fuel_eff_month = travel_df.loc[travel_df['fuel_efficiency'].idxmax(), 'month']

            # Calculate total distance travelled and corresponding dataframe values
            total_km= round(travel_df['business_travel'].sum())
            total_km_max = round(travel_df['business_travel'].max())
            total_km_max_month = travel_df.loc[travel_df['business_travel'].idxmax(), 'month']

            # Identify the total liters of fuel consumed across each month
            travel_df['monthly_liter_output'] = travel_df['business_travel'] * travel_df['fuel_efficiency']

            # #Find Liters of fuel consumed
            total_liter = travel_df.loc[travel_df['business_travel'].idxmax(), 'monthly_liter_output']
            liter_output_impact = travel_df['monthly_liter_output'].sum()

            # print(travel_df.head(12))

            # Using plotly to create histogram objects for visualization
            fig1 = business_travel.generate_plot(["business_travel"], travel_df, "Total Business Kilometers Travelled",["Business Travel"], ['green'])

            fig2 = business_travel.generate_plot(["fuel_efficiency"], travel_df, "Transport Mode Fuel Efficiency",["Fuel Efficiency"], ['yellow'])
        
            fig3 = business_travel.generate_plot(['total_travel'], travel_df, "Overall Business Travel Impact", ["Monthly Travel Impact"], ['cyan'])

            svg1 = pio.to_image(fig1, format="svg")
            svg_fig1 = svg1.decode("UTF-8")
            svg2 = pio.to_image(fig2, format="svg")
            svg_fig2 = svg2.decode("UTF-8")
            svg3 = pio.to_image(fig3, format="svg")
            svg_fig3 = svg3.decode("UTF-8")            

            # Store all output variables in browser cookies for usage in templates and other webpages through the browser
            session['months'] = business_travel.months
            session['total_km'] = total_km
            session['total_km_max'] = total_km_max
            session['total_km_max_month'] = total_km_max_month
            session['total_liter'] = round(total_liter, 1)
            session['total_fuel_impact'] = total_travel_impact
            session['total_travel_month'] = total_travel_month
            session['total_travel_distance'] = total_travel_distance
            session['total_travel_efficiency'] = total_travel_efficiency
            session['max_fuel_efficiency'] = round(max_fuel_efficiency, 2)
            session['max_fuel_eff_month'] = max_fuel_eff_month
            session['liter_output_impact'] = liter_output_impact
            session['svg_fig1'] = svg_fig1
            session['svg_fig2'] = svg_fig2
            session['svg_fig3'] = svg_fig3

            return render_template("travel.html")

    return render_template("home.html")


# Yet to yield completion and generate PDF report
@carbon_footprint.route("/energy-pdf")
def energy_pdf():
    html = render_template('data.html')
    pdf = pdfkit.from_string(html, False,  css='website/static/css/template.css' ,options={'enable-local-file-access': ''})

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=energy.pdf'

    return response

@carbon_footprint.route("/waste-pdf")
def waste_pdf():
    html = render_template('waste.html')
    pdf = pdfkit.from_string(html, False, css='website/static/css/template.css', options={'enable-local-file-access': ''})

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=waste.pdf'

    return response

@carbon_footprint.route("/travel-pdf")
def travel_pdf():
    html = render_template('travel.html')
    pdf = pdfkit.from_string(html, False, css='website/static/css/template.css', options={'enable-local-file-access': ''})

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=travel.pdf'

    return response