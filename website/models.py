from flask import request 
import pandas as pd
import plotly.graph_objs as go

class CarbonFootprint:
    '''
    The Parent class that provides:

    1. List of Months as attribute
    2. Data addition from HTTP Post Request forms onto individual list, utilizing *args and **kwargs for variable datapoints
    3. Generating plots based on datapoints inserted

    '''
    def __init__(self):
        '''
        Initialize Months for Data Addition and Visualization of DataFrame Results
        '''
        self.months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    
    def data_addition(self, *datapoints ,**formfields):
        '''
        Uses the flask.requests package to attain form data and append to variable number of lists instantiated in the child class. The **formfields is to account for form data incoming from any of the three forms in the application and append to each Child Class's list object
        '''
        for data, value in zip(datapoints, formfields.values()):
            data.append(request.form.get(f"{value}_{self.months[0]}"))
            data.append(request.form.get(f"{value}_{self.months[1]}"))
            data.append(request.form.get(f"{value}_{self.months[2]}"))
            data.append(request.form.get(f"{value}_{self.months[3]}"))
            data.append(request.form.get(f"{value}_{self.months[4]}"))
            data.append(request.form.get(f"{value}_{self.months[5]}"))
            data.append(request.form.get(f"{value}_{self.months[6]}"))
            data.append(request.form.get(f"{value}_{self.months[7]}"))
            data.append(request.form.get(f"{value}_{self.months[8]}"))
            data.append(request.form.get(f"{value}_{self.months[9]}"))
            data.append(request.form.get(f"{value}_{self.months[10]}"))
            data.append(request.form.get(f"{value}_{self.months[11]}"))

        return
    
    def dataframe_production(self, *datapoints, **column_names):
        '''
        Utilizing the created and data-filled Child Class lists to generate dataframe object. Using *args and **kwargs to allow variability in datapoints being used
        '''
        dataframe_object = pd.DataFrame({
            "month": self.months,
        })

        for data, header in zip(datapoints, column_names.values()):
            dataframe_object[header] = data

        return dataframe_object

    def max_id(self, df):
        max_id = df[df.columns[-1]].idxmax()

        return max_id

    def max_carbon_impact(self, df):
       impact_column =  df.columns[-1]
       max_value = df[impact_column].max()

       return max_value

    def max_month(self, df):
        max_month = df.loc[self.max_id(df), 'month']

        return max_month

    def generate_plot(self, list_name, df, title, legend, color=["blue", "yellow"]):
        '''
        Generating Histogram charts using plotly.graphobjects package for each dataframe object
        '''
        fig = go.Figure()

        for id in range(len(list_name)):
            fig.add_trace(go.Histogram(histfunc="sum", y=df[list_name[id]], x=df["month"], name=legend[id], marker_color=color[id]))

        fig.update_layout(
            template="plotly_dark",
            title_text = title)

        return fig
    
class EnergyConsumption(CarbonFootprint):
    '''
    Energy Consumption Child Class that identifies the electric, natural gas and fuel consumption data points
    '''
    def __init__(self):
        '''Initialize individual arrays for each question response'''
        super().__init__()
        self.electricity = []
        self.natural_gas = []
        self.transportation = []
    
    def energy_calculation(self): 
        '''
        Uses the raw data inputted into the lists and are converted into formula values as per each metric requirements. Converts string data format input into floating point numbers and allows empty data conversion into numeric data using error-handling

        RETURNS
        ------------
        Floating point  and arithmetic performance on each list element and reassigned to same index. 
        ''' 
        #Appending data from the HTML form onto the individual data point lists
        self.data_addition(self.electricity, self.natural_gas, self.transportation, key1="elec", key2="gas", key3="fuel")
        
        #Conversion of all datapoints into floating point numbers and calculation points
        for index in range(len(self.months)):
            try:
                if self.electricity[index] != '':
                    self.electricity[index] = round(float(self.electricity[index]) * 12 * 0.0005, 2)
                else:
                    self.electricity[index] = 0.00
                if self.natural_gas[index] != '':
                    self.natural_gas[index] = round(float(self.natural_gas[index]) * 12 * 0.0053, 2)
                else:
                    self.natural_gas[index] = 0.00
                if self.transportation[index] != '':
                    self.transportation[index] = round(float(self.transportation[index]) * 12 * 2.32, 2)
                else:
                    self.transportation[index] = 0.00
            except ValueError:
                self.electricity[index] = 0.00                
                self.natural_gas[index] = 0.00
                self.transportation[index] = 0.00

        return
    
    def energy_data_aggregation(self):
        '''
        Generate the overall data for each row record into new df aggregate column
        '''
        energy_df = self.dataframe_production(self.electricity, self.natural_gas, self.transportation, col1="electricity_consumption", col2="natural_gas_consumption", col3="transport_utilization")

        energy_df['total_energy'] = energy_df['electricity_consumption'] + energy_df['natural_gas_consumption'] + energy_df['transport_utilization']

        return energy_df

    def max_outputs(self, df):
        '''
        Identify the larget contributor towards Carbon Footprint Energy Consumption By Month.
        '''
        max_fuel = df['transport_utilization'].max()
        max_elec = df['electricity_consumption'].max()
        max_gas = df['natural_gas_consumption'].max()
        max_fuel_month = df.loc[df['transport_utilization'].idxmax(), 'month']
        max_elec_month = df.loc[df['electricity_consumption'].idxmax(), 'month']
        max_gas_month = df.loc[df['natural_gas_consumption'].idxmax(), 'month']

        return max_fuel, max_fuel_month, max_elec, max_elec_month, max_gas, max_gas_month

class WasteConsumption(CarbonFootprint):
    '''
    Carbon Footprint Child Class that manages the waste production and recycling metrics for identification
    '''
    def __init__(self):
        super().__init__()
        self.waste_generation = []
        self.waste_recycling_pct = []
    
    def waste_accumulation(self):
        '''
        Uses the raw data inputted into the lists and are converted into formula values as per each metric requirements. Converts string data format input into floating point numbers and allows empty data conversion into numeric data using error-handling

        RETURNS
        ------------
        Floating point  and arithmetic performance on each list element and reassigned to same index. 
        ''' 
        self.data_addition(self.waste_generation, self.waste_recycling_pct, key1="waste", key2="percent")

        for index in range(len(self.months)):
            try:
                self.waste_generation[index] = round(float(self.waste_generation[index]), 2)
                self.waste_recycling_pct[index] = round(float(self.waste_recycling_pct[index]), 2)
            except:
                if self.waste_generation[index] == '':
                    self.waste_generation[index] = 0.00
                if self.waste_recycling_pct[index] == '':
                    self.waste_recycling_pct[index] = 0.00

        return

    def waste_data_aggregation(self):
        '''
        Generate the overall data for each row record into new df aggregate column
        '''
        waste_df = self.dataframe_production(self.waste_generation, self.waste_recycling_pct, col1="waste_generation", col2="waste_recycling_percentage")

        # Calculate the Carbon Footprint impact in kgCO2 from Waste
        waste_df['total_waste'] = (waste_df['waste_generation'] * 12) * (0.57 - (waste_df['waste_recycling_percentage']/100))

        return waste_df

    def max_efficiency(self, df):
        '''
        Based on Parent Class .max_carbon_impact() method. Given the index of max impact, identify its subsequent recycling efficiency.
        '''
        max_efficiency = df.loc[self.max_id(df), 'waste_recycling_percentage']

        return max_efficiency

    def optimum_efficiency(self, df):
        '''
        Identify maximum recycling contribution made across inputs of range N (specified per month)

        RETURNS
        _______
        The max value and max_month from waste_df
        '''
        opt_eff_id = df['waste_recycling_percentage'].idxmax()
        opt_eff = df.loc[opt_eff_id, 'waste_recycling_percentage']
        opt_month = df.loc[opt_eff_id, 'month']

        return opt_eff, opt_month

class BusinessTravel(CarbonFootprint):
    '''
    Capture the business travel expenditure of individual including fuel efficiency
    '''
    def __init__(self):
        super().__init__()
        self.business_travel_in_kms = []
        self.fuel_efficiency = []

    def transportation_impact(self):
        '''
        Uses the raw data inputted into the lists and are converted into formula values as per each metric requirements. Converts string data format input into floating point numbers and allows empty data conversion into numeric data using error-handling

        RETURNS
        ------------
        Floating point  and arithmetic performance on each list element and reassigned to same index. 
        ''' 
        self.data_addition(self.business_travel_in_kms, self.fuel_efficiency, key1="fuel", key2="efficiency")

        for index in range(len(self.months)):
            try:
                if self.business_travel_in_kms[index] != '':
                    self.business_travel_in_kms[index] = round(float(self.business_travel_in_kms[index]), 2)
                else:
                    self.business_travel_in_kms[index] = 0.00
                if self.fuel_efficiency[index] != '':
                    self.fuel_efficiency[index] = round(float(self.fuel_efficiency[index]), 2)
                else:
                    self.fuel_efficiency[index] = 0.00
            except ValueError:
                self.business_travel_in_kms[index] = 0.00
                self.fuel_efficiency[index] = 0.00

        return
    
    def transport_data_aggregation(self):
        '''
        Generate the overall data for each row record into new df aggregate column
        '''
        business_travel_df = self.dataframe_production(self.business_travel_in_kms, self.fuel_efficiency, col1='business_travel', col2='fuel_efficiency')
        try:
            business_travel_df['total_travel'] = (business_travel_df['business_travel'] * (1 / business_travel_df['fuel_efficiency']) * 2.31) / 12
        except:
            business_travel_df['total_travel'] = 0

        # Convert NaN values to zeros
        business_travel_df['total_travel'] = business_travel_df['total_travel'].fillna(0)

        return business_travel_df