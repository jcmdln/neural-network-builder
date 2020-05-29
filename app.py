import streamlit as st
import pandas as pd
from fastai.tabular import *
import plotly.express as px

st.title('Test for importing csv and making a neural network utilizing fast.ai')
'''### Please upload a clean csv below
### A clean CSV has had all nulls removed or otherwise properly filled
'''
file = st.file_uploader('Please upload a cleaned CSV', type=['csv'])
if file is not None:
    df = pd.read_csv(file)
    st.subheader('Please verify the contents of your file')
    df

    #----------------------------------------------------------
    #fastai variable definitions begin below this line
    #----------------------------------------------------------

    available_processing = ['Categorify', 'FillMissing', 'Normalize']
    procs_dict = {'Categorify': Categorify, 'FillMissing': FillMissing, 'Normalize': Normalize}
    procs = st.multiselect('Please select any preprocessing that you would like to complete',
                           available_processing)
    predict_var = st.selectbox('Please select your dependant variable (Prediction Target)', df.columns)
    input_nodes = len(df.columns)-1
    output_nodes = len(df[predict_var].unique())
    recommended_hidden = int(((2/3)*input_nodes)+output_nodes)
    df_options = df.loc[:, df.columns != predict_var]
    cat_names = st.multiselect('Please select your categorical variables (Discrete Options)', df_options.columns)
    hidden_layer_count = st.slider('Please select the number of hidden layers (2 is recommended)', 1, 10, 2)
    hidden_node_count = st.radio('Please choose how hidden layer nodes are formed', ['Use recommended', 'Enter size'])
    if hidden_node_count == 'Enter size':
        hidden = st.slider('Enter Node Size', min_value=input_nodes, max_value=(input_nodes + output_nodes) * 2)
    else:
        hidden = recommended_hidden
    st.write('Your hidden layers will have', hidden, 'nodes')
    val_percent = st.number_input('What percentage of the set should be used for Validation (Recommended 20%)', min_value=0, max_value=50, value=20)
    val_idx = range(int(len(df) * (1-(val_percent/100))), len(df))
    bs = st.slider('Please select batch size', 1, len(df.index),value=None)
    if df is not None and predict_var is not None and val_idx is not None and procs is not None and cat_names is not None and bs is not None:
        data = TabularDataBunch.from_df(path='output', df=df, dep_var=predict_var, valid_idx=val_idx, procs=[procs_dict[x] for x in procs], cat_names=cat_names, bs=bs)
        st.header('Please Verify the following')
        st.write('You are predicting for:')
        st.write(predict_var)
        st.write('Your categorical variables are', cat_names)
        st.write('Your continuous variables are', data.train_ds.cont_names)
        st.write('You will be Validating against', int(len(df) * (val_percent / 100)), 'entries')
        st.write('You will have', hidden_layer_count, 'hidden layers')
        st.write('Your Layers will have', hidden, 'nodes')
        step = 1
        layer_count = hidden_layer_count +2
        layers = []
        while step <= layer_count:
            if step == 1:
                layers = []
                layers.append(input_nodes)
                step += 1
            elif step == layer_count:
                layers.append(output_nodes)
                step += 1
            else:
                layers.append(hidden)
                step += 1
        st.subheader('Your model is constructed as follows')
        layers
        learn = tabular_learner(data, layers=layers, metrics=accuracy)
        epochs = st.slider('How many epochs would you like to run', 1, 150, value=None)
        if st.button('Train The Model'):
            learn.fit_one_cycle(epochs, 1e-2)
        interp = ClassificationInterpretation.from_learner(learn)
        interp.plot_confusion_matrix(output_nodes)