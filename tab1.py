import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_table
import Pipeline

try:
    original_data = pd.read_csv("data.csv")
except FileNotFoundError as e:
    print(e)
    print('Please check whether you have placed the file named "data.csv" '
          'in the same folder where this executable file has been kept')

processed_data = Pipeline.pipeline(original_data)
print('Cleaning Original Data')
data = processed_data.copy()
print('Working on Revenue Tab')

# Droping duplicate
data.sort_values("invoice_no", inplace=True)
data.drop_duplicates('invoice_no', inplace=True)

graph_colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
# ===============================================================================================================================
# Revenue

table_set = data[['UniqueID', 'date', 'total']].copy()

table_set['date'] = pd.to_datetime(table_set['date'])

#table_set.loc[:, 'date'] = pd.to_datetime(table_set['date'])
table_set['date'], table_set['time'] = table_set['date'].dt.normalize(), table_set['date'].dt.time

daily_revenue = table_set.groupby(['date']).agg({'UniqueID': 'count',
                                                 'total': 'sum'})

daily_revenue['date'] = daily_revenue.index


def place_value(number):
    return "{:,}".format(number)


a = place_value(round(daily_revenue.total.sum(), 3))
b = place_value(round(daily_revenue.total.min(), 3))
c = place_value(round(daily_revenue.total.mean(), 3))
d = place_value(round(daily_revenue.total.max(), 3))
summary = [['Total Revenue', a], ['Mininmum Value', b], ['Average Value', c], ['Maximum Value', d]]
rev_summary_table = pd.DataFrame(summary, columns=['Metric', 'In Rs.'])

rev_summary_table_layout = dash_table.DataTable(
    style_data={
        'maxWidth': '70%',
        'backgroundColor': 'rgb(60, 60, 60)',
        'color': 'white',
        'border': '0.25px solid black'
    },
    style_cell={'fontSize': 18, 'font-family': 'sans-serif', 'textAlign': 'center',
                'minWidth': '70%', 'width': '70%', 'maxWidth': '70%'},
    style_table={
        'maxWidth': '900px',
        'margin-left': 'auto',
        'margin-right': 'auto'
    },
    export_format='xlsx',
    style_header={
        'fontWeight': 'bold',
        'borderBottom': '1px solid black',
        'fontSize': 22,
        'backgroundColor': 'rgb(255,153,153)',
        # 'backgroundColor': 'rgb(152,175,228)',
        'border': '0.25px solid black'
    },

    id='rev_table',
    columns=[{"name": i, "id": i} for i in rev_summary_table.columns],
    data=rev_summary_table.to_dict('records'),
)

total_revenue = "  Total revenue : Rs. " + str(a)

fig_revenue_overall = go.Figure(data=[go.Scatter(x=daily_revenue['date'], y=daily_revenue['total'],
                                                 line={'color': 'black'})])  # MADE CHANGE HERE
fig_revenue_overall.update_layout(
    xaxis_title="Month", yaxis_title="Revenue",
    font=dict(
        size=15
    ),
    plot_bgcolor='rgb(204,204,255)',
)

# ===============================================================================================================================

# PIE CHART 

order_type = data[['area']].copy()
order_type['area'].fillna("Dine-in", inplace=True)
order_type = order_type.replace('Dining', 'Dine-in')
order_type1 = pd.DataFrame(order_type.area.value_counts())
order_type1 = order_type1.rename(columns={'area': 'area_count'})
order_type1 = order_type1.reset_index()
order_type1 = order_type1.rename(columns={'index': 'area'})
order_type_fig = px.pie(order_type1, values='area_count', names='area',
                        color_discrete_sequence=px.colors.sequential.RdPu_r, width=800, height=400)

order_type_fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="rgb(245,245,245)",
    font=dict(
        size=15
    )
)

# ===============================================================================================================================
#
# # Monthly compare - Bar Graph
# ACTUALLY FOR LINE GRAPH
daily_revenue['month'] = pd.DatetimeIndex(daily_revenue['date']).month
daily_revenue['year'] = pd.DatetimeIndex(daily_revenue['date']).year
daily_revenue['day'] = pd.DatetimeIndex(daily_revenue['date']).day

year_list = list(daily_revenue.year.unique())

# ACTUALLY FOR MOM GRAPH
mom_daily_revenue = daily_revenue.copy()
mom_daily_revenue["year"] = mom_daily_revenue["year"].astype(str)
mom_daily_revenue["month"] = mom_daily_revenue["month"].astype(str)

mom_daily_revenue["month"].replace(
    {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul",
     "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}, inplace=True)

arr1 = 'Jan ' + mom_daily_revenue['year']
arr2 = 'Feb ' + mom_daily_revenue['year']
arr3 = 'Mar ' + mom_daily_revenue['year']
arr4 = 'Apr ' + mom_daily_revenue['year']
arr5 = 'May ' + mom_daily_revenue['year']
arr6 = 'Jun ' + mom_daily_revenue['year']
arr7 = 'Jul ' + mom_daily_revenue['year']
arr8 = 'Aug ' + mom_daily_revenue['year']
arr9 = 'Sep ' + mom_daily_revenue['year']
arr10 = 'Oct ' + mom_daily_revenue['year']
arr11 = 'Nov ' + mom_daily_revenue['year']
arr12 = 'Dec ' + mom_daily_revenue['year']

MOM_bar_fig = px.bar(mom_daily_revenue, x='month', y='total', color='month')

MOM_bar_fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        ticktext=[arr1[len(arr1) - 1], arr2[0], arr3[0], arr4[0], arr5[0], arr6[0],
                  arr7[0], arr8[0], arr9[0], arr10[0], arr11[0], arr12[0]]
    )
)

MOM_bar_fig.update_layout(
    # title="Monthly Revenue",
    xaxis_title="Month",
    yaxis_title="Revenue",
    font=dict(
        size=15
    ),
    plot_bgcolor='rgb(204,204,255)'
)

# ===============================================================================================================================

# ==============================================================================================================================

MWD_layout = html.Div([
    html.H1('Daily revenue comparison', style={'color': 'black',  # 'fontSize': 32,
                                               'text-align': 'center'}),
    html.H3('Select Year'),
    dcc.Dropdown(
        id='I_MWD_fig',
        options=[
            {'label': each_year, 'value': each_year} for each_year in year_list
        ],
        value=year_list[len(year_list) - 1],
        style={'width': '49%', 'display': 'inline-block'}
    ),
    dcc.Graph(id='O_MWD_fig'),
    html.H1('Monthly revenue comparison', style={'color': 'black',
                                                 'text-align': 'center'}),  # fontSize': 32}),
    dcc.Graph(id='MOM_bar_fig', figure=MOM_bar_fig),
])

# ==============================================================================================================================

# YOY - Year on year

YOY_fig = px.bar(mom_daily_revenue, x='year', color='year', y='total',
                 color_discrete_sequence=['rgb(153,0,153)', 'rgb(254,129,127)'])

YOY_fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1
    )
)

YOY_fig.update_layout(
    # title="Yearly Revenue",
    xaxis_title="Year",
    yaxis_title="Revenue",
    font=dict(
        size=15
    ),
    plot_bgcolor='rgb(204,204,255)'
)

# ===============================================================================================================================

DOD_fig = px.bar(daily_revenue, x='day', y='total', color='day')

DOD_fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        tick0=0,
        dtick=1
    )
)

DOD_fig.update_layout(
    title="Daily Revenue",
    xaxis_title="Day",
    yaxis_title="Revenue",
)
