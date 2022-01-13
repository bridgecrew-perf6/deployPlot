# INGGRID RESMI BENITA (1301184107)
# SASKIA PUTRI ANANDA (1301184157)
# ANIS NOVITASARI (1301184424)

# import library yang dibutuhkan
import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, BasicTicker
from bokeh.models import Slider, Select, Column, Row, Range
from bokeh.transform import transform

# Filterisasi Dataset
# https://colab.research.google.com/drive/1tuNR5SXDRrgFHnKpEmN4wiNn5vZSMxBt?usp=sharing

# Membaca data (Dataset ini adalah dataset hasil preprocesing menggunakan bahasa pemrogram R)
df = pd.read_csv("matriks_date_hour.csv") 
df = df.set_index('hour')
df.columns.name = "date"

df_week = df.copy(deep=True)
df_week = df_week[["1", "2", "3", "4", "5", "6", "7"]]
df_week = pd.DataFrame(df_week.stack(), columns=["frequency"]).reset_index()
source = ColumnDataSource(df_week)

# Membuat mapper
colors = [
    "#f99696",
    "#ee8e9a",
    "#e1889e",
    "#d382a0",
    "#c47da1",
    "#b379a1",
    "#a375a0",
    "#92719c",
    "#816d98",
    "#706892",
    "#61648a",
    "#535f81",
    "#465a78",
    "#3a546e",
    "#314e63",
    "#2a4858"
]
mapper = LinearColorMapper(palette=colors, low=df_week.frequency.min(), high=df_week.frequency.max())

x_range = [str(x) for x in range(1, 8)]
y_range = [str(x) for x in range(0, 24)]

# Membuat figure
p = figure(
    width=720,
    height=400,
    title="Heatmap Transaksi Minggu ke-1",
    x_range=x_range,
    y_range=y_range,
    toolbar_location=None,
    tools="",
    x_axis_location="below",
    x_axis_label = "Tanggal",
    y_axis_label="Jam",
    name='plot'
)

# Membat heatmap
p.rect(
    x="date",
    y="hour",
    width=1,
    height=1,
    source=source,
    line_color=None,
    fill_color=transform('frequency', mapper)
)

# Membuat color bar
color_bar = ColorBar(
    color_mapper=mapper,
    ticker=BasicTicker(desired_num_ticks=16)
)
# memposisikan color bar di bawah plot
p.add_layout(color_bar, 'below')

# Mengambil nilai slider_week
def update_plot(attr, old, new):
    minggu_ke = slider_minggu.value 
    jenis = type_selector.value

    title = "Heatmap Transaksi Minggu ke-"+str(minggu_ke)

    dataset_file_name = "matriks_date_hour"

    if jenis != "(Semua)":
        dataset_file_name = dataset_file_name+"_"+jenis

    dataset_file_name = dataset_file_name + ".csv"
    
    # Membaca data (Dataset ini adalah dataset hasil preprocesing menggunakan bahasa pemrogram R)
    df = pd.read_csv(dataset_file_name)  
    df = df.set_index('hour')
    df.columns.name = "date"

    first_date = 1 + (minggu_ke-1)*7
    last_date = 7 + (minggu_ke-1)*7

    df_week = df.copy(deep=True)
    df_week = df_week[[str(x) for x in range(first_date, last_date+1)]]
    df_week = pd.DataFrame(df_week.stack(), columns=["frequency"]).reset_index()
    source = ColumnDataSource(df_week)

    x_range = [str(x) for x in range(first_date, last_date+1)]
    y_range = [str(x) for x in range(0, 24)]

    # Membuat figure
    p_new = figure(
        width=720,
        height=400,
        title=title,
        x_range=x_range,
        y_range=y_range,
        toolbar_location=None,
        tools="",
        x_axis_location="below",
        x_axis_label="Tanggal",
        y_axis_label="Jam",
        name='plot'
    )

    mapper = LinearColorMapper(palette=colors, low=df_week.frequency.min(), high=df_week.frequency.max())

    # Membat heatmap
    p_new.rect(
        x="date",
        y="hour",
        width=1,
        height=1,
        source=source,
        line_color=None,
        fill_color=transform('frequency', mapper)
    )

    # Membuat color bar
    color_bar = ColorBar(
        color_mapper=mapper,
        ticker=BasicTicker(desired_num_ticks=16)
    )
    # memposisikan color bar di bawah plot
    p_new.add_layout(color_bar, 'below')  

    # Menghapus current plot dari tampilan, kemudian menampilkan plot baru
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
    plotToRemove = curdoc().get_model_by_name('plot')
    listOfSubLayouts.remove(plotToRemove)
    listOfSubLayouts.append(p_new)

# Membuat slider week, ada 4 week yang dapat dipilih
slider_minggu = Slider(start=1, end=4, step=1, value=1, title="Minggu ke-")

# menambahkan on change listener. Jika nilai slider berubah, maka program menjalankan fungsi update_plot
slider_minggu.on_change('value', update_plot)  

# Membuat select untuk memilih tipe transaksi
types = ["(Semua)", "Negative", "Positive"]
type_selector = Select(
    options=types,
    value='(Semua)',
    title='Tipe Transaksi'
)
# menambahkan on change listener. Jika nilai select berubah, maka program menjalankan fungsi update_plot
type_selector.on_change('value', update_plot)  

# Membuat layout yang menampung slider, select dan heatmap
layout = Row(Column(slider_minggu, type_selector), p, name='mainLayout')  

# Menampilkan layout
curdoc().add_root(layout)  
