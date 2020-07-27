import argparse

import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.layouts import column, row
from bokeh.models import Button
from bokeh.io import curdoc
import webbrowser

from statistics import add_stats_to_data


class AnomalyViewer():
    def __init__(self, data, export_path='export_anomalies.csv'):
        self.data = data
        self.export_path = export_path

        add_stats_to_data(self.data)

        self.create_source()
        self.create_embeding_plot()
        self.create_datatable()
        self.create_buttons()

    def create_embeding_plot(self):
        tooltips = [(column, '@' + column) for column in self.data.columns if column not in ['*embeding_x*', '*embeding_y*']]
        tools = 'pan,wheel_zoom,box_zoom,reset, box_select, tap'
        self.embeding_plot = figure(tooltips=tooltips, tools=tools)
        self.embeding_plot.circle('*embeding_x*', '*embeding_y*', source=self.source)

    def create_datatable(self):
        columns = [TableColumn(field=column, title=column) for column in self.data.columns if column not in ['url', '*embeding_x*', '*embeding_y*']]
        self.data_table = DataTable(source=self.source, columns=columns, editable=True)
        self.data_table.source.on_change('data', self.data_table_data_changed)

    def data_table_data_changed(self, attr, old, new):
        self.recalculate_embeding_button.disabled = False

    def create_buttons(self):
        self.show_selected_button = Button(label='Show selected', button_type='primary', disabled=True)
        self.recalculate_embeding_button = Button(label='Recalculate embeding', button_type='primary', disabled=True)
        self.export_data_button = Button(label='Export data', button_type='primary')

        self.show_selected_button.on_click(self.show_selected_button_clicked)
        self.recalculate_embeding_button.on_click(self.recalculate_embeding_button_clicked)
        self.export_data_button.on_click(self.export_data_button_clicked)

    def show_selected_button_clicked(self):
        selected = self.source.selected.indices
        if selected:
            first_selected = self.data.iloc[selected[0]]
            url = first_selected['url']
            webbrowser.open_new_tab(url)

    def recalculate_embeding_button_clicked(self):
        self.data = self.source.to_df().drop(['index', '*embeding_x*', '*embeding_y*', '*lof*'], axis=1)
        add_stats_to_data(self.data)

        self.source.data['*embeding_x*'] = self.data['*embeding_x*'].to_list()
        self.source.data['*embeding_y*'] = self.data['*embeding_y*'].to_list()
        self.source.data['*lof*'] = self.data['*lof*'].to_list()
        self.recalculate_embeding_button.disabled = True

    def export_data_button_clicked(self):
        self.source.to_df().drop(['index', '*embeding_x*', '*embeding_y*'], axis=1).to_csv(self.export_path, index=False)

    def create_source(self):
        self.source = ColumnDataSource(self.data)
        if 'url' in self.source.data:
            self.source.selected.on_change('indices', self.source_selection_changed)

    def source_selection_changed(self, attr, old, new):
        self.show_selected_button.disabled = len(self.source.selected.indices) == 0

    def get_model(self):
        return row(self.data_table, column(row(self.show_selected_button, self.recalculate_embeding_button, self.export_data_button), self.embeding_plot), sizing_mode='stretch_both')


def main(csv_path, export_path):
    data = pd.read_csv(csv_path)
    anomaly_viewer = AnomalyViewer(data, export_path)
    curdoc().add_root(anomaly_viewer.get_model())


parser = argparse.ArgumentParser(description='Anomaly Viewer helps you find anomalous data points in csv files.')
parser.add_argument('csv', type=str, help='Path to the input csv file.')
parser.add_argument('--export', default='export_anomalies.csv', type=str, help='Export path of the resulting anomaly table.')
args = parser.parse_args()

main(args.csv, args.export)
