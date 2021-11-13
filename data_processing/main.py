from typing import Dict

import numpy as np
import pandas as pd
import pylab as py
from matplotlib import pyplot as plt
from pandas import DataFrame
from scipy import stats
from scipy.interpolate import LinearNDInterpolator

from .config import (BAR_GRAPH_SIZE, INTERPOLANT_TRANSPARENCY, MESHGRID_SCALE,
                     RUNAWAY, Z_SCORE)


class DataProcessor:
    def __init__(self, region_name: str, region_config: Dict) -> None:
        self.region_name = region_name
        self.region_config = region_config
        self.df = None

    def _drop_outliers(self) -> None:
        """Drop outliers from DataFrame"""
        self.df = self.df[
            (np.abs(stats.zscore(self.df['price_per_meter'])) < Z_SCORE)]

    def _drop_outborder_coords(self) -> None:
        """Drop coordinates lies outside the border"""
        bottom_border = self.region_config['bottom'] - RUNAWAY
        top_border = self.region_config['top'] + RUNAWAY
        left_border = self.region_config['left'] - RUNAWAY
        right_border = self.region_config['right'] + RUNAWAY
        self.df = self.df.loc[self.df['coord_lat'] >= bottom_border]
        self.df = self.df.loc[self.df['coord_lat'] <= top_border]
        self.df = self.df.loc[self.df['coord_lng'] >= left_border]
        self.df = self.df.loc[self.df['coord_lng'] <= right_border]

    def _data_preparation(self) -> None:
        """Preparation of raw data from scv-file to DataFrame"""
        self.df = self.df.drop_duplicates()
        self._drop_outliers()
        self._drop_outborder_coords()

    def _get_map_ratio(self) -> float:
        """Calculate a map ratio from map coordinates"""
        numerator = (self.region_config['right'] - self.region_config['left'])
        denominator = (
                self.region_config['top'] - self.region_config['bottom'])
        return numerator / denominator

    def draw(self) -> None:
        """Read and preparate raw data from csv file. Draw graphics"""
        self.df = pd.read_csv(f'data/{self.region_name}.csv')
        self._data_preparation()
        self._create_heat_map()
        self._create_graph_average_price()
        self._create_graph_average_square()

    def _get_data_border(self) -> tuple:
        """Get boundary values of coordinates"""
        d_right = self.df['coord_lng'].max()
        d_left = self.df['coord_lng'].min()
        d_top = self.df['coord_lat'].max()
        d_bottom = self.df['coord_lat'].min()
        return d_right, d_left, d_top, d_bottom

    def _calculate_interpolation(self) -> tuple:
        """"Find a interpolate function and return coordinates"""
        d_right, d_left, d_top, d_bottom = self._get_data_border()
        f = LinearNDInterpolator((self.df['coord_lng'], self.df['coord_lat']),
                                 self.df['price_per_meter'])
        xx, yy = np.meshgrid(
            np.linspace(d_left, d_right, MESHGRID_SCALE),
            np.linspace(d_bottom, d_top, MESHGRID_SCALE))
        zz = f(xx, yy)
        return xx, yy, zz

    def _create_heat_map(self):
        """
        Create and save heat map. Heat map built on creating and
        rendering an interpolation function LinearNDInterpolator.
        The interpolation result is plot on the map image.
        """
        img = plt.imread(f'maps/{self.region_name}.jpeg')
        xx, yy, zz = self._calculate_interpolation()
        fig, ax = plt.subplots()
        ax.pcolormesh(xx, yy, zz, cmap=py.cm.RdYlGn.reversed(),
                      shading='auto', alpha=INTERPOLANT_TRANSPARENCY)
        ax.imshow(img, extent=[self.region_config['left'],
                               self.region_config['right'],
                               self.region_config['bottom'],
                               self.region_config['top']])
        ax.set_aspect(self._get_map_ratio())
        plt.xlim([self.region_config['left'], self.region_config['right']])
        plt.ylim([self.region_config['bottom'], self.region_config['top']])
        plt.savefig(f'output/{self.region_name}_heatmap.png')
        plt.gcf().clear()

    def _group_df(self, meaning: str) -> DataFrame:
        """Group DataFrame by meaning"""
        return self.df.groupby('district_name').mean(meaning)

    def _create_graph_average_price(self) -> None:
        """
        Create and save a bar graph of the average price of real estate by area
        """
        grouped_df = self._group_df('price')
        grouped_df['price'].plot.barh(stacked=True, figsize=BAR_GRAPH_SIZE)
        plt.grid(axis='x')
        plt.title('Средняя стоимость недвижимости')
        plt.xlabel('Цена')
        plt.ylabel('Муниципальный округ')
        plt.savefig(f'output/{self.region_name}_graph_average_price.png')
        plt.gcf().clear()

    def _create_graph_average_square(self) -> None:
        """
        Create and save a bar graph of the average square of real estate by area
        """
        grouped_df = self._group_df('square')
        grouped_df['square'].plot.barh(stacked=True, figsize=BAR_GRAPH_SIZE)
        plt.grid(axis='x')
        plt.title('Средняя площадь недвижимости')
        plt.xlabel('Площадь')
        plt.ylabel('Муниципальный округ')
        plt.savefig(f'output/{self.region_name}_graph_average_square.png')
        plt.gcf().clear()
