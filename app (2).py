
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv('volume_spike.csv', parse_dates=['Tanggal'])
    df = df.sort_values(['Kode', 'Tanggal'])
    return df

df = load_data()

# Dropdown kode saham
kode_list = sorted(df['Kode'].dropna().unique())
selected_kode = st.selectbox("Pilih Kode Saham", kode_list)

# Filter dan plot
df_saham = df[df['Kode'] == selected_kode]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_saham['Tanggal'],
    y=df_saham['Volume'],
    name='Volume',
    marker_color='lightblue',
    opacity=0.6
))

fig.add_trace(go.Scatter(
    x=df_saham['Tanggal'],
    y=df_saham['Volume_MA5'],
    name='MA 5 Hari',
    line=dict(color='orange', width=2)
))

spike_df = df_saham[df_saham['Spike'] == 'YES']
fig.add_trace(go.Scatter(
    x=spike_df['Tanggal'],
    y=spike_df['Volume'],
    mode='markers',
    name='Spike',
    marker=dict(color='red', size=8, symbol='circle')
))

fig.update_layout(
    title=f'Volume Saham {selected_kode}',
    xaxis_title='Tanggal',
    yaxis_title='Volume',
    height=500,
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)
