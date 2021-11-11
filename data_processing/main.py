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


def drop_dublicates(df: DataFrame) -> DataFrame:
    """Drop dublicates from DataFrame"""
    return df.drop_duplicates()


def drop_outliers(df: DataFrame) -> DataFrame:
    """Drop outliers from DataFrame"""
    return df[(np.abs(stats.zscore(df['price_per_meter'])) < Z_SCORE)]


def drop_outborder_coords(df: DataFrame, region_config: Dict) -> DataFrame:
    """Drop coordinates lies outside the border"""
    bottom_border = region_config['bottom'] - RUNAWAY
    top_border = region_config['top'] + RUNAWAY
    left_border = region_config['left'] - RUNAWAY
    right_border = region_config['right'] + RUNAWAY
    df = df.loc[df['coord_lat'] >= bottom_border]
    df = df.loc[df['coord_lat'] <= top_border]
    df = df.loc[df['coord_lng'] >= left_border]
    df = df.loc[df['coord_lng'] <= right_border]
    return df


def data_preparation(region_name: str, region_config: Dict) -> DataFrame:
    """Preparation of raw data from scv-file to DataFrame"""
    df = pd.read_csv(f'data/{region_name}.csv')
    df = drop_dublicates(df)
    df = drop_outliers(df)
    df = drop_outborder_coords(df, region_config)
    return df


def get_map_ratio(region_config: Dict) -> float:
    """Calculate a map ratio from map coodinates"""
    map_ratio = (region_config['right'] - region_config['left']) / \
                (region_config['top'] - region_config['bottom'])
    return map_ratio


def create_heat_map(df: DataFrame,
                    region_name: str,
                    region_config: Dict) -> None:
    """
    Create and save heat map. Heat map built on creating and
    rendering an interpolation function LinearNDInterpolator.
    The interpolation result is plot on the map image.
    """
    img = plt.imread(f'maps/{region_name}.jpeg')
    map_ratio = get_map_ratio(region_config)
    f = LinearNDInterpolator((df['coord_lng'], df['coord_lat']),
                             df['price_per_meter'])
    d_right = df['coord_lng'].max()
    d_left = df['coord_lng'].min()
    d_top = df['coord_lat'].max()
    d_bottom = df['coord_lat'].min()
    xx, yy = np.meshgrid(np.linspace(d_left, d_right, MESHGRID_SCALE),
                         np.linspace(d_bottom, d_top, MESHGRID_SCALE))
    zz = f(xx, yy)
    fig, ax = plt.subplots()
    ax.pcolormesh(xx, yy, zz, cmap=py.cm.RdYlGn.reversed(), shading='auto',
                  alpha=INTERPOLANT_TRANSPARENCY)
    ax.imshow(img, extent=[region_config['left'], region_config['right'],
                           region_config['bottom'], region_config['top']])
    ax.set_aspect(map_ratio)
    plt.xlim([region_config['left'], region_config['right']])
    plt.ylim([region_config['bottom'], region_config['top']])
    plt.savefig(f'output/{region_name}_heatmap.png')
    plt.gcf().clear()


def create_graph_average_price(df: DataFrame, region_name: str) -> None:
    """
    Create and save a bar graph of the average price of real estate by area
    """
    df = df.groupby('district_name').mean('price')
    df['price'].plot.barh(stacked=True, figsize=BAR_GRAPH_SIZE)
    plt.grid(axis='x')
    plt.title('Средняя стоимость недвижимости')
    plt.xlabel('Цена')
    plt.ylabel('Муниципальный округ')
    plt.savefig(f'output/{region_name}_graph_average_price.png')
    plt.gcf().clear()


def create_graph_average_square(df: DataFrame, region_name: str) -> None:
    """
    Create and save a bar graph of the average square of real estate by area
    """
    df = df.groupby('district_name').mean('square')
    df['square'].plot.barh(stacked=True, figsize=BAR_GRAPH_SIZE)
    plt.grid(axis='x')
    plt.title('Средняя площадь недвижимости')
    plt.xlabel('Площадь')
    plt.ylabel('Муниципальный округ')
    plt.savefig(f'output/{region_name}_graph_average_square.png')
    plt.gcf().clear()
