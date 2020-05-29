# app.py

from fastai.tabular import *
from plotly import express as px
from sys import exit
from typing import List, Union
import pandas as pd
import streamlit as st


def something(File):
    df = pd.read_csv(File)

    st.subheader('Please verify the contents of your file')
    df

    procs_dict = {
        'Categorify': Categorify,
        'FillMissing': FillMissing,
        'Normalize': Normalize
    }

    procs = st.multiselect('Preprocessing', [
        'Categorify', 'FillMissing', 'Normalize'
    ])

    predict_var = st.selectbox(
        'Please select your dependant variable (Prediction Target)', df.columns)

    input_nodes = len(df.columns)-1
    output_nodes = len(df[predict_var].unique())
    recommended_hidden = int(((2/3)*input_nodes)+output_nodes)
    df_options = df.loc[:, df.columns != predict_var]
    cat_names = st.multiselect(
        'Please select your categorical variables (Discrete Options)', df_options.columns)
    hidden_layer_count = st.slider(
        'Please select the number of hidden layers (2 is recommended)', 1, 10, 2)
    hidden_node_count = st.radio('Please choose how hidden layer nodes are formed',
                                 ['Use recommended', 'Enter size'])

    if hidden_node_count == 'Enter size':
        hidden = st.slider('Enter Node Size', min_value=input_nodes,
                           max_value=(input_nodes + output_nodes) * 2)
    else:
        hidden = recommended_hidden

    st.write('Your hidden layers will have', hidden, 'nodes')
    val_percent = st.number_input(
        'What percentage of the set should be used for Validation (Recommended 20%)', min_value=0, max_value=50, value=20)

    val_idx = range(int(len(df) * (1-(val_percent/100))), len(df))
    bs = st.slider('Please select batch size', 1, len(df.index), value=None)

    if all(v is not None for v in [bs, cat_names, df, predict_var, procs, val_idx]):
        data = TabularDataBunch.from_df(
            path='output', df=df, dep_var=predict_var, valid_idx=val_idx,
            procs=[procs_dict[x] for x in procs], cat_names=cat_names, bs=bs)

        st.header('Please Verify the following')
        st.write('You are predicting for:')
        st.write(predict_var)
        st.write('Your categorical variables are', cat_names)
        st.write('Your continuous variables are', data.train_ds.cont_names)
        st.write('You will be Validating against', int(
            len(df) * (val_percent / 100)), 'entries')
        st.write('You will have', hidden_layer_count, 'hidden layers')
        st.write('Your Layers will have', hidden, 'nodes')

        step: int = 1
        layer_count: int = hidden_layer_count + 2
        layers: List = []

        while step <= layer_count:
            if step == 1:
                layers = []
                layers.append(input_nodes)
            elif step == layer_count:
                layers.append(output_nodes)
            else:
                layers.append(hidden)

            step += 1

        st.subheader('Your model is constructed as follows')
        layers

        learn = tabular_learner(data, layers=layers, metrics=accuracy)
        epochs = st.slider(
            'How many epochs would you like to run', 1, 150, value=None)

        if st.button('Train The Model'):
            learn.fit_one_cycle(epochs, 1e-2)

        interp = ClassificationInterpretation.from_learner(learn)
        interp.plot_confusion_matrix(output_nodes)


def main() -> None:
    st.title("Test Neural Networks with Fast.AI")

    uploaded_file = st.file_uploader("Please upload a CSV that has had all "
                                     + "nulls removed or otherwise "
                                     + "properly filled.", type=['csv'])

    if uploaded_file is not None:
        something(uploaded_file)


if __name__ == "__main__":
    main()
