import pandas as pd
import numpy as np

import os
import laspy

from pyproj import Proj
from tqdm.cli import tqdm

from las_to_cesium.cesium_projection import CesiumProjection
from las_to_cesium.kml_parser import KmlParser


def parse_files(folder):

    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(folder):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    flights = []
    print('Parsing...')
    for f in tqdm(listOfFiles):
        if f[-3:].lower() == 'kml':
            flights.append(KmlParser(f))

    frames = []
    for flight in flights:
        df = flight.track
        frames.append(df)

    return pd.concat(frames)


def make_les_using_utm(df):

    print('############################################')
    print()

    print('Creating empty file...')
    print()
    of = laspy.create(file_version="1.2")

    print('Header offset', of.header.offset)
    print('Header scale', of.header.scale)

    point_format = of.point_format
    print('Dimensions:')
    print('\t', list(point_format.dimension_names))

    print('############################################')
    print()

    of.header.offsets = (0, 0, 0)
    of.header.scales = (0.1, 0.1, 0.1)

    print(of.header.offset)
    print(of.header.scale)

    myProj = Proj(proj='utm', ellps='WGS84', zone=32, units='m')
    x, y = myProj(df.longitude.to_numpy(), df.latitude.to_numpy())
    df['x'] = x
    df['y'] = y
    df['z'] = df.altitude

    origin = np.array([
        0.5 * df.x.min() + 0.5 * df.x.max(),
        0.5 * df.y.min() + 0.5 * df.y.max(),
        0.5 * df.z.min() + 0.5 * df.z.max()
    ])

    print('Projected Location:\n\t', origin)

    x = df.x.values - origin[0]
    y = df.y.values - origin[1]
    z = df.z.values - origin[2]

    pos = np.array([x, y, z])

    of.x = pos[0, :]
    of.y = pos[1, :]
    of.z = pos[2, :]

    of.write('data.las')

    myProj = Proj(proj='utm', ellps='WGS84', zone=32, units='m')
    lon, lat = myProj(origin[0], origin[1], inverse=True)

    print('origin: ', lon, lat, origin[2])


def make_les_using_cesium(df):

    print('############################################')
    print()

    print('Creating empty file...')
    print()
    of = laspy.create(file_version="1.2")

    print('Header offset', of.header.offset)
    print('Header scale', of.header.scale)

    point_format = of.point_format
    print('Dimensions:')
    print('\t', list(point_format.dimension_names))

    print('############################################')
    print()

    of.header.offsets = (0,0,0)
    of.header.scales = (0.01,0.01,0.01)

    # print(of.header.offset)
    # print(of.header.scale)

    oLat = df.latitude.mean()
    oLon = df.longitude.mean()

    cesiumProj = CesiumProjection()
    pos = cesiumProj.cartesian_from_degrees(df.longitude.values, df.latitude.values, df.altitude.values)

    origin = cesiumProj.cartesian_from_degrees(oLon, oLat, 0)

    print(f'Geodetic origin:\t{oLon} lon, {oLat} lat, 0 alt')
    print('Cartesian Location:\n\t', origin)

    basis = cesiumProj.orth_basis_at_cartographic(oLon, oLat)

    # print('Basis\n', basis)

    IM = np.linalg.inv(basis)
    # print('Inverse\n', IM)

    # print('Original data:\n', pos)

    pos = np.matmul(IM, pos)
    # print('Rotated data:\n', pos)

    origin_rot = np.matmul(IM, origin.T)
    # print('Rotated origin\n\t', origin_rot)

    pos = (pos.T - origin_rot.T).T
    # print('Centred data:\n', pos)

    # Changing from X up to Z up coordinates
    rot = np.array([
        [0,  0, 1],
        [0, -1, 0],
        [1,  0, 0]
    ])
    pos = np.matmul(rot, pos)

    of.x = pos[0, :]
    of.y = pos[1, :]
    of.z = pos[2, :]

    of.write('data.las')


def make_les_using_cesium_subtract_first(df):

    print('############################################')
    print()

    print('Creating empty file...')
    print()
    of = laspy.create(file_version="1.2")

    print('Header offset', of.header.offset)
    print('Header scale', of.header.scale)

    point_format = of.point_format
    print('Dimensions:')
    print('\t', list(point_format.dimension_names))

    print('############################################')
    print()

    of.header.offsets = (0,0,0)
    of.header.scales = (0.01,0.01,0.01)

    print(of.header.offset)
    print(of.header.scale)

    oLat = df.latitude.mean()
    oLon = df.longitude.mean()

    # oLat = 0.5 * (df.latitude.min() + df.latitude.max())
    # oLon = 0.5 * (df.longitude.min() + df.longitude.max())

    cesiumProj = CesiumProjection()
    pos = cesiumProj.cartesian_from_degrees(df.longitude.values, df.latitude.values, df.altitude.values)

    origin = cesiumProj.cartesian_from_degrees(oLon, oLat, 0)

    print(f'Geodetic origin:\t{oLon} lon, {oLat} lat, 0 alt')
    print('Cartesian Location:\n\t', origin)

    basis = cesiumProj.orth_basis_at_cartographic(oLon, oLat)

    print('Basis\n', basis)

    IM = np.linalg.inv(basis)
    print('Inverse\n', IM)

    print('Original data:\n', pos)

    pos = (pos.T - origin.T).T
    print('Centred data:\n', pos)

    rot = np.array([
        [0,  0, 1],
        [0, -1, 0],
        [1,  0, 0]
    ])

    # Combine the base transformation with the axis rotation matrix
    IM = np.matmul(rot, IM)

    pos = np.matmul(IM, pos)
    print('Rotated data:\n', pos)

    of.x = pos[0, :]
    of.y = pos[1, :]
    of.z = pos[2, :]

    of.write('data.las')


def main():

    import sys

    if len(sys.argv) < 2:
        print('Using default folder location')
        folder = './data/single-flight'
    else:
        folder = sys.argv[1]

    df = parse_files(folder)
    make_les_using_cesium(df)


if __name__ == '__main__':

    main()
