import pandas as pd
import dash
from dash import dcc,html,Input,Output,State,dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go 
data = {
    "Student": ["Alice", "Bob", "Charlie", "David", "Ella", "Frank", "Grace", "Hannah", "Isaac", "Jack"],
    "Math Term 1": [85, 78, 92, 88, 76, 95, 68, 81, 74, 90],
    "Math Term 2": [88, 79, 91, 85, 79, 94, 70, 82, 75, 92],
    "Math Term 3": [90, 82, 93, 87, 80, 96, 72, 85, 77, 94],
    "Science Term 1": [90, 85, 80, 70, 88, 92, 75, 83, 80, 85],
    "Science Term 2": [92, 88, 78, 72, 90, 93, 78, 85, 82, 88],
    "Science Term 3": [94, 89, 81, 75, 91, 95, 80, 87, 84, 90],
    "English Term 1": [78, 82, 85, 90, 86, 80, 79, 83, 75, 88],
    "English Term 2": [80, 83, 86, 92, 89, 82, 81, 85, 78, 90],
    "English Term 3": [82, 85, 88, 93, 91, 85, 83, 87, 80, 92],
    "Attendance (%)": [95, 88, 92, 85, 98, 90, 87, 93, 92, 96],
    "Gender": ["Female", "Male", "Male", "Male", "Female", "Male", "Female", "Female", "Male", "Male"],
    "Class": ["A", "B", "A", "B", "A", "C", "B", "A", "C", "B"]
}
df = pd.DataFrame(data)
df1 = df[['Math Term 1', 'Math Term 2', 'Math Term 3', 'Science Term 1', 'Science Term 2', 'Science Term 3', 'English Term 1', 'English Term 2', 'English Term 3']].mean()
df2 = df['Class'].value_counts()
df3 = df[df['Student'] == 'Charlie'][['Math Term 1', 'Math Term 2', 'Math Term 3', 'Science Term 1', 'Science Term 2', 'Science Term 3', 'English Term 1', 'English Term 2', 'English Term 3']]
bar=go.Figure(go.Bar(x=df["Student"],y=df1)).update_layout(dragmode=False)
pie=go.Figure(go.Pie(labels=df["Class"],values=df2)).update_layout(dragmode=False)
line=go.Figure(go.Scatter(x=df3.columns,y=df3.iloc[0],mode="lines")).update_layout(dragmode=False)
df1['math']=df["Math Term 1"]+df["Math Term 2"] + df["Math Term 3"]
df1['science']=df["Science Term 1"] + df["Science Term 2"] + df["Science Term 3"]
df1['english']=df["English Term 1"]+df["English Term 2"]+df["English Term 3"]
a=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
styler={"margin":"5px","padding":"5px","color":"pink","borderRadius":"15px"}
a.layout=dbc.Container([
     dbc.Row([
                                 dbc.Col(dbc.Card([dbc.CardBody([html.H1("average marks"),dcc.Graph(figure=bar)])]),width=4,style=styler),
                                 dbc.Col(dbc.Card([dbc.CardBody([html.H1("sections"),dcc.Graph(figure=pie)])]),width=4,style=styler),
                                 dbc.Col(dbc.Card([dbc.CardBody([html.H3("a student report"),dcc.Dropdown(id="down",options=[{'value': i ,'label':i} for i  in df["Student"]],value="Alice"),html.Div(id="student_table")])]),width=3,style={"margin":"10px","padding":"10px","color":"pink","borderRadius":"5px","overflow":"scroll"}),
                                 dbc.Col([html.H1("Math summary"),dcc.Graph(figure=go.Figure(go.Bar(x=df["Student"],y=df1['math'],name="math summary")))],width=3,style={"margin":"5px","padding":"8px","color":"pink","borderRadius":"10px"}),
                                 dbc.Col([html.H1("Science summary"),dcc.Graph(figure=go.Figure(go.Bar(x=df["Student"],y=df1['science'],name="science summary")))],width=3,style={"margin":"5px","padding":"8px","color":"pink","borderRadius":"10px"}),
                                 dbc.Col([html.H1("English summary"),dcc.Graph(figure=go.Figure(go.Bar(x=df["Student"],y=df1['english'],name="english summary")))],width=3,style={"margin":"5px","padding":"8px","color":"pink","borderRadius":"10px"})]),
    dbc.Row([
                                 dbc.Col(dbc.Card([dbc.CardBody([html.H1("charlie's progress"),dcc.Graph(figure=line)])]),width=4,style=styler),
                                 dbc.Col(dbc.Card([dbc.CardBody([html.H1("data table"),dash_table.DataTable(columns=[{'id':i,'name':i} for i in df.columns],data=df.to_dict("records"))])]),width=7,style={"margin":"10px","padding":"10px","color":"pink","borderRadius":"5px","overflow":"scroll"})])],style={"backgroundColor":"black"},fluid=True)
@a.callback(Output('student_table','children'),Input("down",'value'),prevent_initial_call=True)
def data(value):
    df1=df[df["Student"]==value]
    return html.Div([dash_table.DataTable(columns=[{'id':col,'name':col} for col in df1.columns],data=df1.to_dict('records'),style_table={"overflow":"scroll"})])
a.run(port=8051)                                 
                                 
                                 
                                 
