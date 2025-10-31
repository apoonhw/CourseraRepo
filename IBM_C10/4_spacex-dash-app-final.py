#IBM Applied Data Science Capstone - Module 3 - By Aki

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#Preprocess the data
mapped_spacex_df = spacex_df
Result_map = {0:'Unsuccessful Launch', 1:'Successful Launch'}
mapped_spacex_df['Result'] = mapped_spacex_df['class'].map(Result_map)

# Create a dash application
app = dash.Dash(__name__)

# Create app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
    style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
    ),
    html.Br(),
    #Task 1: Launch site drop-down input component
    html.Div(dcc.Dropdown(
        id='site-dropdown', 
        options=[
            {'label':'All Sites', 'value':'ALL', 'title':'All launch sites'},
            {'label':'CCAFS LC-40', 'value':'CCAFS LC-40', 'title':'Cape Canaveral Air Force Station - Launch Complex 40'},
            {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40', 'title':'Cape Canaveral Air Force Station - Space Launch Complex 40'},
            {'label':'KSC LC-39A', 'value':'KSC LC-39A', 'title':'Kennedy Space Centre Launch Complex 39A'},
            {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E', 'title':'Vandenberg Space Force Base Special Launch Complex 4 East'}
        ],
        value='ALL',
        placeholder='Select a SpaceX Launch Site here', 
        searchable=True),
        style={'font-size':20}
        ),
    html.Br(),
    #Task 2: Output container for the pie plot; (Optional) responsive attribute controls whether the plot is responsive to window resizing
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    #Task 3: Payload range slider component
    html.P('Payload range (Kg):', style={'textAlign':'left', 'font-weight':'bold','font-size':20}),
    html.Div(dcc.RangeSlider(
        id='payload-slider',
        min=0, max = 10000, step=1000,
        value=[min_payload, max_payload],
        tooltip={
            'placement':'top',
            'always_visible':False},
        allowCross=False), 
        style={'font-size':20, 'font-weight':'bold'}
        ),
    html.Br(),
    #Task 4: Output container for the scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    html.Br()
    ])

#Create callbacks

#Task 2 - Call back function for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))    
def get_pie_chart(selected_site):      #input arguments of the callback --> values of the input in the order they are specified
    #Check filtering type
    if selected_site == 'ALL':
        filtered_df = mapped_spacex_df
        pie_categories = 'Launch Site'
        pie_data = filtered_df.groupby(pie_categories)['class'].sum().reset_index()
        pie_title = 'Total Success Launches by Site' 
    else:
        filtered_df = mapped_spacex_df[mapped_spacex_df['Launch Site'] == selected_site]
        pie_categories = 'Result'
        pie_data = filtered_df.groupby(pie_categories)['class'].count().reset_index()
        pie_title = 'Total Success Launches for Site {}'.format(selected_site)
    #Plot the figure
    success_pie = px.pie(
        pie_data,
        values = 'class',
        names = pie_categories,
        title = pie_title
        )
    return success_pie

#Task 4 - Call back function for scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(selected_site, selected_payload_range):
    #Check filtering type
    if selected_site == 'ALL':
        filtered_df = mapped_spacex_df 
        scatter_title = 'Correlation between Payload and Launch Outcomes for all sites' 
    else:
        filtered_df = mapped_spacex_df[mapped_spacex_df['Launch Site'] == selected_site]
        scatter_title = 'Correlation between Payload and Launch Outcomes for Site {}'.format(selected_site)  
    #plot the figure
    scatter_data = filtered_df
    success_scatter = px.scatter(
        scatter_data,
        x = 'Payload Mass (kg)',
        y = 'class',
        color= 'Booster Version Category',
        hover_name = 'Flight Number',
        hover_data = ['Launch Site','Payload Mass (kg)','Booster Version','Result'],
        title = scatter_title,
        range_x = selected_payload_range,
        labels={'Payload Mass (kg)': 'Payload Mass in kg','class':'Launch outcome (0= Failed; 1= Succeeded)','Booster Version Category':'Booster Ver. Category'}
        )
    return success_scatter

# Run the app
if __name__ == '__main__':
    app.run(debug=True)