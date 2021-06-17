
# For Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#from specific functions
from components.functions import results_assessment, graph_histogram

# For graph
import plotly.express as px
#import shap

#for model
from joblib import load
import xgboost
import pandas as pd
import sklearn
#import sklearn.preprocessing





external_stylesheets = ['bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

cachedir = 'Data/'
VERSION_NAME="full_compressed_sampled_307511"
days_conversion = -0.0328767
label_min_value = 48

train_histo = pd.read_pickle(cachedir+"train_final_df_histogram"+VERSION_NAME+".pkl")
y_train = pd.read_pickle(cachedir+"train_label"+VERSION_NAME+".pkl")
test = pd.read_pickle(cachedir+"test_final_df"+VERSION_NAME+".pkl")
y_test = pd.read_pickle(cachedir+"test_label"+VERSION_NAME+".pkl")

#train = train.set_index("SK_ID_CURR")
##y_train = y_train.set_index("SK_ID_CURR")
#test = test.set_index("SK_ID_CURR")
#y_test = y_test.set_index("SK_ID_CURR")


model = xgboost.XGBClassifier()
model.load_model(cachedir+'modelxgboost3'+VERSION_NAME+'.json')
#model = load(cachedir+"modelxgboost3"+VERSION_NAME)

loan_selected_index = test.iloc[0,:].name
test.loc["New_loan",:] = test.loc[loan_selected_index,:]


list_features_selection = ['age','AMT_INCOME_TOTAL',
                            'AMT_CREDIT','DAYS_EMPLOYED',
                            'NEW_CREDIT_TO_GOODS_RATIO',
                            'NEW_EXT_SOURCES_PROD','NEW_EXT_SOURCES_MEAN',
                            'AMT_GOODS_PRICE',
                            'AMT_ANNUITY']

train_histogram = pd.concat([train_histo,y_train],axis=1)[['TARGET']+list_features_selection].fillna(0)
train_histogram['DAYS_EMPLOYED']=train_histogram['DAYS_EMPLOYED']*days_conversion


result_assessment_model = model.predict_proba(test.loc[[loan_selected_index,"New_loan",],])

red_button_style = {'background-color': 'red',
                    'color': 'white'}
normal_button_style={'fontsize':'12px'}

################# INTERACTIONS #########################
slider_age=dcc.RangeSlider(
    id='slider_age',
    min=18,
    max=70,
    marks={i: '{} years'.format(i) for i in range(18, 70) if i%10==0},
    value=[18,70]
    )

slider_revenu=dcc.RangeSlider(id='slider_revenu',
                    min=0,
                    max=100,
                    marks={i: '{} k$'.format(int(i*10)) for i in range(0, 100) if i%10==0
                            },
                    value=[0,100])


Loans_selection = dcc.Dropdown(id='loans_selection',
    options=[{'label': SK_ID, 'value': SK_ID} for SK_ID in y_test.index],
    value=loan_selected_index,
    searchable=True,
    multi=False,
    optionHeight=30
)

Features_histogram_selection = dcc.Dropdown(id='features_histogram_selection',
    options=[{'label': feat, 'value': feat} for feat in list_features_selection],
    value='NEW_EXT_SOURCES_PROD',
    searchable=True,
    multi=False,
    optionHeight=30
)

ratio_value_input = dcc.Input(
                    id="ratio_input", 
                    type="number", 
                    placeholder="New credit to goods ratio",
                    min=0,
                    value=round(test.loc[loan_selected_index,'NEW_CREDIT_TO_GOODS_RATIO'],2)
                    )

AMT_GOODS_PRICE_value_input =dcc.Input(
                    id="AMT_GOODS_PRICE_input", type="number", placeholder="Good prices",
                    min=0,
                    value=round(test.loc[loan_selected_index,'AMT_GOODS_PRICE'],3)
                    )

DAYS_EMPLOYED_value_input =dcc.Input(
                    id="DAYS_EMPLOYED_input", type="number", placeholder="Days worked",
                    min=0,
                    value= round(test.loc[loan_selected_index,'DAYS_EMPLOYED']*days_conversion,1)
                    )                   
################# FIGURES ############################
Histogram = dcc.Graph(
        id='histo_graph',
        figure=graph_histogram(df=train_histogram,
                    loan_test_value=0,
                    feature_figure_1 = 'NEW_EXT_SOURCES_PROD',
                    min_revenu_value = 0,
                    max_revenu_value = 1000000,
                    min_age_value = 0,
                    max_age_value = 99
                    )
)

result_assessment = dcc.Graph(
    id='result_assessment',
    figure=results_assessment(min_value=label_min_value, 
                            your_application_value = round(result_assessment_model[1,0],2)*100
                            )
    )

text_result_assessment = html.Label('To pass, your result must be over 48%',
                    id='text_assement',
                    style={'fontsize':'6px'})


app.layout = html.Div([
    html.Header([
        html.Div([
                html.Label('Select age range'),
                slider_age,
                html.Hr(className="light"),

                html.Label('Select revenu range'),
                slider_revenu
                ],                
        style={
            'width': '48%', 
            'display': 'inline-block',
            'margin-top': '1.5rem',
            'margin-bottom': '1.5rem'
            }
                ),
        html.Div([
            html.Label('Selection of the loans'),
            Loans_selection,
            html.Hr(className="light"),

            html.Label('Selection of the feature'),
            Features_histogram_selection,
            html.Hr(className="light"),
            
            
            html.Div([        
                html.Label('Goods price',style={'fontsize':'6px'}),
                html.Br(),
                AMT_GOODS_PRICE_value_input
                ],
                style={'width': '25%', 'display': 'inline-block','float': 'left'}
                ),

            html.Div([              
                html.Label('Credit/annuity ratio',style={'fontsize':'6px'}),
                html.Br(),
                ratio_value_input
                ],
                style={
                    'width': '25%', 
                    'display': 'inline-block',
                    'float': 'center'
                    }
                ),
            html.Div([ 
                html.Button('Original values',
                    value='Original values', 
                    id='button_update', 
                    n_clicks=0,
                    className = "Buttons",
                    type='button',
                    style=normal_button_style)],
                style={
                    'width': '25%', 
                    'display': 'inline-block',
                    'float': 'right'
                    }
                ),
            html.Div([              
                html.Label('Months worked',style={'fontsize':'6px'}),
                html.Br(),
                DAYS_EMPLOYED_value_input
                ],
                style={
                    'width': '25%', 
                    'display': 'inline-block',
                    'float': 'center'
                    }
                )
                ],                
            style={
                'width': '48%', 
                'display': 'inline-block',
                'float': 'right'
                }

            )
            ],
        style={
            'marginBottom': 5, 
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
                }
            ),

    html.Div([
            html.Div([
                result_assessment,
                text_result_assessment
                ],style={'width': '39%','display': 'inline-block','float': 'center'}),
            html.Div([
                Histogram,
                html.Label("Black Dashed line represents the applicant value. \n Green dashed line represents the new value entered.")
                ],style={'width': '60%','display': 'inline-block','float': 'right'}),
            ],
            style={'display': 'inline-block',"background-color":'white'}),
            ])



################### Update ratio graph
@app.callback(
    dash.dependencies.Output('histo_graph', 'figure'),
    [dash.dependencies.Input('slider_revenu', 'value'),
     dash.dependencies.Input('slider_age', 'value'),
    dash.dependencies.Input('loans_selection', 'value'),
    dash.dependencies.Input('features_histogram_selection','value'),
    dash.dependencies.Input('ratio_input', 'value'),
    dash.dependencies.Input('AMT_GOODS_PRICE_input', 'value'),
    dash.dependencies.Input('DAYS_EMPLOYED_input', 'value')])

def update_graph(revenu_value, age_value,loans_id,feature_selected,new_ratio_value,new_AMT_GOODS_PRICE,new_DAYS_EMPLOYED):

    fig = graph_histogram(df=train_histogram,
                    loan_test_value = test.loc[loans_id,feature_selected],
                    feature_figure_1 = feature_selected,
                    min_revenu_value = revenu_value[0]*10000,
                    max_revenu_value = revenu_value[1]*10000,
                    min_age_value = age_value[0],
                    max_age_value = age_value[1]
                    )
    
    fig.update_layout(
        title_font_family="arial",
        title_font_color = "black",
        title=feature_selected +'(Revenu : ' + str(revenu_value[0]*10) + " - " + str(revenu_value[1]*10) + "k$ / age :" + str(age_value[0]) + " - " + str(age_value[1]) +")"
        )
    
    
    if feature_selected=='NEW_CREDIT_TO_GOODS_RATIO':
        fig.add_shape(type="line", yref="paper",
            x0=new_ratio_value, 
            y0=0, 
            x1=new_ratio_value, 
            y1=0.70,
            line=dict(color="green",
                    dash="dash",
                    width=3),
                    name="New credit to annuity ratio"
        )

    elif feature_selected=='DAYS_EMPLOYED':
        
        fig = graph_histogram(df=train_histogram[train_histogram[feature_selected]<500],
                    loan_test_value = test.loc[loans_id,feature_selected]*days_conversion,
                    feature_figure_1 = feature_selected,
                    min_revenu_value = revenu_value[0]*10000,
                    max_revenu_value = revenu_value[1]*10000,
                    min_age_value = age_value[0],
                    max_age_value = age_value[1]
                    )

        fig.add_shape(type="line", yref="paper",
            x0=new_DAYS_EMPLOYED, 
            y0=0, 
            x1=new_DAYS_EMPLOYED, 
            y1=0.70,
            line=dict(color="green",
                    dash="dash",
                    width=3),
                    name="New DAYS worked"
        )
        fig.update_layout(
            title_font_family="arial",
            title_font_color = "black",
            title="Month Worked (Revenu : " + str(revenu_value[0]*10) + " - " + str(revenu_value[1]*10)+"k$ / age :" + str(age_value[0]) + " - " + str(age_value[1]) +")",
            xaxis_title="Months Worked",
            )
    

    elif feature_selected=='AMT_GOODS_PRICE':
        fig.add_shape(type="line", yref="paper",
            x0=new_AMT_GOODS_PRICE, 
            y0=0, 
            x1=new_AMT_GOODS_PRICE, 
            y1=0.70,
            line=dict(color="green",
                    dash="dash",
                    width=3),
                    name="New value for EXT_SOURCES_MEAN"
        )                    

    
    
    return fig
#########################################

################### UPDATE data
@app.callback(
    [dash.dependencies.Output('ratio_input', 'value'),
    dash.dependencies.Output('AMT_GOODS_PRICE_input', 'value'), 
    dash.dependencies.Output('DAYS_EMPLOYED_input', 'value'),
    dash.dependencies.Output('button_update', 'value'),
    dash.dependencies.Output('button_update', 'style')],
    [dash.dependencies.Input('button_update', 'n_clicks'),
    dash.dependencies.Input('loans_selection', 'value'),
    dash.dependencies.Input('ratio_input', 'value'),
    dash.dependencies.Input('AMT_GOODS_PRICE_input', 'value'),
    dash.dependencies.Input('DAYS_EMPLOYED_input', 'value')])

def update_ratio_value(btn1, loan_id, new_ratio_value,new_AMT_GOODS_PRICE,new_DAYS_EMPLOYED):

    ctx = dash.callback_context
   
    if not ctx.triggered:
        New_button_value = 'Original values'
        style=normal_button_style
        new_AMT_GOODS_PRICE = round(test.loc[loan_id,'AMT_GOODS_PRICE'],3)
        new_DAYS_EMPLOYED = round(test.loc[loan_id,'DAYS_EMPLOYED']*days_conversion,1)
        new_ratio = round(test.loc[loan_id,'NEW_CREDIT_TO_GOODS_RATIO'],3)
    else:    
        last_change = ctx.triggered[0]['prop_id'].split('.')[0]
        New_button_value = 'Original values'
        style=normal_button_style
        if last_change=='loans_selection' or last_change=='button_update' and btn1>0:
            new_ratio = round(test.loc[loan_id,'NEW_CREDIT_TO_GOODS_RATIO'],3)
            new_AMT_GOODS_PRICE = round(test.loc[loan_id,'AMT_GOODS_PRICE'],3)
            new_DAYS_EMPLOYED = round(test.loc[loan_id,'DAYS_EMPLOYED']*days_conversion,1)
            New_button_value = 'Original values'
            style=normal_button_style

        elif new_DAYS_EMPLOYED != round(test.loc[loan_id,'DAYS_EMPLOYED']*days_conversion,1) \
        or new_AMT_GOODS_PRICE != round(test.loc[loan_id,'AMT_GOODS_PRICE'],3) \
        or new_ratio_value != round(test.loc[loan_id,'NEW_CREDIT_TO_GOODS_RATIO'],3):
            
            New_button_value = 'UPDATED values'
            new_ratio = new_ratio_value
            new_AMT_GOODS_PRICE = new_AMT_GOODS_PRICE
            new_DAYS_EMPLOYED = new_DAYS_EMPLOYED
            style = red_button_style
        else:
            new_ratio = round(test.loc[loan_id,'NEW_CREDIT_TO_GOODS_RATIO'],3)
            new_AMT_GOODS_PRICE = round(test.loc[loan_id,'AMT_GOODS_PRICE'],3)
            new_DAYS_EMPLOYED = round(test.loc[loan_id,'DAYS_EMPLOYED']*days_conversion,1)
            New_button_value = 'Original values'
            style=normal_button_style
    
    return new_ratio,new_AMT_GOODS_PRICE, new_DAYS_EMPLOYED, New_button_value,style
#########################################

################### Update Result Assesment
@app.callback(
    dash.dependencies.Output('result_assessment', 'figure'),
    dash.dependencies.Output('text_assement', component_property='children'),
    [dash.dependencies.Input('loans_selection', 'value'),
    dash.dependencies.Input('ratio_input', 'value'),
    dash.dependencies.Input('AMT_GOODS_PRICE_input', 'value'),
    dash.dependencies.Input('DAYS_EMPLOYED_input', 'value')])

def update_graph(loans_id,new_ratio_value,new_AMT_GOODS_PRICE,new_DAYS_EMPLOYED):

    test.loc["New_loan",:] = test.loc[loans_id,:]
    test.loc["New_loan",'NEW_CREDIT_TO_GOODS_RATIO']=new_ratio_value
    test.loc["New_loan",'AMT_GOODS_PRICE']=new_AMT_GOODS_PRICE
    test.loc["New_loan",'DAYS_EMPLOYED']=new_DAYS_EMPLOYED/days_conversion
    result_assessment_model_updated = round(model.predict_proba(test.loc[[loans_id,"New_loan"],:])[1,0]*100,0)


                      
    #fig.update_layout(title='Your application results : ' + str(result_assessment_model_updated) + "%")
    if result_assessment_model_updated>label_min_value:
        title ="Your loans will be accepted. \
                \n Your result is " + str(result_assessment_model_updated) + "% \
                \n (above the minimum value " + str(label_min_value) + "%)"
        fig = results_assessment(min_value=label_min_value, 
                            your_application_value = result_assessment_model_updated
                            )
    else:
        title = "Your loans will NOT be accepted. \
                \n Your result is " + str(result_assessment_model_updated) + "% \
                \n (under the minimum value " + str(label_min_value) + "%)"
        fig = results_assessment(min_value=label_min_value, 
                            your_application_value = result_assessment_model_updated
                            )
                    
     
   
    return fig,title



#########################################

if __name__ == '__main__':
    app.run_server(debug=False)
