import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import dash_table
from tab1 import processed_data

print('Working on Product Tab')

# FOR Tab 3 - Preprocessing ===========================================================================================
# FOR ALL
# Read the dataset and creating one df required for all other charts

df = processed_data.copy()

df['date'] = pd.to_datetime(df.date)
df = df.sort_values(by='date')
df['Month & Year'] = df['date'].apply(lambda x: x.strftime('%B - %Y'))
df['Day_Of_Week'] = df['date'].apply(lambda x: x.strftime('%A'))
productcustom_df = df[['invoice_no', 'date', 'Month & Year', 'Day_Of_Week', 'item_name', 'item_total']]
# print(productcustom_df.head())

# FOR TOP SECTION
# Creating df for Top Products Overall based on entire data
top_product_df = productcustom_df.groupby(['item_name'], sort=False)['item_total'].sum().reset_index()
top_product_df = top_product_df.sort_values(by='item_total', ascending=False)
top_product_df = top_product_df.head(10)
top_product_df = top_product_df.sort_values(by='item_total', ascending=True)
# print(top_product_df.head())

# FOR TOP SECTION
# Creating df for Bottom Products Overall based on entire data
bottom_product_df = productcustom_df.groupby(['item_name'], sort=False)['item_total'].sum().reset_index()
bottom_product_df = bottom_product_df.sort_values(by='item_total', ascending=True)
bottom_product_df = bottom_product_df.head(10)
bottom_product_df = bottom_product_df.sort_values(by='item_total', ascending=False)
# print(bottom_product_df.head())

# FOR BOTTOM SECTION
# Readying df for Top and Bottom Proucts by Month
monthlyproduct_df = productcustom_df.groupby(['Month & Year', 'item_name'],
                                             sort=False)['item_total'].sum().reset_index()

month_year = list(monthlyproduct_df['Month & Year'].unique())
day_week = list(productcustom_df['Day_Of_Week'].unique())

all_options = {
    'Month': month_year,
    'Day': day_week
}
# print(all_options)

# Subtab 9 =======================================================================================================================

subtab9_layout = html.Div([
    html.Div([
        html.H3('Ranking of Products by: '),
        dcc.Dropdown(
            id='I_based_on_entire_data',
            options=[
                {'label': 'Top Products (Based on entire data)', 'value': 'Top_entire'},
                {'label': 'Bottom Products (Based on entire data)', 'value': 'Bottom_entire'}
            ],
            value='Top_entire',
            style={'width': '100%',
                   'display': 'inline-block'}
        ),
    ], style={'width': '49%'}),
    html.Div([
        html.Div([
            dcc.Graph(
                id="O_based_on_entire_data"
            ),
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Graph(
                id="O_freq_based_on_entire_data"
            ),
        ], style={'width': '49%', 'display': 'inline-block',
                  'margin-left': 20})
    ]),
])

# Subtab 10 =====================================================================================================================    

subtab10_layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H3('Ranking of Products by: '),
                dcc.RadioItems(
                    id='overall_radio_left',
                    options=[
                        {'label': 'Top', 'value': 'Top'},
                        {'label': 'Bottom', 'value': 'Bottom'}
                    ],
                    value='Top',
                    labelStyle={'display': 'inline-block', 'margin-right': 50}
                )
            ], style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                html.H3('Sort by:'),
                dcc.RadioItems(
                    id='specifics_radio_left',
                    options=[
                        {'label': 'Month', 'value': 'Month'},
                        {'label': 'Day', 'value': 'Day'}
                    ],
                    value='Month',
                    labelStyle={'display': 'inline-block', 'margin-right': 35}
                )
            ], style={'width': '49%', 'display': 'inline-block'}),
            html.H3('Select your specific Month/Day of choice'),
            dcc.Dropdown(
                id='dropdown_options_left',
                value=month_year[len(month_year) - 2],
                style={'width': '100%',
                       'display': 'inline-block'}

            ),
            dcc.Graph(
                id="O_Month_Date_left"
            )
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                html.H3('Ranking of Products by: '),
                dcc.RadioItems(
                    id='overall_radio_right',
                    options=[
                        {'label': 'Top', 'value': 'Top'},
                        {'label': 'Bottom', 'value': 'Bottom'}
                    ],
                    value='Top',
                    labelStyle={'display': 'inline-block', 'margin-right': 50}
                )
            ], style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                html.H3('Sort by:'),
                dcc.RadioItems(
                    id='specifics_radio_right',
                    options=[
                        {'label': 'Month', 'value': 'Month'},
                        {'label': 'Day', 'value': 'Day'}
                    ],
                    value='Month',
                    labelStyle={'display': 'inline-block', 'margin-right': 35}
                )
            ], style={'width': '49%', 'display': 'inline-block'}),
            html.H3('Select your specific Month/Day of choice'),
            dcc.Dropdown(
                id='dropdown_options_right',
                value=month_year[len(month_year) - 1],
                style={'width': '100%',
                       'display': 'inline-block'}
            ),
            dcc.Graph(
                id="O_Month_Date_right"
            )
        ], style={'width': '49%', 'display': 'inline-block',
                  'margin-left': 20
                  }),  # className='six columns'),
        # ], className='row'),
    ]),
])

print('Please Wait. It is almost Done!')
data1 = df[['date', 'invoice_no', 'UniqueID', 'total', 'item_name']]


# Function for converting data into proper format

def marketing(data1):
    data1 = data1[['date', 'invoice_no', 'UniqueID', 'total', 'item_name']]
    data1['date'] = pd.to_datetime(data1['date'])
    data1['date'], data1['time'] = data1['date'].dt.normalize(), data1['date'].dt.time
    data1 = data1.drop(columns=['time'])
    dummy = pd.get_dummies(data1['item_name'])
    data3 = pd.concat([data1, dummy], axis=1)
    data4 = data3.groupby(['invoice_no', 'UniqueID', 'date', 'total']).agg(lambda x: x.values.sum())  # OPTIMISED
    data4 = data4.reset_index()
    return data4


data4 = marketing(data1)
data5 = data4.drop(["date", "total", "item_name"], axis=1)
data5 = data5.drop(["invoice_no", "UniqueID"], axis=1)
data5 = data5.replace([2, 3, 4, 5], 1)

# Working on the base apriori function
freq_items = apriori(data5, min_support=0.01, use_colnames=True, verbose=0)
freq_items = freq_items.sort_values(by='support', ascending=False)

# Working on table Products with Top Support
TopSupport = freq_items.copy()
TopSupport.columns = ['Percentage of Orders', 'Product']
TopSupport = TopSupport[['Product', 'Percentage of Orders']]
TopSupport['Percentage of Orders'] = TopSupport['Percentage of Orders'].apply(lambda x: round(x * 100, 2))
TopSupport.insert(0, 'Serial No.', range(1, 1 + len(TopSupport)))
TopSupport['Product'] = TopSupport['Product'].apply(lambda x: list(x))
# TopSupport['Dish Name'] = TopSupport['Dish Name'].apply(lambda x: ', '.join(x))
TopSupport['Product'] = TopSupport['Product'].apply(lambda x: 0 if len(x) >= 2 else x[0])
TopSupport = TopSupport[TopSupport['Product'] != 0]
selectfew_TopSupport = TopSupport.head(10)
top5perc = round(selectfew_TopSupport['Percentage of Orders'].head().sum(), 1)

# Working on Product Associations based on Top Support
rules_TopSupport = association_rules(freq_items, metric="support", min_threshold=0.015)
rules_TopSupport = rules_TopSupport.sort_values(by=['support'], ascending=False)  # MADE CHANGE HERE
rules_TopSupport = rules_TopSupport[rules_TopSupport.lift > 1]
rules_TopSupport = rules_TopSupport[['antecedents', 'consequents', 'support']]
rules_TopSupport.columns = ['Product', 'Associated Product', 'Percentage of Orders']
rules_TopSupport['Percentage of Orders'] = rules_TopSupport['Percentage of Orders'].apply(lambda x: round(x * 100, 2))
rules_TopSupport.insert(0, 'Serial No', range(1, 1 + len(rules_TopSupport)))

rules_TopSupport['Product'] = rules_TopSupport['Product'].apply(lambda x: list(x))
rules_TopSupport['Product'] = rules_TopSupport['Product'].apply(lambda x: x[0])
rules_TopSupport['Associated Product'] = rules_TopSupport['Associated Product'].apply(lambda x: list(x))
rules_TopSupport['Associated Product'] = rules_TopSupport['Associated Product'].apply(lambda x: ', '.join(x))


def remove_common_rows(data):
    ind = []
    for i in range(len(data)):
        item1 = data['Product'].iloc[i]
        item2 = data['Associated Product'].iloc[i]
        for j in range(i + 1, len(data)):
            search1 = data['Product'].iloc[j]
            search2 = data['Associated Product'].iloc[j]
            if (item1 == search2 and item2 == search1):
                ind.append(j + 1)
                # print(ind)

    if len(ind) > 0:
        data = data.set_index('Serial No')
        data = data.drop(ind)
        data = data.reset_index()
        data.insert(0, 'Serial No.', range(1, 1 + len(data)))
        data.drop('Serial No', axis=1, inplace=True)
    return data

rules_TopSupport = remove_common_rows(rules_TopSupport)


# Working on Product Associations based on Top Confidence
rules_TopConfidence = association_rules(freq_items, metric="confidence", min_threshold=0.25)
rules_TopConfidence = rules_TopConfidence.sort_values(by=['confidence'],
                                                      ascending=False)  # CHANGES MADE HERE, Can also sort by support
rules_TopConfidence = rules_TopConfidence[rules_TopConfidence.lift > 1]
rules_TopConfidence = rules_TopConfidence[['antecedents', 'consequents', 'confidence', 'support']]
rules_TopConfidence.columns = ['Product', 'Associated Product', 'Percentage of Confidence', 'Percentage of Orders']
rules_TopConfidence['Percentage of Confidence'] = rules_TopConfidence['Percentage of Confidence'].apply(
    lambda x: round(x * 100, 2))
rules_TopConfidence['Percentage of Orders'] = rules_TopConfidence['Percentage of Orders'].apply(
    lambda x: round(x * 100, 2))
rules_TopConfidence.insert(0, 'Serial No.', range(1, 1 + len(rules_TopConfidence)))

rules_TopConfidence['Product'] = rules_TopConfidence['Product'].apply(lambda x: list(x))
rules_TopConfidence['Product'] = rules_TopConfidence['Product'].apply(lambda x: ', '.join(x))
rules_TopConfidence['Associated Product'] = rules_TopConfidence['Associated Product'].apply(lambda x: list(x))
rules_TopConfidence['Associated Product'] = rules_TopConfidence['Associated Product'].apply(lambda x: ', '.join(x))

# Working on Product Associations of you desired product
rules_custom = association_rules(freq_items, metric="support", min_threshold=0.001)
rules_custom = rules_custom.sort_values(by=['confidence'], ascending=False)
rules_custom = rules_custom[rules_custom.lift > 1]

rules_custom['antecedents'] = rules_custom['antecedents'].apply(lambda x: list(x))
rules_custom['antecedents'] = rules_custom['antecedents'].apply(lambda x: ', '.join(x))
rules_custom['consequents'] = rules_custom['consequents'].apply(lambda x: list(x))
rules_custom['consequents'] = rules_custom['consequents'].apply(lambda x: ', '.join(x))

list_A = list(rules_custom.antecedents.unique())
list_A.sort()
list_B = list(rules_custom.consequents.unique())
list_B.sort()
rulescustom_dropdownlist = list(set(list_A + list_B))
rulescustom_dropdownlist.sort()
list_C = list(TopSupport['Product'].unique())
list_C.sort()
# print('Done with basic preprocessing!')

suntab11_layout = html.Div([
    html.H1('Products that comprise the majority of your transactions',
            style={'text-align': 'center'}),
    dash_table.DataTable(
        id='O_TopSupport',
        columns=[{"name": i, "id": i} for i in selectfew_TopSupport.columns],
        data=selectfew_TopSupport.to_dict('records'),
        style_table={
            'maxHeight': '340px',
            'maxWidth': '900px',
            # 'overflowY': 'scroll',
            'margin-left': 'auto',
            'margin-right': 'auto'
        },
        export_format='xlsx',
        export_headers='display',
        style_data={
            'maxWidth': '70%',
            'backgroundColor': 'rgb(60, 60, 60)',
            'color': 'white',
            'border': '0.25px solid black'
        },
        style_cell={'fontSize': 18, 'font-family': 'sans-serif',
                    'width': '150px', 'textAlign': 'center'
                    },
        style_header={
            # 'backgroundColor': 'white',
            'fontWeight': 'bold',
            'borderBottom': '1px solid black',
            'fontSize': 22,
            # 'backgroundColor': 'rgb(204,0,102)',
            'backgroundColor': 'rgb(255,153,153)',
            'border': '0.25px solid black'
        },

    ),
    html.Div([
        html.P("This table shows how much each product contributes to your "
               "total number of sales"),
        html.P('Top Products comprise ' + str(top5perc) + '% of all '
                                                          'your transactions.'),
    ], style={'font-size': '1.2em',
              'backgroundColor': 'rgb(204,204,255)',
              'border-radius': '10px 10px 10px 10px',
              'text-align': 'center'}),
    html.Div([
        html.Div([
            html.H2('Associated products which occur together most frequently',
                    style={'text-align': 'center'}),
            dash_table.DataTable(
                id='O_rules_TopSupport',
                columns=[{"name": i, "id": i} for i in rules_TopSupport.columns],
                data=rules_TopSupport.to_dict('records'),
                style_table={
                    'maxHeight': '300px',
                    'overflowY': 'scroll'
                },
                export_format='xlsx',
                export_headers='display',
                style_data={
                    'maxWidth': '70%',
                    'backgroundColor': 'rgb(60, 60, 60)',
                    'color': 'white',
                    'border': '0.25px solid black'
                },
                style_cell={'fontSize': 16, 'font-family': 'sans-serif',
                            'width': '150px', 'textAlign': 'center'},
                style_header={
                    # 'backgroundColor': 'rgb(192,192,192)',
                    'backgroundColor': 'rgb(255,153,153)',
                    'fontWeight': 'bold',
                    'borderBottom': '1px solid black',
                    'fontSize': 20,
                    'border': '0.25px solid black'
                },
            ),

        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.H2('Associated products with strong relationships',
                    style={'text-align': 'center'}),
            dash_table.DataTable(
                id='O_rules_TopConfidence',
                columns=[{"name": i, "id": i} for i in rules_TopConfidence.columns],
                data=rules_TopConfidence.to_dict('records'),
                style_table={
                    'maxHeight': '300px',
                    'overflowY': 'scroll'
                },
                export_format='xlsx',
                export_headers='display',
                style_data={
                    'maxWidth': '70%',
                    # 'backgroundColor': 'rgb(204, 153, 255)',
                    'backgroundColor': 'rgb(60, 60, 60)',
                    # 'color': 'black'
                    'color': 'white',
                    'border': '0.25px solid black'
                },
                style_cell={'fontSize': 16, 'font-family': 'sans-serif',
                            'width': '150px', 'textAlign': 'center'},
                style_header={
                    # 'backgroundColor': 'rgb(102, 0, 204)',
                    'backgroundColor': 'rgb(255, 153, 153)',
                    'fontWeight': 'bold',
                    'borderBottom': '1px solid black',
                    'fontSize': 20,
                    'border': '0.25px solid black'
                },
            ),

        ], style={'width': '49%', 'display': 'inline-block', 'margin-left': 10}),
        html.P(''),  # left purposely to cause a gap
        html.Div([
            html.P('Here the Product and the Associated Product occur together most frequently '
                   'in all of your orders. You could offer Combo Meals or '
                   'you could help your hotel staff in up-selling products.'),
            html.P('Note: Only those orders which occur together and comprise at least'
                   ' 1.5% of all transactions will be shown in the above table.')
        ], style={'font-size': '1.2em',
                  'backgroundColor': 'rgb(204,204,255)',
                  'border-radius': '10px 10px 10px 10px',
                  'text-align': 'center',
                  'width': '49%', 'display': 'inline-block'
                  }),
        html.Div([
            html.P('Here the Product and the Associated product always go together '
                   'and thus the Products in this table are probably complimentary products.'),
            html.P('If the Product itself is a standalone product, you could raise the '
                   'price of the Associated Product (as they are highly likely to '
                   'bought once the initial Product is bought).'),
            html.P('Note: For the case of better understanding, if the '
                   'Percentage of Confidence is 50% and let’s say the Product is '
                   'bought 100 times in total, 50% of the times it also included '
                   'the Associated Product.')
        ], style={'font-size': '1.2em',
                  'backgroundColor': 'rgb(204,204,255)',
                  'border-radius': '10px 10px 10px 10px',
                  'text-align': 'center',
                  'width': '49%', 'display': 'inline-block', 'margin-left': 10}
        )
    ]),
    html.H1('Existing Combinations', style={'text-align': 'center'}),
    dcc.Dropdown(
        id='I_rules_custom',
        options=[
            {'label': i, 'value': i} for i in rulescustom_dropdownlist
        ],
        value='None'

    ),
    dash_table.DataTable(
        id='O_rules_custom',
        columns=[{"name": i, "id": i} for i in rules_custom.columns],
        style_table={
            'maxHeight': '300px',
            'overflowY': 'scroll'
        },
        export_format='xlsx',
        export_headers='display',
        style_data={
            'maxWidth': '70%',
            'backgroundColor': 'rgb(60, 60, 60)',
            'color': 'white',
            'border': '0.25px solid black'
        },
        style_cell={'fontSize': 18, 'font-family': 'sans-serif',
                    'width': '150px', 'textAlign': 'center'},
        style_header={
            # 'backgroundColor': 'white',
            'backgroundColor': 'rgb(255,153,153)',
            'fontWeight': 'bold',
            'borderBottom': '1px solid black',
            'fontSize': 22,
            'border': '0.25px solid black'
        },

    ),
    html.Div([
        html.P('Find out how a specific product is related to other'
               ' products.'),
    ], style={'font-size': '1.2em',
              'backgroundColor': 'rgb(204,204,255)',
              'border-radius': '10px 10px 10px 10px',
              'text-align': 'center'
              }),
    # Layout for Single Product Discount Calculator begin
    html.H1('Target Sales Calculator', style={'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.H3('Enter Product A', style={'margin-left': 50}),
                dcc.Dropdown(
                    id='I_Prod_A_name',
                    options=[
                        {'label': i, 'value': i} for i in list_C
                    ],
                    value='None',
                    style={'backgroundColor': 'rgb(250,250,250)'}
                ),
            ], style={'width': '15%', 'display': 'inline-block'}),
            html.Div([
                html.H3('Price of Product'),
                html.H4(id='O_Product_SalePrice', style={'margin-left': 50}),
            ], style={'width': '15%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H3('Revenue generated'),
                html.H4(id='O_Revenue_of_product', style={'margin-left': 50}),
            ], style={'width': '20%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H3('% of Orders'),
                html.H4(id='O_Percentage_Of_Sales', style={'margin-left': 50}),
            ], style={'width': '20%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H3('Orders (in numbers)'),
                html.H4(id='O_Number_Of_Transactions', style={'margin-left': 75}),
            ], style={'width': '20%', 'display': 'inline-block'}),
        ], style={'backgroundColor': 'rgb(192,192,192)'}),

        html.Div([
            html.H3('New Product A price'),
            dcc.Input(id='I_ProductA_new_price',
                      placeholder='Enter new price'),
        ], style={'width': '20%', 'margin-left': 25, 'display': 'inline-block'}),
        html.Div([
            html.H3('Targeted Sales required'),
            html.H4(id='O_suggest_target', style={'margin-left': 75})
        ], style={'width': '15%', 'margin-left': 25, 'display': 'inline-block',
                  'backgroundColor': 'rgb(255,153,153)',
                  'border-radius': '10px 10px 10px 10px'}),
    ]),
    html.Div([
        html.P('Find  the number of sales that you would require to '
               'compensate for your discount or even an increase in '
               'sale price. You can also use this same calculator '
               'to verify whether you have achieved your goal or not(Just '
               'enter the product name without adding new price).',
               style={'margin-top': '0em',
                      'margin-bottom': '0em'}),

        html.P('Note: You should make sure you are comparing equal time periods.'
               ' If the suggested target you get is based on a period of past '
               'six months, then you should check whether you have achieved your '
               'target only after six months!'
               # style={'margin-top': '0em',
               #        'margin-bottom': '0em'}
               ),
    ], style={'font-size': '1.2em',
              'backgroundColor': 'rgb(204,204,255)',
              'border-radius': '10px 10px 10px 10px',
              'text-align': 'center',
              }),
    # Layout for Multi-Product Discount Calculator begins
    html.H1('Combo-Deal Calculator', style={'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.H3('Enter Product A'),
                dcc.Dropdown(
                    id='I_As_Prod_A_name',
                    options=[
                        {'label': i, 'value': i} for i in rulescustom_dropdownlist
                    ],
                    value='None',
                    style={'backgroundColor': 'rgb(250,250,250)'}
                ),
            ], style={'width': '15%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H3('Enter Product B'),
                dcc.Dropdown(
                    id='I_As_Prod_B_name',
                    options=[
                        {'label': i, 'value': i} for i in list_C
                    ],
                    value='None',
                    style={'backgroundColor': 'rgb(250,250,250)'}
                ),
            ], style={'width': '15%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H3('Product A Price'),
                html.H4(id='O_As_ProductA_SalePrice', style={'margin-left': 40}),
            ], style={'width': '15%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H3('Product B Price'),
                html.H4(id='O_As_ProductB_SalePrice', style={'margin-left': 40}),
            ], style={'width': '15%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H3('Total Price'),
                html.H4(id='O_As_TotalPrice', style={'margin-left': 25}),
            ], style={'width': '15%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H3('Revenue generated'),
                html.H4(id='O_As_Revenue_of_products', style={'margin-left': 40}),
            ], style={'width': '15%', 'margin-left': 25, 'display': 'inline-block'}),
        ], style={'backgroundColor': 'rgb(192,192,192)'}),
        html.Div([
            html.Div([
                html.H3('% of Orders'),
                html.H4(id='O_As_Percentage_Of_Sales', style={'margin-left': 40}),
            ], style={'width': '15%', 'margin-left': 650, 'display': 'inline-block'}),
            html.Div([
                html.H3('Orders (in numbers)'),
                html.H4(id='O_As_Number_Of_Transactions', style={'margin-left': 50}),
            ], style={'margin-left': 25, 'display': 'inline-block'}),
        ], style={'backgroundColor': 'rgb(250,250,250)'}),
        html.Div([
            html.Div([
                html.H4('New Product A price'),
                dcc.Input(id='I_Multi_ProductA_new_price',
                          placeholder='For Product A'),
            ], style={'width': '20%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H4('New Product B price'),
                dcc.Input(id='I_Multi_ProductB_new_price',
                          placeholder='For Product B'),
            ], style={'width': '20%', 'margin-left': 25, 'display': 'inline-block'}),
            html.Div([
                html.H3('Combo-Meal Price'),
                html.H4(id='O_As_ComboPrice', style={'margin-left': 40}),
            ], style={'width': '13%', 'margin-left': 10, 'display': 'inline-block'}),
            html.Div([
                html.H3('Targeted Sales required'),
                html.H4(id='O_Multi_suggest_target', style={'margin-left': 50})
            ], style={'width': '15%', 'margin-left': 25, 'display': 'inline-block',
                      'backgroundColor': 'rgb(255,153,153)',
                      'border-radius': '10px 10px 10px 10px'}),
        ]),
    ]),
    html.Div([
        html.P("Remember those McDonald's combo meals where the "
               "customer is provided with an incentive to buy a "
               "combo-meal and save money? The customer enjoy's the "
               "savings while the franchise enjoy's greater sales. Now "
               "create one of your own!"),
        html.P('Find the number of sales that you would require to '
               'compensate for the discount you would like to offer for your combo'
               ' meals. Only those products which have relevant relationships '
               "as shown in the table titled 'Existing Combinations' "
               "above will be eligible for this calculator"),

        html.P('Note: You should make sure you are comparing equal'
               ' time periods. If the suggested target you get is based'
               ' on a period of past six months, then you should check '
               'whether you have achieved your target only after '
               'six months!')
    ], style={'font-size': '1.2em',
              'backgroundColor': 'rgb(204,204,255)',
              'border-radius': '10px 10px 10px 10px',
              'text-align': 'center'
              }),
])
