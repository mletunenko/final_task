from typing import Dict

import numpy as np
import pandas as pd
import pylab as py
from matplotlib import pyplot as plt
from pandas import DataFrame
from scipy import stats
from scipy.interpolate import LinearNDInterpolator


def data_preparation(region_name: str, region_config: Dict) -> pd.DataFrame:
    df = pd.read_csv(f"data/{region_name}.csv")
    df = df.drop_duplicates()
    df = df[
        (np.abs(stats.zscore(df['price_per_meter'])) < 3)]

    bottom_border = region_config['bottom'] - 1
    top_border = (region_config['top']) + 1
    left_border = (region_config['left']) - 1
    right_border = (region_config['right']) + 1

    df = df.loc[df["coord_lat"] >= bottom_border]
    df = df.loc[df["coord_lat"] <= top_border]
    df = df.loc[df["coord_lng"] >= left_border]
    df = df.loc[df["coord_lng"] <= right_border]

    return df


def create_heat_map(df: DataFrame, region_name: str,
                    region_config: Dict) -> None:
    img_file = f"maps/{region_name}.jpeg"
    map_ratio = (region_config['right'] - region_config['left']) / \
                (region_config['top'] - region_config['bottom'])

    f = LinearNDInterpolator((df['coord_lng'], df['coord_lat']),
                             df['price_per_meter'])

    d_right = df['coord_lng'].max()
    d_left = df['coord_lng'].min()
    d_top = df['coord_lat'].max()
    d_bottom = df['coord_lat'].min()
    size = 4000
    xx, yy = np.meshgrid(np.linspace(d_left, d_right, size),
                         np.linspace(d_bottom, d_top, size))
    zz = f(xx, yy)

    img = plt.imread(img_file)
    fig, ax = plt.subplots()

    ax.pcolormesh(xx, yy, zz, cmap=py.cm.RdYlGn.reversed(), shading='auto',
                  alpha=0.5)
    ax.imshow(img, extent=[region_config['left'], region_config['right'],
                           region_config['bottom'], region_config['top']])

    ax.set_aspect(map_ratio)
    plt.xlim([region_config['left'], region_config['right']])
    plt.ylim([region_config['bottom'], region_config['top']])

    plt.savefig(f"output/{region_name}_heatmap.png")
    plt.gcf().clear()


def create_graph_average_price(df: DataFrame, region_name: str) -> None:
    df = df.groupby('district_name').mean('price')
    df['price'].plot.barh(stacked=True, figsize=(20, 30))
    plt.grid(axis='x')
    plt.title('Средняя стоимость недвижимости')
    plt.xlabel("Цена")
    plt.ylabel('Муниципальный округ')

    plt.savefig(f"output/{region_name}_graph_average_price.png")
    plt.gcf().clear()


def create_graph_average_square(df: DataFrame, region_name: str) -> None:
    df = df.groupby('district_name').mean('square')
    df['square'].plot.barh(stacked=True, figsize=(20, 30))
    plt.grid(axis='x')
    plt.title('Средняя площадь недвижимости')
    plt.xlabel("Площадь")
    plt.ylabel('Муниципальный округ')

    plt.savefig(f"output/{region_name}_graph_average_square.png")
    plt.gcf().clear()
