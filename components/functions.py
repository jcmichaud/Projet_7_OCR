import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


#Result figure

############################ DONUT GRAPH RESULT ########################################################################## 
def results_assessment(min_value=48,your_application_value = 85):

  label_min_value = str(min_value)+"%"
  label_your_application_value = str(your_application_value)+"%"

  if min_value < your_application_value: 

      values = [0,
                min_value,
                your_application_value-min_value,
                100 - your_application_value
                ]

      labels = ["Passed",
                label_min_value,
                label_your_application_value,
                "  "               
                ]

      color_label = ['green',
                     'black',
                     'black',
                     'black',
                    ]

      colors_pie = ['white',
                'darkgreen',
                'lightgreen',
                'whitesmoke'
                ]

      colors_line = ['black',
                'black',
                'black',
                'black'
                ]

      parents=["", 
               "Passed", 
               "Passed", 
               "Passed"]

      text = ["Results",            
              'Minimum result to accept the loan',
              'Your result',
              '']
      #title = "Your loans will be accepted. Your result is " + str(your_application_value) + "% (above the minimum value" + label_min_value + ")"

      rotation = 90   #90-(100 - your_application_value)*360/100


  elif min_value > your_application_value: 
      #values = [100-min_value, min_value-your_application_value,your_application_value]
      #colors = ['darkorange',"bisque",'white']
      #labels = [str(your_application_value)+"%",str(min_value)+"%",'']
      #text = ['Your result','Minimum result to accept the loan','']
      #annotations = [dict(text='Minimum', x=0.6, y=-0.05, font_size=20, font_color="bisque", showarrow=False)]
      #rotation = -your_application_value/100*360

      values = [0,
                your_application_value,
                min_value-your_application_value,
                100 - min_value
                ]

      labels = ["Failled",             
                label_your_application_value,
                label_min_value,
                "  "               
                ]
      color_label = ['red',
                     'black',
                     'black',
                     'black',
                    ]

      colors_pie = ['white',
                'darkorange',
                "bisque",
                'whitesmoke'
                ]

      colors_line = ['black',
                'black',
                'black',
                'black'
                ]

      parents=["", 
               "Failled", 
               "Failled", 
               "Failled"]

      text = ["Results",
              'Your result',            
              'Minimum result to accept the loan',
              '']

     
      rotation = 90  

      # Use `hole` to create a donut-like pie char
  fig = go.Figure(go.Sunburst(
                  labels=labels,
                  parents=parents,
                  values=values,
                  ))

  fig.update_traces(name="Pie chart result",
                    rotation = rotation,
                    hoverinfo="text",
                    text=text,
                    textinfo='label',
                    insidetextorientation='horizontal',
                    sort=False,
                    textfont_size=20,
                    marker=dict(colors=colors_pie, line=dict(color=colors_line, width=2)),
                    textfont=dict(size=[50,20,20,20],color=color_label),
                    opacity=0.7
                   )

  fig.update_layout(title_text="Result of your assessment",
                    title_xref='paper',
                    font=dict(
                        family="arial",
                        size=12,
                        color="black"
                            ),
                    width=300,
                    height=400)
  return fig


############################ HISTOGRAMME GRAPH RESULT ##########################################################################
def graph_histogram(df,
                    loan_test_value,
                    feature_figure_1 = 'AMT_CREDIT',
                    min_revenu_value = 100000,
                    max_revenu_value = 200000,
                    min_age_value = 30,
                    max_age_value = 39
                    ):

    min_revenu_condition = df['AMT_INCOME_TOTAL']>=min_revenu_value
    max_revenu_condition = df['AMT_INCOME_TOTAL']<=max_revenu_value

    

    min_age_condition = df['age']>=min_age_value
    max_age_condition = df['age']<=max_age_value

    temp_df = df.loc[
                (df['TARGET']!=-999)
                & min_revenu_condition
                & max_revenu_condition
                & min_age_condition
                & max_age_condition
                ,:].copy()

    temp_df[feature_figure_1]=temp_df[feature_figure_1].fillna(0)            

    fig = px.histogram(temp_df.fillna(0), 
                    x=feature_figure_1,
                    color='TARGET',
                    hover_data=[feature_figure_1,'AMT_INCOME_TOTAL','age','TARGET'],
                    histnorm='density',
                    marginal="box"
                    )

    fig.add_shape(type="line", yref="paper",
              x0=loan_test_value, 
              y0=0, 
              x1=loan_test_value, 
              y1=0.70,
              line=dict(color="black",
                        dash="dash",
                        width=3)
)
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.5)
    fig.update_layout(barmode="overlay", 
                        width=1000, 
                        height=400)

    return fig


    





