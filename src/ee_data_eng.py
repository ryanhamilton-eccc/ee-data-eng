import click

import geopandas as gpd
import pandas as pd

from pathlib import Path

"""
v0.1.0
- Add click command line interface
- Args, training_data, validation_data
- take both spatial file and combine them into one dataframe and save it to a file
- class_int 
"""


@click.command()
@click.argument('training_data', type=click.Path(exists=False))
@click.argument('validation_data', type=click.Path(exists=False))
@click.option('--label_col', default="class_name", help='Column that contains the class labels')
@click.option('--output', default="processed/combined.shp", help='Output file path')
def cli(training_data, validation_data, label_col, output):
    click.echo(f'Loading training data from {training_data}')
    gdf_train = gpd.read_file(training_data)
    gdf_train['split'] = 'train'
    click.echo(gdf_train.head())
    
    click.echo(f'Loading validation data from {validation_data}')
    gdf_val = gpd.read_file(validation_data)
    gdf_val['split'] = 'test'
    click.echo(gdf_val.head())
    
    click.echo('Combining training and validation data')
    gdf = pd.concat([gdf_train, gdf_val])

    # to create lookup table need key, value
    # key is the class_name
    # value is the class_int
    key = gdf[label_col].unique().tolist()
    value = list(range(1, len(key)+1))
    lookup = pd.DataFrame({'class_name': key, 'class_int': value})
    click.echo(lookup)
    gdf = gdf.merge(lookup, on='class_name')
    
    gdf = gdf[[label_col, 'class_int', 'split', 'geometry']]

    output = Path(output)
    if not output.parent.exists():
        output.parent.mkdir(exist_ok=True)
    
    gdf.to_file(output, driver='ESRI Shapefile')
