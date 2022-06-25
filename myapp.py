from bokeh.io import output_notebook, curdoc
from bokeh.plotting import figure, show
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import ColumnDataSource, GroupFilter, CDSView, HoverTool, Div
from bokeh.layouts import column, widgetbox
import pandas as pd
import numpy as np

#insert dataset saham hangseng
df_HS=pd.read_csv('Hang_Seng.csv')

#output dataset saham hangseng
df_HS

#Tambahkan kolom nama dan kolomnya diisikan "HANG SENG"
df_HS['Name'] = 'HANG SENG'

#output dataset saham hangseng
df_HS

#insert dataset saham Nasdag 
df_Nasdaq=pd.read_csv('Nasdaq.csv')

#outputkan dataset saham Nasdag
df_Nasdaq

#Tambahkan kolom nama dan kolomnya diisikan "NASDAQ"
df_Nasdaq['Name'] = 'NASDAQ'

#outputkan dataset saham Nasdag
df_Nasdaq

#insert dataset saham Nikkei 
df_Nikkei=pd.read_csv('Nikkei.csv')

#Outputkan dataset saham Nikkei
df_Nikkei

#Tambahkan kolom nama dan kolomnya diisikan "NIKKEI"
df_Nikkei['Name'] = 'NIKKEI'

#Outputkan dataset saham Nikkei
df_Nikkei

#Gabungkan dasaset saham HANGSENG, NASDAQ, dan NIKKEI
df_tubes_visdat = pd.concat([df_HS, df_Nasdaq, df_Nikkei])

#Outputkan dataset final saham 
df_tubes_visdat

#insert dataset saham tubes visdat 
df_tubes_visdat=pd.read_csv('df_tubes_visdat_0291_4319.csv',parse_dates=['Date'])

#Mengganti nama kolom dengan "Adj Close"  menjadi "AdjClose" lalu mengurutkan dataset saham finalnya berdasarkan date dari terlama terlebih dahulu menuju terbaru
df_tubes_visdat = df_tubes_visdat.rename(columns = {'Adj Close': 'AdjClose'}, inplace = False)
df_tubes_visdat.sort_values(by ='Date')

#menambahkan kolom dengan nama kolom "Day_Perc_Change" dan diisikan dengan menggunakan fungsi bawaan pct_change() dari library python
df_tubes_visdat['Day_Perc_Change'] = df_tubes_visdat['AdjClose'].pct_change()*100 

#menghapus kolom open karena tidak dibutuhkan
df_tubes_visdat.drop( 'Open', axis=1, inplace=True)

#menghapus kolom high karena tidak dibutuhkan
df_tubes_visdat.drop(  'High', axis=1, inplace=True)

#menghapus kolom low karena tidak dibutuhkan
df_tubes_visdat.drop( 'Low', axis=1, inplace=True)

#menghapus kolom close karena tidak dibutuhkan lagi(sudah dihitung Day_Perc_Change)
df_tubes_visdat.drop( 'Close',axis=1, inplace=True)

#mengoutputkan dataset final saham yang telah diupdate dengan proses sebelumnya
df_tubes_visdat.head()

#mengdeskripsikan dataset final saham 
df_tubes_visdat.describe

#menampilkan type data setiap kolom dalam dataset final saham
df_tubes_visdat.dtypes

#mencari nilai kosong dalam setiap kolom dalam dataset final saham dan mengoutputkannya 
missing_value=df_tubes_visdat.isnull().sum().sort_values(ascending = False)
print(missing_value)

#mengecek nilai yang sama dalam semua kolom dan mengoutputkannya 
cek_data_sama = df_tubes_visdat.duplicated()
print('Jumlah Data Sama = %d' % (cek_data_sama.sum()))
print('Total Data = %d' % (df_tubes_visdat.shape[0]))

output_notebook() # menampilkan output pada notebook
select_tools = ['pan', 'box_select', 'wheel_zoom', 'tap', 'reset']
#membuat gambar plot Adj Close dengan label Xnya dab label Ynya dengan nama berurutan adalah Date dan Adj Close
adjClose_fig = figure(x_axis_type='datetime',
           plot_height=700, plot_width=800,
           title='Data Adj Close',
           toolbar_location="below",
           tools=select_tools,
           x_axis_label='Date', y_axis_label='Adj Close')
#membuat gambar plot Volume dengan label Xnya dab label Ynya dengan nama berurutan adalah Date dan Volume
volume_fig = figure(x_axis_type='datetime',
           plot_height=700, plot_width=800,
           title='Data Volume',
           toolbar_location="below",
           tools=select_tools,
           x_axis_label='Date', y_axis_label='Volume')

#membuat gambar plot Day Percentage Change dengan label Xnya dab label Ynya dengan nama berurutan adalah Date dan Day Percentage Change
day_perc_change_fig = figure(x_axis_type='datetime',
           plot_height=700, plot_width=800,
           title='Data Day Percentage Change',
           toolbar_location="below",
           tools=select_tools,
           x_axis_label='Date', y_axis_label='Day Percentage Change')

# Mengubah dataset final saham ke dalam bentuk columdatasource
cds_dataset = ColumnDataSource(df_tubes_visdat)

#Melakukan proses filter dan View saham Hangseng, Nasdaq, dan Nikkei
hangseng_filter = [GroupFilter(column_name='Name', group='HANG SENG')]
hangseng_view = CDSView(source=cds_dataset,
                      filters=hangseng_filter)

nasdaq_filter = [GroupFilter(column_name='Name', group='NASDAQ')]
nasdaq_view = CDSView(source=cds_dataset,
                      filters=nasdaq_filter)

nikkei_filter = [GroupFilter(column_name='Name', group='NIKKEI')]
nikkei_view = CDSView(source=cds_dataset,
                      filters=nikkei_filter)
                      
#Mendefinisikan lingkaran atau circle yang akan dioutputkan
circle_kwargs = {
    'source': cds_dataset,
    'size': 4,
    'alpha': 0.7,
    'selection_color':'red',
    'nonselection_color':'lightgray',
    'nonselection_alpha': 0.3,
    'muted_alpha': 0.1
}

#Mendefinisikan output dari saham hangseng
hangseng_kwargs = {
    'view': hangseng_view,
    'color': 'pink',
    'legend': 'HANG SENG'
}

#Mendefinisikan output dari saham nasdaq
nasdaq_kwargs = {
    'view': nasdaq_view,
    'color': 'blue',
    'legend': 'NASDAQ'
}

#Mendefinisikan output dari saham nikkei
nikkei_kwargs = {
    'view': nikkei_view,
    'color': 'yellow',
    'legend': 'NIKKEI'
}
                      
#Menambahkan data saham hangseng, nasdaq, dan nikkei dengan bentuk circle ke figure adjClose
adjClose_fig.circle(x='Date', y='AdjClose', **circle_kwargs, **hangseng_kwargs)
adjClose_fig.circle(x='Date', y='AdjClose', **circle_kwargs, **nasdaq_kwargs)
adjClose_fig.circle(x='Date', y='AdjClose', **circle_kwargs, **nikkei_kwargs)

#Menambahkan data saham hangseng, nasdaq, dan nikkei dengan bentuk circle ke figure volume
volume_fig.circle(x='Date', y='Volume', **circle_kwargs, **hangseng_kwargs)
volume_fig.circle(x='Date', y='Volume', **circle_kwargs, **nasdaq_kwargs)
volume_fig.circle(x='Date', y='Volume', **circle_kwargs, **nikkei_kwargs)

#Menambahkan data saham hangseng, nasdaq, dan nikkei dengan bentuk circle ke figure day_perc_change
day_perc_change_fig.circle(x='Date', y='Day_Perc_Change', **circle_kwargs, **hangseng_kwargs)
day_perc_change_fig.circle(x='Date', y='Day_Perc_Change', **circle_kwargs, **nasdaq_kwargs)
                     
#Mendefinisikan tooltips
tooltips_adjClose = [
            ('Name','@Name'),
            ('Adj Close', '@AdjClose')
           ]

tooltips_volume = [
            ('Name','@Name'),
            ('Volume', '@Volume')
           ]

tooltips_day_perc_change = [
            ('Name','@Name'),
            ('Day Percentage Change', '@Day_Perc_Change')
           ]
#Mendefinisikan hover glyph
hover_glyph_adjClose = adjClose_fig.circle(x='Date', y='AdjClose', source=cds_dataset,
                         size=7, alpha=0,
                         hover_fill_color='red', hover_alpha=0.5)

hover_glyph_volume = volume_fig.circle(x='Date', y='Volume', source=cds_dataset,
                         size=7, alpha=0,
                         hover_fill_color='red', hover_alpha=0.5)

hover_glyph_day_perc_change = day_perc_change_fig.circle(x='Date', y='Day_Perc_Change', source=cds_dataset,
                         size=7, alpha=0,
                         hover_fill_color='red', hover_alpha=0.5)
#Mendefinisikan hover
adjClose_fig.add_tools(HoverTool(tooltips=tooltips_adjClose, renderers=[hover_glyph_adjClose]))

volume_fig.add_tools(HoverTool(tooltips=tooltips_volume, renderers=[hover_glyph_volume]))

day_perc_change_fig.add_tools(HoverTool(tooltips=tooltips_day_perc_change, renderers=[hover_glyph_day_perc_change]))
                      
#Mengoutputkan Figure pergerakan harga saham
html = """ <h2>Visualisasi Data Interaktif Pergerakan Harga Saham Hangseng, Nasdaq, dan Nikkei</h2>
<b><h2>2018 - 2020</h2>"""
sup_title = Div(text=html)

adjClose_fig.legend.click_policy = 'mute'
volume_fig.legend.click_policy = 'mute'
day_perc_change_fig.legend.click_policy = 'mute'

# Membuat panel
adjClose_panel = Panel(child=adjClose_fig, title='Adj Close Data')
volume_panel = Panel(child=volume_fig, title='Volume Data')
day_perc_change_panel = Panel(child=day_perc_change_fig, title='Day Percentage Change Data')

# Assign panel ke dalam tab
tabs = Tabs(tabs=[adjClose_panel, volume_panel, day_perc_change_panel])

# Menampilkan tab layout
show(column(sup_title,tabs))
