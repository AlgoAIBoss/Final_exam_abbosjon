import pandas as pd
import sqlite3
from pandaserd import ERD
from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go

### EXERCISE NUMBER 1
conn = sqlite3.connect("./assets/hr")
regions = pd.read_sql_query("select * from regions;", conn)
countries = pd.read_sql_query("select * from countries;", conn)
locations = pd.read_sql_query("select * from locations;", conn)
departments = pd.read_sql_query("select * from departments;", conn)
employees = pd.read_sql_query("select * from employees;", conn)
jobs = pd.read_sql_query("select * from jobs;", conn)
job_history = pd.read_sql_query("select * from job_history;", conn)


erd = ERD()
regions_table = erd.add_table(regions, 'regions', bg_color='pink')
countries_table = erd.add_table(countries, 'countries', bg_color='skyblue')
locations_table = erd.add_table(locations, 'locations', bg_color='lightblue')
departments_table = erd.add_table(departments, 'departments', bg_color='lightyellow')
employees_table = erd.add_table(employees, 'employees', bg_color='grey')
job_history_table = erd.add_table(job_history, 'job_history', bg_color='gold')
jobs_table = erd.add_table(jobs, 'jobs', bg_color='pink')


erd.create_rel('regions', 'countries', on='region_id', right_cardinality='*')
erd.create_rel('countries', 'locations', on='country_id', right_cardinality='*')
erd.create_rel('departments', 'job_history', on='department_id', right_cardinality='*')
erd.create_rel('locations', 'departments', on='location_id', right_cardinality='*')
erd.create_rel('jobs', 'employees', on='job_id', right_cardinality='*')
erd.create_rel('job_history', 'employees', on='employee_id', right_cardinality='*')
erd.create_rel('jobs', 'job_history', on='job_id', right_cardinality='*')
erd.create_rel('employees', 'departments', on='department_id', left_cardinality='*')

## above code snipped was taken from pandaserd documentation 
# erd.write_to_file('output.txt')
## the image was produced using the generated code in output.txt






app = Dash(__name__)
server =  app.server

### EXERCISE NUMBER 2 
employees_joined = pd.read_sql("SELECT employees.first_name, jobs.job_title " +
                                "FROM employees " + 
                                "INNER JOIN jobs ON employees.job_id " + 
                                "= jobs.job_id",conn)

figure = px.histogram(employees_joined, x='job_title',color="job_title")

## EXERCISE 3
jobs=pd.read_sql_query("select * from jobs;", conn)
jobs = jobs.drop(0, axis=0)
jobs["difference"]=jobs['max_salary']-jobs['min_salary']
jobs_diff=jobs[['job_title','difference']]
MAX=jobs_diff['difference'].max()

app.layout = html.Div(children=[
    html.H1(['Dashboard'], style={'text-align': 'center'}),
    html.H2(['Abbosjon Madiev'], style={'text-align': 'center'}),
    html.Hr(),
    html.H4(['Exercise 1: Entity Relationship Diagram of the Database']),
    html.P([html.Img(src=r'assets/graph.png', width="75%")], style={'text-align':'center'}),

    html.Br(),

    html.H4('Employess with the same Job'),
    dcc.Graph(figure=figure),

    html.H4('Minimum - Maximum Job Salary'),
 
    dcc.Graph(id='fig3'),
    dcc.RangeSlider(0, MAX, 1000, value=[0, MAX], id="inp3"),
])



@app.callback(
    Output('fig3', 'figure'),
    Input('inp3', 'value'))
def update_output(value):
    MIN=value[0]
    MAX=value[-1]
    figure3 = go.Figure()
    figure3["layout"]["xaxis"]["title"] = "Job"
    figure3["layout"]["yaxis"]["title"] = "Difference between max and min"
    df = jobs_diff[jobs_diff["difference"]>=MIN][jobs_diff["difference"]<=MAX]
    figure3.add_trace(go.Bar(x=df['job_title'], y=df['difference'],
    name='Job differences'))
    return figure3



if __name__ == "__main__":
    app.run_server(debug=True, port=4000)




# fig = go.Figure()
# fig = px.bar(data_connected, x='job_title',color="job_title")
# ])