def run_my_program():
    import tab1
    import tab2
    import tab3
    import common
    import dash
    from dash.dependencies import Input, Output
    import dash_html_components as html
    import dash_core_components as dcc
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from tab1 import processed_data

    data = processed_data.copy()
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash()  # external_stylesheets=[dbc.themes.DARKLY])

    # ======================================================================================================================
    # ======================================================================================================================

    # Create a Dash layout==================================================================================================
    app.layout = html.Div([
        common.header_lay,
        dcc.Tabs(id="tabs", value='tab1',
                 children=[
                     dcc.Tab(label='Revenue', value='tab1',
                             children=[dcc.Tabs(id="subtabs1", value="subtab1",
                                                children=[dcc.Tab(label='Overall Revenue', value="subtab1",
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style),
                                                          dcc.Tab(label='Monthly Revenue Compare', value="subtab2",
                                                                  children=[tab1.MWD_layout],
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style),
                                                          dcc.Tab(label='Order Type Distribution', value="subtab3",
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style),
                                                          dcc.Tab(label='YOY', value="subtab4",
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style)
                                                          ]
                                                )],
                             style=common.tab_style, selected_style=common.tab_selected_style
                             ),
                     dcc.Tab(label='Customer', value='tab2',
                             children=[dcc.Tabs(id="subtabs2", value="subtab5",
                                                children=[dcc.Tab(label='Customer Segments', value="subtab5",
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style),
                                                          dcc.Tab(label='RFM Table', value="subtab6",
                                                                  children=[tab2.rfm_table_layout],
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style),
                                                          dcc.Tab(label='New vs Repeat Customers', value="subtab7",
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style),
                                                          dcc.Tab(label='Total Number of Customers', value="subtab8",
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style)
                                                          ]
                                                )],
                             style=common.tab_style, selected_style=common.tab_selected_style,
                             ),
                     dcc.Tab(label='Product', value='tab3',
                             children=[dcc.Tabs(id="subtabs3", value="subtab9",
                                                children=[dcc.Tab(id='Top and Bottom Product',
                                                                  label='Revenue and Frequency of Products',
                                                                  value="subtab9",
                                                                  children=[tab3.subtab9_layout],
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style),

                                                          dcc.Tab(id='Product Compare', label='Revenue Comparison',
                                                                  value="subtab10",
                                                                  children=[tab3.subtab10_layout],
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style),

                                                          dcc.Tab(id='subtab11', label='MBA', value="subtab11",
                                                                  children=[tab3.suntab11_layout],
                                                                  style=common.Sub_tab_style,
                                                                  selected_style=common.Sub_tab_selected_style),

                                                          # dcc.Tab(label='Sub tab12', value="subtab12",
                                                          #         style=common.Sub_tab_style,
                                                          #         selected_style=common.Sub_tab_selected_style)
                                                          ]
                                                )],
                             style=common.tab_style, selected_style=common.tab_selected_style,
                             ),
                 ]),
        html.Div(id='tabs-content')
    ])

    # ======================================================== TAB 1 =======================================================
    # ======================================================================================================================
    # ====================================================== REVENUE =======================================================

    @app.callback(Output('tabs-content', 'children'),
                  [Input('tabs', 'value'),
                   Input('subtabs1', 'value'),
                   Input('subtabs2', 'value')])
    def render_content(tab, subtab1, subtab2):
        if tab == 'tab1' and subtab1 == 'subtab1':
            return html.Div([
                html.H1('Revenue Graph', style={'text-align': 'center'}),  # style=common.text_style),
                dcc.Graph(
                    id='graph-1',
                    figure=tab1.fig_revenue_overall
                ),
                html.H1('Summary', style={'text-align': 'center'}),
                tab1.rev_summary_table_layout,
            ])

        elif tab == 'tab1' and subtab1 == 'subtab3':
            return html.Div([
                html.H1('Order type distribution', style={'text-align': 'center'}),  # style=common.text_style),
                html.Div([
                    dcc.Graph(id='order_type_fig', figure=tab1.order_type_fig)
                ], style={'width': '58%',
                          'margin-left': 'auto',
                          'margin-right': 'auto'}),
            ])

        elif tab == 'tab1' and subtab1 == 'subtab4':
            return html.Div([
                html.H1('Yearly Revenue Comparison', style={'text-align': 'center'}),
                dcc.Graph(id='YOY_fig', figure=tab1.YOY_fig)
            ])


        # ======================================================== TAB 2 ===================================================================
        # ==================================================================================================================================
        # ====================================================== CUSTOMER ==================================================================

        elif tab == 'tab2' and subtab2 == 'subtab5':
            return html.Div([

                html.H1('Number of Customers per segment : ', style={'text-align': 'center'}),
                # style=common.text_style),
                dcc.Graph(
                    id='NPS_fig',
                    figure=tab2.NPS_fig
                ),
                html.H1('Revenue per customer segment : ', style={'text-align': 'center'}),  # style=common.text_style),
                dcc.Graph(
                    id='RPS_fig',
                    figure=tab2.RPS_fig
                ),
                # html.H3(tab2.total_no_of_cust), #, style=common.text_style),
                html.Div([
                    html.P(tab2.total_no_of_cust),
                    html.P('Swiggy customers is not being considered for this analysis')
                ], style={'font-size': '1.2em',
                          'backgroundColor': 'rgb(204,204,255)',
                          'border-radius': '10px 10px 10px 10px',
                          'text-align': 'center'}),
            ])


        elif tab == 'tab2' and subtab2 == 'subtab7':
            return html.Div([
                html.H1('Frequency of New and Repeated Customers : ', style={'text-align': 'center'}),
                # style=common.text_style),
                dcc.Graph(
                    id='Repeat_new_cust',
                    figure=tab2.Repeat_new_cust
                ),
            ])

        elif tab == 'tab2' and subtab2 == 'subtab8':
            return html.Div([
                html.H1('Total Number of Customers : ', style={'text-align': 'center'}),  # style=common.text_style),
                dcc.Graph(
                    id='Total_cust',
                    figure=tab2.Total_cust
                ),
            ])

    # ======================================================== TAB 1 ==================================================================
    @app.callback(Output('O_MWD_fig', 'figure'),
                  [Input('I_MWD_fig', 'value')]
                  )
    def update_revenue_graph(value):
        new_daily_revenue = tab1.daily_revenue[tab1.daily_revenue.year == value].copy()
        new_daily_revenue["year"] = new_daily_revenue["year"].astype(str)
        new_daily_revenue["month"] = new_daily_revenue["month"].astype(str)

        new_daily_revenue["month"].replace(
            {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul",
             "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}, inplace=True)

        # MWD - Month with day comparison
        arr1 = 'Jan ' + new_daily_revenue['year']
        arr2 = 'Feb ' + new_daily_revenue['year']
        arr3 = 'Mar ' + new_daily_revenue['year']
        arr4 = 'Apr ' + new_daily_revenue['year']
        arr5 = 'May ' + new_daily_revenue['year']
        arr6 = 'Jun ' + new_daily_revenue['year']
        arr7 = 'Jul ' + new_daily_revenue['year']
        arr8 = 'Aug ' + new_daily_revenue['year']
        arr9 = 'Sep ' + new_daily_revenue['year']
        arr10 = 'Oct ' + new_daily_revenue['year']
        arr11 = 'Nov ' + new_daily_revenue['year']
        arr12 = 'Dec ' + new_daily_revenue['year']

        m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        arr = [arr1[len(arr1) - 1], arr2[0], arr3[0], arr4[0], arr5[0], arr6[0],
               arr7[0], arr8[0], arr9[0], arr10[0], arr11[0], arr12[0]]

        j = 0

        MWD_fig = go.Figure()

        for i in m:
            mon = new_daily_revenue['month'] == i
            revenue_mon = new_daily_revenue[mon]

            MWD_fig.add_trace(go.Line
                              (x=revenue_mon['day'], y=revenue_mon['total'], name=arr[j])
                              )

            j = j + 1

        MWD_fig.update_layout(
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1,
            )
        )

        MWD_fig.update_layout(
            # title="Daily Revenue for Each Month",
            xaxis_title="Day",
            yaxis_title="Revenue",
            font=dict(
                size=15
            ),
            plot_bgcolor='rgb(204,204,255)',
        )
        return MWD_fig

    # ======================================================== TAB 2 ===================================================================
    @app.callback(Output('datatable-interactivity', 'data'),
                  [Input('dropdown_interactivity', 'value')]
                  )
    def update_interactivity(value):
        final_rfm = tab2.segmented_rfm[tab2.segmented_rfm['Customer Segment'] == value]
        return final_rfm.to_dict('records')

    # ======================================================== TAB 3 ===================================================================
    # ==================================================================================================================================
    # ====================================================== PRODUCT ===================================================================

    @app.callback(Output('O_based_on_entire_data', 'figure'),
                  [Input('I_based_on_entire_data', 'value')])
    def update_graph_entire_data(value):
        if value == "Top_entire":
            top_product_df = tab3.productcustom_df.groupby(['item_name'], sort=False)['item_total'].sum().reset_index()
            top_product_df = top_product_df.sort_values(by='item_total', ascending=False)
            top_product_df = top_product_df.head(10)
            top_product_df = top_product_df.sort_values(by='item_total', ascending=True)

            fig = px.bar(top_product_df, x="item_total", y="item_name",
                         title='Overall Top Products for the entire data',
                         orientation='h', color_discrete_sequence=['rgb(153,0,153)'])
            fig.update_layout(
                xaxis_title="Contribution of a given dish in Rupees",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    # family="Courier New, monospace",
                    size=13,
                    # color="#7f7f7f"
                )

            )
            return fig
        else:
            bottom_product_df = tab3.productcustom_df.groupby(['item_name'], sort=False)[
                'item_total'].sum().reset_index()
            bottom_product_df = bottom_product_df.sort_values(by='item_total', ascending=True)
            bottom_product_df = bottom_product_df.head(10)
            bottom_product_df = bottom_product_df.sort_values(by='item_total', ascending=False)

            fig = px.bar(bottom_product_df, x="item_total", y="item_name",
                         title='Overall Bottom Products for the entire data',
                         orientation='h', color_discrete_sequence=['rgb(254,129,127)'])
            fig.update_layout(
                xaxis_title="Contribution of a given dish in Rupees",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )
            return fig

    @app.callback(Output('O_freq_based_on_entire_data', 'figure'),
                  [Input('I_based_on_entire_data', 'value')])
    def update_graph_freq_entire_data(value):
        if value == "Top_entire":
            dish_list = list(tab3.top_product_df.item_name)
            freq_list = list(tab3.productcustom_df[tab3.productcustom_df.item_name == i].shape[0] for i in dish_list)
            freq_df = pd.DataFrame({'dishes': dish_list, 'corresponding_freq': freq_list})

            fig = px.bar(freq_df, x="corresponding_freq", y="dishes", title='Frequency of these products',
                         orientation='h', color_discrete_sequence=['rgb(153,0,153)'])
            fig.update_layout(
                xaxis_title="Frequency at which each dish is ordered",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )
            return fig
        else:
            dish_list = list(tab3.bottom_product_df.item_name)
            freq_list = list(tab3.productcustom_df[tab3.productcustom_df.item_name == i].shape[0] for i in dish_list)
            freq_df = pd.DataFrame({'dishes': dish_list, 'corresponding_freq': freq_list})

            fig = px.bar(freq_df, x="corresponding_freq", y="dishes", title='Frequency of these products',
                         orientation='h', color_discrete_sequence=['rgb(254,129,127)'])
            fig.update_layout(
                xaxis_title="Frequency at which each dish is ordered",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )
            return fig

    @app.callback(
        Output('dropdown_options_left', 'options'),
        [Input('specifics_radio_left', 'value')]
    )
    def update_dropdown(selected_specific):
        return [{'label': i, 'value': i} for i in tab3.all_options[selected_specific]]

    @app.callback(Output("O_Month_Date_left", "figure"),
                  [Input("overall_radio_left", 'value'),
                   Input('specifics_radio_left', 'value'),
                   Input('dropdown_options_left', 'value')])
    def update_graph_left(ranking_type, sort_by, value):
        # print(ranking_type, sort_by, value)
        if ranking_type == 'Top' and sort_by == 'Month':
            selective_monthlyproduct_df = tab3.monthlyproduct_df[tab3.monthlyproduct_df['Month & Year'] == value]
            selective_monthlyproduct_df = selective_monthlyproduct_df.sort_values(by='item_total', ascending=False)
            selective_monthlyproduct_df = selective_monthlyproduct_df.head(10)
            selective_monthlyproduct_df = selective_monthlyproduct_df.sort_values(by='item_total', ascending=True)

            fig = px.bar(selective_monthlyproduct_df, x="item_total", y="item_name",
                         title='Overall Top Products for the period of ' + value, orientation='h',
                         color_discrete_sequence=['rgb(153,0,153)'])
            fig.update_layout(
                xaxis_title="Contribution of a given dish for the period of " + value + " in Rupees",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )
            return fig
        elif ranking_type == 'Bottom' and sort_by == 'Month':
            selective_monthlyproduct_df = tab3.monthlyproduct_df[tab3.monthlyproduct_df['Month & Year'] == value]
            selective_monthlyproduct_df = selective_monthlyproduct_df.sort_values(by='item_total', ascending=True)
            selective_monthlyproduct_df = selective_monthlyproduct_df.head(10)
            selective_monthlyproduct_df = selective_monthlyproduct_df.sort_values(by='item_total', ascending=False)

            fig = px.bar(selective_monthlyproduct_df, x="item_total", y="item_name",
                         title='Overall Bottom Products for the period of ' + value, orientation='h',
                         color_discrete_sequence=['rgb(254,129,127)'])
            fig.update_layout(
                xaxis_title="Contribution of a given dish for the period of " + value + " in Rupees",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )
            return fig
        elif ranking_type == 'Top' and sort_by == 'Day':
            daily_product_df = tab3.productcustom_df.groupby(['Day_Of_Week', 'item_name'], sort=False)[
                'item_total'].sum().reset_index()
            selective_daily_product_df = daily_product_df[daily_product_df['Day_Of_Week'] == value]
            selective_daily_product_df = selective_daily_product_df.sort_values(by='item_total', ascending=False)
            selective_daily_product_df = selective_daily_product_df.head(10)
            selective_daily_product_df = selective_daily_product_df.sort_values(by='item_total', ascending=True)

            fig = px.bar(selective_daily_product_df, x="item_total", y="item_name",
                         title='Overall Top Products on ' + value, orientation='h',
                         color_discrete_sequence=['rgb(153,0,153)']
                         )
            fig.update_layout(
                xaxis_title="Contribution to overall Revenue",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )

            return fig
        else:
            daily_product_df = tab3.productcustom_df.groupby(['Day_Of_Week', 'item_name'], sort=False)[
                'item_total'].sum().reset_index()
            selective_daily_product_df = daily_product_df[daily_product_df['Day_Of_Week'] == value]
            selective_daily_product_df = selective_daily_product_df.sort_values(by='item_total', ascending=True)
            selective_daily_product_df = selective_daily_product_df.head(10)
            selective_daily_product_df = selective_daily_product_df.sort_values(by='item_total', ascending=False)

            fig = px.bar(selective_daily_product_df, x="item_total", y="item_name",
                         title='Overall Bottom Products on ' + value,
                         orientation='h', color_discrete_sequence=['rgb(254,129,127)']
                         )
            fig.update_layout(
                xaxis_title="Contribution to overall Revenue",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )

            return fig

    @app.callback(
        Output('dropdown_options_right', 'options'),
        [Input('specifics_radio_right', 'value')]
    )
    def update_dropdown(selected_specific):
        return [{'label': i, 'value': i} for i in tab3.all_options[selected_specific]]

    @app.callback(Output("O_Month_Date_right", "figure"),
                  [Input("overall_radio_right", 'value'),
                   Input('specifics_radio_right', 'value'),
                   Input('dropdown_options_right', 'value')])
    def update_graph_right(ranking_type, sort_by, value):
        # print(ranking_type, sort_by, value)
        if ranking_type == 'Top' and sort_by == 'Month':
            selective_monthlyproduct_df = tab3.monthlyproduct_df[tab3.monthlyproduct_df['Month & Year'] == value]
            selective_monthlyproduct_df = selective_monthlyproduct_df.sort_values(by='item_total', ascending=False)
            selective_monthlyproduct_df = selective_monthlyproduct_df.head(10)
            selective_monthlyproduct_df = selective_monthlyproduct_df.sort_values(by='item_total', ascending=True)

            fig = px.bar(selective_monthlyproduct_df, x="item_total", y="item_name",
                         title='Overall Top Products for the period of ' + value, orientation='h',
                         color_discrete_sequence=['rgb(153,0,153)'])
            fig.update_layout(
                xaxis_title="Contribution of a given dish for the period of " + value + " in Rupees",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )
            return fig
        elif ranking_type == 'Bottom' and sort_by == 'Month':
            selective_monthlyproduct_df = tab3.monthlyproduct_df[tab3.monthlyproduct_df['Month & Year'] == value]
            selective_monthlyproduct_df = selective_monthlyproduct_df.sort_values(by='item_total', ascending=True)
            selective_monthlyproduct_df = selective_monthlyproduct_df.head(10)
            selective_monthlyproduct_df = selective_monthlyproduct_df.sort_values(by='item_total', ascending=False)

            fig = px.bar(selective_monthlyproduct_df, x="item_total", y="item_name",
                         title='Overall Bottom Products for the period of ' + value, orientation='h',
                         color_discrete_sequence=['rgb(254,129,127)'])
            fig.update_layout(
                xaxis_title="Contribution of a given dish for the period of " + value + " in Rupees",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )
            return fig
        elif ranking_type == 'Top' and sort_by == 'Day':
            daily_product_df = tab3.productcustom_df.groupby(['Day_Of_Week', 'item_name'], sort=False)[
                'item_total'].sum().reset_index()
            selective_daily_product_df = daily_product_df[daily_product_df['Day_Of_Week'] == value]
            selective_daily_product_df = selective_daily_product_df.sort_values(by='item_total', ascending=False)
            selective_daily_product_df = selective_daily_product_df.head(10)
            selective_daily_product_df = selective_daily_product_df.sort_values(by='item_total', ascending=True)

            fig = px.bar(selective_daily_product_df, x="item_total", y="item_name",
                         title='Overall Top Products on ' + value,
                         orientation='h', color_discrete_sequence=['rgb(153,0,153)']
                         )
            fig.update_layout(
                xaxis_title="Contribution to overall Revenue",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )

            return fig
        else:
            daily_product_df = tab3.productcustom_df.groupby(['Day_Of_Week', 'item_name'], sort=False)[
                'item_total'].sum().reset_index()
            selective_daily_product_df = daily_product_df[daily_product_df['Day_Of_Week'] == value]
            selective_daily_product_df = selective_daily_product_df.sort_values(by='item_total', ascending=True)
            selective_daily_product_df = selective_daily_product_df.head(10)
            selective_daily_product_df = selective_daily_product_df.sort_values(by='item_total', ascending=False)

            fig = px.bar(selective_daily_product_df, x="item_total", y="item_name",
                         title='Overall Bottom Products on ' + value,
                         orientation='h', color_discrete_sequence=['rgb(254,129,127)']
                         )
            fig.update_layout(
                xaxis_title="Contribution to overall Revenue",
                yaxis_title="Dishes",
                paper_bgcolor="rgb(240,240,240)",
                plot_bgcolor='rgba(0,0,0,0)',
                title={
                    'y': 0.9,
                    'x': 0.5
                },
                font=dict(
                    size=13,
                )
            )

            return fig

    @app.callback([Output('O_rules_custom', 'columns'), Output('O_rules_custom', 'data')],
                  [Input('I_rules_custom', 'value')]
                  )
    def update_rules_custom(value):
        if value == 'None':
            columns = []
            data = []
            return columns, data
        else:
            custom_table = tab3.rules_custom[['antecedents', 'consequents', 'confidence', 'support']]
            custom_table.columns = ['Product', 'Associated Product', 'Percentage of Confidence', 'Percentage of Orders']
            custom_table['Percentage of Confidence'] = custom_table['Percentage of Confidence'].apply(
                lambda x: round(x * 100, 2))
            custom_table['Percentage of Orders'] = custom_table['Percentage of Orders'].apply(
                lambda x: round(x * 100, 2))
            custom_table.insert(0, 'Serial No.', range(1, 1 + len(custom_table)))

            custom_table = custom_table[custom_table['Product'] == value]
            custom_table = custom_table[['Associated Product', 'Percentage of Confidence', 'Percentage of Orders']]
            columns = [{"name": i, "id": i} for i in custom_table.columns]
            data = custom_table.to_dict('records')
            return columns, data

    @app.callback([Output('O_Percentage_Of_Sales', 'children'),
                   Output('O_Product_SalePrice', 'children'),
                   Output('O_Revenue_of_product', 'children'),
                   Output('O_Number_Of_Transactions', 'children')],
                  [Input('I_Prod_A_name', 'value')])
    def return_saleprice(value):
        if value == None:
            return None, None, None, None
        elif value == 'None':
            return None, None, None, None
        else:
            # Selects the % of transaction for a particular dish
            ProductA = tab3.TopSupport[tab3.TopSupport['Product'] == value]
            ProductA_perc_Trns = ProductA.iloc[0, 2]

            # Selects the selling price of the most selling product
            sale_price = data[['item_name', 'item_price']][
                data['item_name'] == value]
            sale_price_table = sale_price.item_price.value_counts()
            sale_price_table = sale_price_table.reset_index()
            sale_price_table.columns = [['Sale_Price', 'Frequency']]
            price_ProductA = sale_price_table.iat[0, 0]

            # Finds the previous number of transactions and the revenue contributed by the product
            Total_Trns = len(list(data.invoice_no.unique()))
            Total_Trns = round(Total_Trns)
            Number_Of_Trns = ((ProductA_perc_Trns / 100) * Total_Trns)
            Number_Of_Trns = round(Number_Of_Trns)
            Revenue_of_product = ((ProductA_perc_Trns / 100) * Total_Trns) * price_ProductA
            Revenue_of_product = round(Revenue_of_product)
            return ProductA_perc_Trns, price_ProductA, Revenue_of_product, Number_Of_Trns

    @app.callback(Output('O_suggest_target', 'children'),
                  [Input('I_ProductA_new_price', 'value'),
                   Input('I_Prod_A_name', 'value')])
    def suggested_target(value, product_name):
        if value is None and product_name == 'None':  # Good correction Input and Drop down sends input values differently
            return None
        elif value is None:
            return None
        elif product_name == 'None':
            return None
        elif product_name is None:
            return None
        elif value == '':
            return None
        else:
            # Selects the % of transaction for a particular dish
            ProductA = tab3.TopSupport[tab3.TopSupport['Product'] == product_name]
            ProductA_perc_Trns = ProductA.iloc[0, 2]

            # Selects the selling price of the most selling product
            sale_price = data[['item_name', 'item_price']][
                data['item_name'] == product_name]
            sale_price_table = sale_price.item_price.value_counts()
            sale_price_table = sale_price_table.reset_index()
            sale_price_table.columns = [['Sale_Price', 'Frequency']]
            price_ProductA = sale_price_table.iat[0, 0]

            # Recalculates the revenue earned by original price
            # Finds the new target required for sales numbers
            Total_Trns = len(list(data.invoice_no.unique()))
            Revenue_of_product = ((ProductA_perc_Trns / 100) * Total_Trns) * price_ProductA
            Revenue_of_product = round(Revenue_of_product, 0)
            new_target = Revenue_of_product / int(value)
            new_target = round(new_target, 0)

            return new_target

    @app.callback([Output('O_As_Percentage_Of_Sales', 'children'),
                   Output('O_As_ProductA_SalePrice', 'children'),
                   Output('O_As_ProductB_SalePrice', 'children'),
                   Output('O_As_Number_Of_Transactions', 'children'),
                   Output('O_As_Revenue_of_products', 'children'),
                   Output('O_As_TotalPrice', 'children'),
                   ],
                  [Input('I_As_Prod_A_name', 'value'),
                   Input('I_As_Prod_B_name', 'value')])
    def return_saleprice(Prod_A_name, Prod_B_name):
        if Prod_A_name == 'None':
            return None, None, None, None, None, None
        elif Prod_B_name == 'None':
            return None, None, None, None, None, None
        else:
            # Selects the % of transaction for that particular associations of products

            custom_table = tab3.rules_custom[['antecedents', 'consequents', 'confidence', 'support']]
            custom_table.columns = ['Product', 'Associated Product', 'Percentage of Confidence', 'Percentage of Orders']
            custom_table['Percentage of Confidence'] = custom_table['Percentage of Confidence'].apply(
                lambda x: round(x * 100, 2))
            custom_table['Percentage of Orders'] = custom_table['Percentage of Orders'].apply(
                lambda x: round(x * 100, 2))
            custom_table.insert(0, 'Serial No.', range(1, 1 + len(custom_table)))
            custom_table = custom_table[custom_table['Product'] == Prod_A_name]
            custom_table = custom_table[['Associated Product', 'Percentage of Confidence', 'Percentage of Orders']]
            no_consequent_elements = len(list(custom_table['Associated Product'].unique()))
            if no_consequent_elements == 0:
                return None, None, None, None, None, None
            else:
                custom_table = custom_table[custom_table['Associated Product'] == Prod_B_name]
                conditional_no_consequent_elements = len(list(custom_table['Associated Product'].unique()))
                if conditional_no_consequent_elements == 0:
                    return None, None, None, None, None, None
                else:
                    As_Product_Perc_Transactions = custom_table.iloc[0, 2]

                    # Selects the selling price of the most selling product A
                    sale_price = data[['item_name', 'item_price']][
                        data['item_name'] == Prod_A_name]
                    sale_price_table = sale_price.item_price.value_counts()
                    sale_price_table = sale_price_table.reset_index()
                    sale_price_table.columns = [['Sale_Price', 'Frequency']]
                    price_ProductA = sale_price_table.iat[0, 0]

                    # Selects the selling price of the most selling product B
                    sale_price = data[['item_name', 'item_price']][
                        data['item_name'] == Prod_B_name]
                    sale_price_table = sale_price.item_price.value_counts()
                    sale_price_table = sale_price_table.reset_index()
                    sale_price_table.columns = [['Sale_Price', 'Frequency']]
                    price_ProductB = sale_price_table.iat[0, 0]

                    As_TotalPrice = price_ProductA + price_ProductB

                    # Finds the previous number of transactions and the revenue contributed by the product
                    Total_Trns = len(list(data.invoice_no.unique()))
                    Total_Trns = round(Total_Trns)
                    Number_Of_Trns = ((As_Product_Perc_Transactions / 100) * Total_Trns)
                    Number_Of_Trns = round(Number_Of_Trns)
                    As_Revenue_of_products = ((As_Product_Perc_Transactions / 100) * Total_Trns) * (
                            price_ProductA + price_ProductB)
                    As_Revenue_of_products = round(As_Revenue_of_products)

                    return As_Product_Perc_Transactions, price_ProductA, price_ProductB, Number_Of_Trns, As_Revenue_of_products, As_TotalPrice

    # Callback function for Muli-Product Discount Calculator Begins
    @app.callback([Output('O_Multi_suggest_target', 'children'),
                   Output('O_As_ComboPrice', 'children')],
                  [Input('I_Multi_ProductA_new_price', 'value'),
                   Input('I_Multi_ProductB_new_price', 'value'),
                   Input('I_As_Prod_A_name', 'value'),
                   Input('I_As_Prod_B_name', 'value')])
    def suggested_target(ProductA_new_price, ProductB_new_price, Prod_A_name, Prod_B_name):
        if ProductA_new_price is None or ProductB_new_price is None:
            return None, None
        if ProductA_new_price == '' or ProductB_new_price == '':
            return None, None
        if Prod_A_name == 'None' or Prod_B_name == 'None':
            return None, None
        else:
            # Selects the % of transaction for that particular associations of products

            custom_table = tab3.rules_custom[['antecedents', 'consequents', 'confidence', 'support']]
            custom_table.columns = ['Product', 'Associated Product', 'Percentage of Confidence', 'Percentage of Orders']
            custom_table['Percentage of Confidence'] = custom_table['Percentage of Confidence'].apply(
                lambda x: round(x * 100, 2))
            custom_table['Percentage of Orders'] = custom_table['Percentage of Orders'].apply(
                lambda x: round(x * 100, 2))
            custom_table.insert(0, 'New_ID', range(1, 1 + len(custom_table)))
            custom_table = custom_table[custom_table['Product'] == Prod_A_name]
            custom_table = custom_table[['Associated Product', 'Percentage of Confidence', 'Percentage of Orders']]
            no_consequent_elements = len(list(custom_table['Associated Product'].unique()))
            if no_consequent_elements == 0:
                return None, None
            else:
                custom_table = custom_table[custom_table['Associated Product'] == Prod_B_name]
                conditional_no_consequent_elements = len(list(custom_table['Associated Product'].unique()))
                if conditional_no_consequent_elements == 0:
                    return None, None
                else:
                    As_Product_Perc_Transactions = custom_table.iloc[0, 2]

                    # Selects the selling price of the most selling product A
                    sale_price = data[['item_name', 'item_price']][
                        data['item_name'] == Prod_A_name]
                    sale_price_table = sale_price.item_price.value_counts()
                    sale_price_table = sale_price_table.reset_index()
                    sale_price_table.columns = [['Sale_Price', 'Frequency']]
                    price_ProductA = sale_price_table.iat[0, 0]

                    # Selects the selling price of the most selling product B
                    sale_price = data[['item_name', 'item_price']][
                        data['item_name'] == Prod_B_name]
                    sale_price_table = sale_price.item_price.value_counts()
                    sale_price_table = sale_price_table.reset_index()
                    sale_price_table.columns = [['Sale_Price', 'Frequency']]
                    price_ProductB = sale_price_table.iat[0, 0]
                    As_TotalPrice = price_ProductA + price_ProductB

                    # Finds the previous number of transactions and the revenue contributed by the product
                    Total_Trns = len(list(data.invoice_no.unique()))
                    Total_Trns = round(Total_Trns)
                    Number_Of_Trns = ((As_Product_Perc_Transactions / 100) * Total_Trns)
                    Number_Of_Trns = round(Number_Of_Trns)
                    As_Revenue_of_products = ((As_Product_Perc_Transactions / 100) * Total_Trns) * (
                            price_ProductA + price_ProductB)
                    As_Revenue_of_products = round(As_Revenue_of_products)
                    ComboPrice = (int(ProductA_new_price) + int(ProductB_new_price))
                    As_suggested_target = As_Revenue_of_products / ComboPrice
                    As_suggested_target = round(As_suggested_target)
            return As_suggested_target, ComboPrice

    return app


if __name__ == '__main__':
    #try:
    app = run_my_program()  # For the purpose of Multi-processing.
    from Web_browser import *

    load_browser()
    app.run_server(port=2002, debug=False, use_reloader=False)

    #except Exception:
     #   print('Sorry, there is an Error!')

