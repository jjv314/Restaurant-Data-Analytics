import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from datetime import timedelta
import plotly.express as px
import dash_table
import plotly.graph_objects as go
from tab1 import processed_data

print('Working on Customer Tab')

data = processed_data.copy()

# Droping duplicate
data.sort_values("invoice_no", inplace=True)
data.drop_duplicates('invoice_no', inplace=True)

# Subsetting original dataset
table_set = data[['UniqueID', 'date', 'total']].copy()

# Counting total customer
total_unique_cust = table_set['UniqueID'].nunique()
total_cust = "Total number of unique customers in the data : " + str(total_unique_cust)

# Converting date variable from orginal dataset into datetime variable
table_set['date'] = pd.to_datetime(table_set['date'])

table_set['date'] = pd.to_datetime(table_set['date'])
table_set['date'], table_set['time'] = table_set['date'].dt.normalize(), table_set['date'].dt.time

# Creating duplicate dataset
Customer_table = table_set.copy()
snapshot_date = Customer_table['date'].max() + timedelta(days=1)

# Creating RFM table
# Grouping the data by date and summing the total amount variable to get the daily revenue
data_process = Customer_table.groupby(['UniqueID']).agg({
    'date': lambda x: (snapshot_date - x.max()).days,
    'UniqueID': 'count',
    'total': 'sum'})

data_process1 = data_process.rename(columns={'date': 'Recency', 'UniqueID': 'Frequency', 'total': 'Monetary'})

rfmTable = data_process1.drop([2])  # Drop swiggy id = 2

# ==============================================================  Part 1  ==============================================

freq_fig = px.histogram(rfmTable, x="Frequency")
Monetary_fig = px.histogram(rfmTable, x="Monetary")

# ============================================= End ====================================================================

# Generating summary for RFM table
rfm_summary = rfmTable.describe().round(3)  # Summary of RFM
rfm_summary.reset_index(inplace=True)
rfm_summary = rfm_summary.rename(columns={'index': 'Summary'})

quantiles = rfmTable.quantile(q=[0.25, 0.5, 0.75])
quantiles = quantiles.to_dict()

segmented_rfm = rfmTable


def RScore(x, p, d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4


def FMScore(x, p, d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1


segmented_rfm['r_quartile'] = segmented_rfm['Recency'].apply(RScore, args=('Recency', quantiles,))
segmented_rfm['f_quartile'] = segmented_rfm['Frequency'].apply(FMScore, args=('Frequency', quantiles,))
segmented_rfm['m_quartile'] = segmented_rfm['Monetary'].apply(FMScore, args=('Monetary', quantiles,))
segmented_rfm.head()

segmented_rfm['RFM Score'] = segmented_rfm.r_quartile.map(str) + segmented_rfm.f_quartile.map(
    str) + segmented_rfm.m_quartile.map(str)

segmented_rfm = segmented_rfm.drop(columns=['r_quartile', 'f_quartile', 'm_quartile'])  # **** added to remove columns

segmented_rfm.reset_index(inplace=True)

# ###################################### NEW SECTIOIN ############################################
segmented_rfm.loc[segmented_rfm['RFM Score'] == '111', 'Customer Segment'] = 'Best customer'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '211', 'Customer Segment'] = 'Highest spending active loyal customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '121', 'Customer Segment'] = 'Highest spending active loyal customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '112', 'Customer Segment'] = 'Highest spending active loyal customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '122', 'Customer Segment'] = 'Highest spending active loyal customer'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '141', 'Customer Segment'] = 'High spending new customers'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '142', 'Customer Segment'] = 'High spending new customers'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '131', 'Customer Segment'] = 'High spending new customers'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '132', 'Customer Segment'] = 'High spending new customers'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '341', 'Customer Segment'] = 'Big spendors'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '331', 'Customer Segment'] = 'Big spendors'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '321', 'Customer Segment'] = 'Big spendors'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '241', 'Customer Segment'] = 'Big spendors'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '231', 'Customer Segment'] = 'Big spendors'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '221', 'Customer Segment'] = 'Big spendors'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '313', 'Customer Segment'] = 'Loyal customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '312', 'Customer Segment'] = 'Loyal customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '314', 'Customer Segment'] = 'Loyal customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '413', 'Customer Segment'] = 'Loyal customer'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '411', 'Customer Segment'] = 'Churned best customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '412', 'Customer Segment'] = 'Churned best customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '421', 'Customer Segment'] = 'Churned best customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '422', 'Customer Segment'] = 'Churned best customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '311', 'Customer Segment'] = 'Churned best customer'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '132', 'Customer Segment'] = 'Recent customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '131', 'Customer Segment'] = 'Recent customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '144', 'Customer Segment'] = 'Recent customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '143', 'Customer Segment'] = 'Recent customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '133', 'Customer Segment'] = 'Recent customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '124', 'Customer Segment'] = 'Recent customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '123', 'Customer Segment'] = 'Recent customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '134', 'Customer Segment'] = 'Recent customer'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '113', 'Customer Segment'] = 'Lowest spending active loyal customer'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '114', 'Customer Segment'] = 'Lowest spending active loyal customer'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '443', 'Customer Segment'] = 'Lost low spending'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '444', 'Customer Segment'] = 'Lost low spending'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '434', 'Customer Segment'] = 'Lost low spending'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '441', 'Customer Segment'] = 'Lost big spendors'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '431', 'Customer Segment'] = 'Lost big spendors'

segmented_rfm.loc[segmented_rfm['RFM Score'] == '432', 'Customer Segment'] = 'Almost lost'
segmented_rfm.loc[segmented_rfm['RFM Score'] == '423', 'Customer Segment'] = 'Almost lost'

# ###################################### TILL HERE ###############################################

segmented_rfm["Customer Segment"].fillna("Others", inplace=True)

seg_categories = list(segmented_rfm['Customer Segment'].unique())
rfm_table_layout = html.Div([
    html.H1('RFM table', style={'color': 'black', 'text-align': 'center'}),  # 'fontSize': 35}),
    html.Div([
        html.H3('Enter Customer Segment'),
        dcc.Dropdown(
            id='dropdown_interactivity',
            options=[
                {'label': i, 'value': i} for i in seg_categories
            ],
            value='Loyal customer',
            style={'width': '49%', 'display': 'inline-block'}
        ),
        dash_table.DataTable(

            style_data={
                'maxWidth': '70%',
                'backgroundColor': 'rgb(60, 60, 60)',
                'color': 'white',
                'border': '0.25px solid black'
            },
            style_cell={'fontSize': 18, 'font-family': 'sans-serif', 'width': '150px', 'textAlign': 'center'},
            style_header={
                'fontWeight': 'bold',
                'borderBottom': '1px solid black',
                'fontSize': 22,
                'backgroundColor': 'rgb(255,153,153)',
                'border': '0.25px solid black'
            },

            export_format='xlsx',

            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in segmented_rfm.columns
            ],
            data=segmented_rfm.to_dict('records'),
            # editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            # column_selectable="single",
            # row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10,
        ),
        html.Div(id='datatable-interactivity-container'),  # DONT KNOW THE PURPOSE OF IT
        html.P(' '),
        html.Div([
            html.P('R - Recency (1 - Active / 4 - Non active)',
                   style={'margin-top': '0em',
                          'margin-bottom': '0em',
                          'text-align': 'left'}),

            html.P('F – Frequency (Number of times customer visiting the restaurant)'
                   ' (1- Frequently visiting / 4 – Rarely visiting)',
                   style={'margin-top': '0em',
                          'margin-bottom': '0em',
                          'text-align': 'left'
                          }
                   ),
            html.P('M – Revenue from each customer (1 – High spending / 4 – Low spending)',
                   style={'margin-top': '0em',
                          'margin-bottom': '0em',
                          'text-align': 'left'
                          }
                   ),
            html.P('RFM - Customer Behaviour Analysis  (RFM score 111 – Best Customers / '
                   '444 – Lost Non  Profitable Customers)',
                   style={'margin-top': '0em',
                          'margin-bottom': '0em',
                          'text-align': 'left'
                          }
                   ),
            html.P('Swiggy customers is not being considered for this analysis',
                   style={'margin-top': '0em',
                          'margin-bottom': '0em',
                          'text-align': 'left'
                          }
                   ),
        ], style={'font-size': '1.2em',
                  'backgroundColor': 'rgb(204,204,255)',
                  'border-radius': '10px 10px 10px 10px',
                  'text-align': 'center',
                  }),
    ])
])

total_no_of_cust = segmented_rfm.UniqueID.count()
total_no_of_cust = "  Total number of unique customers :  " + str(total_no_of_cust)

# ============================================== Interactive Table final table =========================================

# segmented_rfm

# ======================================================================================================================

segmented_rfm_count = segmented_rfm.groupby(['Customer Segment']).agg({
    'UniqueID': 'count',
    'Monetary': 'sum'})

segmented_rfm_count = segmented_rfm_count.rename(columns={'UniqueID': 'Count of Customers'})
segmented_rfm_count.reset_index(inplace=True)

segmented_rfm_count = segmented_rfm_count.sort_values(by=['Count of Customers'], ascending=False)

# ============================== Number of customers in every segment ============================================

# segmented_rfm_count

# NPS - Numbers per segment

NPS_fig = px.bar(segmented_rfm_count, x='Customer Segment', y='Count of Customers', color='Customer Segment')

NPS_fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1
    )
)

NPS_fig.update_layout(
    xaxis_title="Segment",
    yaxis_title="Number of Customer",
    font=dict(
        size=15
    ),
    plot_bgcolor='rgb(204,204,255)'
)

# =============================================================================================================


# ======================================== Revenue Per Segment =========================================

segmented_rfm_revenue = segmented_rfm_count.sort_values(by=['Monetary'], ascending=False)

RPS_fig = px.bar(segmented_rfm_revenue, x='Customer Segment', y='Monetary', color='Customer Segment')

RPS_fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1
    )
)

RPS_fig.update_layout(
    xaxis_title="Segment",
    yaxis_title="Revenue Per Segment",
    font=dict(
        size=15
    ),
    plot_bgcolor='rgb(204,204,255)'
)

# ================================================ Subtab 7 & Subtab 8 =================================================

# Droping duplicate
data.sort_values("invoice_no", inplace=True)
data.drop_duplicates('invoice_no', inplace=True)

# ======================================================================================================================
# Revenue

table_set = data[['UniqueID', 'date', 'total']].copy()

table_set['date'] = pd.to_datetime(table_set['date'])

table_set['date'] = pd.to_datetime(table_set['date'])
table_set['date'], table_set['time'] = table_set['date'].dt.normalize(), table_set['date'].dt.time

table_set['month'] = pd.DatetimeIndex(table_set['date']).month
table_set['year'] = pd.DatetimeIndex(table_set['date']).year
table_set['day'] = pd.DatetimeIndex(table_set['date']).day

table_set["year"] = table_set["year"].astype(str)
table_set["month"] = table_set["month"].astype(str)

table_set["month"].replace({"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul",
                            "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}, inplace=True)

table_set['month_yr'] = table_set['month'] + " " + table_set['year']

repeat_cust = pd.DataFrame()
repeat_cust['frequency'] = table_set.groupby(['month_yr', 'UniqueID']).size()

New_cust = repeat_cust[repeat_cust['frequency'] == 1]
New_cust = New_cust.reset_index()
New_cust = New_cust.rename(columns={'frequency': 'New customers'})

Repeated_cust = repeat_cust[repeat_cust['frequency'] != 1]
Repeated_cust = Repeated_cust.reset_index()
Repeated_cust = Repeated_cust.rename(columns={'frequency': 'Repeated customers'})

New_cust_count = New_cust.groupby(['month_yr']).agg({
    'UniqueID': 'count',
})
New_cust_count = New_cust_count.rename(columns={'UniqueID': 'New Customers'})

Repeated_cust_count = Repeated_cust.groupby(['month_yr']).agg({
    'UniqueID': 'count',
})
Repeated_cust_count = Repeated_cust_count.rename(columns={'UniqueID': 'Repeated Customers'})

new_repeat_cust = New_cust_count.merge(Repeated_cust_count, left_index=True, right_index=True)
new_repeat_cust['Total Customer'] = new_repeat_cust['New Customers'] + new_repeat_cust['Repeated Customers']

new_repeat_cust = new_repeat_cust.reset_index()

new_repeat_cust[['Month', 'Year']] = new_repeat_cust.month_yr.str.split(expand=True)

new_repeat_cust["Month"].replace({"Jan": "1", "Feb": "2", "Mar": "3", "Apr": "4", "May": "5", "Jun": "6", "Jul": "7",
                                  "Aug": "8", "Sep": "9", "Oct": "10", "Nov": "11", "Dec": "12"}, inplace=True)

new_repeat_cust.Month = pd.to_numeric(new_repeat_cust.Month, errors='coerce')
new_repeat_cust.Year = pd.to_numeric(new_repeat_cust.Year, errors='coerce')
new_repeat_cust.sort_values(['Year', 'Month'], ascending=[True, True], inplace=True)

# Subtab 7 =============================================================================================================

Repeat_new_cust = go.Figure()

Repeat_new_cust.add_trace(go.Scatter(
    x=new_repeat_cust['month_yr'], y=new_repeat_cust['Repeated Customers'],
    name="Repeated Customers", line={'color': 'rgb(153,0,153)'}
))

Repeat_new_cust.add_trace(go.Scatter(
    x=new_repeat_cust['month_yr'], y=new_repeat_cust['New Customers'],
    name="New Customers"
))

Repeat_new_cust.update_layout(
    xaxis_title="Month & Year", yaxis_title="Number of Customers",
    font=dict(
        size=15
    ),
    plot_bgcolor='rgb(204,204,255)',
)

# Subtab 8 =============================================================================================================

Total_cust = go.Figure()

Total_cust.add_trace(go.Scatter(
    x=new_repeat_cust['month_yr'], y=new_repeat_cust['Total Customer'],
    name="Total Customer", line={'color': 'black'}
))

Total_cust.update_layout(
    xaxis_title="Month & Year", yaxis_title="Total number of customers",
    font=dict(
        size=15
    ),
    plot_bgcolor='rgb(204,204,255)',
)
