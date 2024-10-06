import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40}),
    html.Br(),
    html.Div([
        html.Label('Select Launch Site:'),
        dcc.Dropdown(id='site-dropdown',
                      options=[{'label': 'All Sites', 'value': 'All'}] +
                              [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                      value='All',
                      placeholder="Select a launch site",
                      searchable=True)
    ]),
    
    # Placeholder for success-pie-chart
    html.Div([dcc.Graph(id='success-pie-chart')]),
    
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    # Range slider to select payload range
    html.Div([
        dcc.RangeSlider(id='payload-slider',
                         min=0, max=10000, step=1000,
                         marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1000, 1000)},
                         value=[min_payload, max_payload])
    ]),
    
    html.Br(),
    
    # Placeholder for success-payload-scatter-plot
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart')
    ]),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'All':
        success_counts = spacex_df.groupby('Launch Site')['class'].value_counts().reset_index()
        success_counts.columns = ['Launch Site','success','Count']
        fig = px.pie(success_counts, values='Count', names='Launch Site', color='Launch Site',
                      title='Overall Success Rate')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['Launch Site', 'Count']
        fig = px.pie(success_counts, values='Count', names='Launch Site',
                      title=f'Success Rate at {entered_site}')
    
    return fig

@app.callback(
        Output(component_id='success-payload-scatter-chart', component_property='figure'),
        [Input(component_id='site-dropdown', component_property='value'), 
         Input(component_id="payload-slider", component_property="value")])

def update_success_payload_scatter_plot(selected_site,payload_range):
    min_payload, max_payload = payload_range
    
    if selected_site == 'All':
        # Filtered data for all sites within the payload range
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & (spacex_df['Payload Mass (kg)'] <= max_payload)]
        
        # Rendered scatter plot with all values for variable Payload Mass (kg) and variable class
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version', 
                         title=f'Success vs Payload for All Sites and Payload Range [{min_payload}, {max_payload}]')
        
    else:
        # Filtered data for specific site within the payload range
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                                (spacex_df['Payload Mass (kg)'] <= max_payload) & 
                                (spacex_df['Launch Site'] == selected_site)]
        
        # Rendered scatter plot with values for variable Payload Mass (kg) and variable class
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version', 
                         title=f'Success vs Payload at {selected_site}')
    
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
