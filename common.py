
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
import base64

###################################
#original_data = pd.read_csv("Order_Summary_Item_Report.csv")
###################################
# Header layout and style ======================================================================================================

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#image_filename = 'logo.jif' # replace with your own image
#brand_image_filename = 'Brandlogo.jif'
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#brand_encoded_image = base64.b64encode(open(brand_image_filename, 'rb').read())
header_lay = html.Div(
    [
        dbc.Row(
            [
#                dbc.Col(html.Div(html.Img(src='data:image/png;base64,{}'.format(brand_encoded_image.decode()))),
#                     style={
#                           'position': 'absolute',
#                           'left': '0px', 'top': '0px'}),
             dbc.Col(html.Div('Restaurant Analytics Tool',style={'color': '#00385f','fontSize': 40}),
                     style={
                           'margin-top': 40,
                           'margin-bottom': 40,
                            'text-align': 'center'}),
#             dbc.Col(html.Div(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))),
#                     style={'height':'10%', 'width':'10%',
#                            'margin-left': 'auto',
#                            'vertical-align': 'top',
#                            'position': 'absolute', 'right': '50px',
#                            'top': '0px',
#                           }),

                
            ]
        ),
    ]
)

# Text styling ==================================================================================================================

text_style= {'color': '#00385f','fontSize': 30}


# Table styling =================================================================================================================

table_style_data={
    'maxWidth': '70%',
    'backgroundColor': 'rgb(96, 96, 96)',
    'color': 'white'
    }

table_style_cell={'fontSize':20, 'font-family':'sans-serif','width': '150px','textAlign': 'center'}
                    
table_style_header={
    'backgroundColor': 'white',
    'fontWeight': 'bold',
    'borderBottom': '1px solid black',
    'fontSize':25
    }

# Tab styling ===================================================================================================================

tabs_styles = {
    'height': '200px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '15px',
    'fontWeight': 'bold',
    'fontSize':25,
    'backgroundColor': 'rgb(192,192,192)'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#00385f',
    'color': 'white',
    'padding': '15px',
    'fontSize':25
}

# Sub_Tab styling ===================================================================================================================
Sub_tabs_styles = {
    'height': '100px'
}
Sub_tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '15px',
    'fontWeight': 'bold',
    'fontSize':20
}

Sub_tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#0072c1',
    'color': 'white',
    'padding': '15px',
    'fontSize':20
}

# RFM - Interactive table styling ==================================================================================================

rfm_table_style_data={'maxWidth': '70%',
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
            },

rfm_table_style_cell={'fontSize':20, 'font-family':'sans-serif','width': '150px','textAlign': 'center'},

rfm_table_style_header={'backgroundColor': 'white',
              'fontWeight': 'bold',
              'borderBottom': '1px solid black',
              'fontSize':25
              }

# Graph colors ======================================================================================================================

graph_colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}