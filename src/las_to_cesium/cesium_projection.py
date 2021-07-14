import numpy as np

# https://github.com/CesiumGS/cesium/blob/1.83/Source/Core/Cartesian3.js#L884
# /**
#  * Returns a Cartesian3 position from longitude and latitude values given in radians.
#  *
#  * @param {Number} longitude The longitude, in radians
#  * @param {Number} latitude The latitude, in radians
#  * @param {Number} [height=0.0] The height, in meters, above the ellipsoid.
#  * @param {Ellipsoid} [ellipsoid=Ellipsoid.WGS84] The ellipsoid on which the position lies.
#  * @param {Cartesian3} [result] The object onto which to store the result.
#  * @returns {Cartesian3} The position
#  *
#  * @example
#  * var position = Cesium.Cartesian3.fromRadians(-2.007, 0.645);
#  */
# Cartesian3.fromRadians = function (
#   longitude,
#   latitude,
#   height,
#   ellipsoid,
#   result
# ) {
#   //>>includeStart('debug', pragmas.debug);
#   Check.typeOf.number("longitude", longitude);
#   Check.typeOf.number("latitude", latitude);
#   //>>includeEnd('debug');
#
#   height = defaultValue(height, 0.0);
#   var radiiSquared = defined(ellipsoid)
#     ? ellipsoid.radiiSquared
#     : wgs84RadiiSquared;
#
#   var cosLatitude = Math.cos(latitude);
#   scratchN.x = cosLatitude * Math.cos(longitude);
#   scratchN.y = cosLatitude * Math.sin(longitude);
#   scratchN.z = Math.sin(latitude);
#   scratchN = Cartesian3.normalize(scratchN, scratchN);
#
#   Cartesian3.multiplyComponents(radiiSquared, scratchN, scratchK);
#   var gamma = Math.sqrt(Cartesian3.dot(scratchN, scratchK));
#   scratchK = Cartesian3.divideByScalar(scratchK, gamma, scratchK);
#   scratchN = Cartesian3.multiplyByScalar(scratchN, height, scratchN);
#
#   if (!defined(result)) {
#     result = new Cartesian3();
#   }
#   return Cartesian3.add(scratchK, scratchN, result);
# };


class CesiumProjection:

    def __init__(self):

        self.wgs84RadiiSquared = np.array((6378137.0 * 6378137.0, 6378137.0 * 6378137.0, 6356752.3142451793 * 6356752.3142451793))
        self.wgs84inverse = 1. / self.wgs84RadiiSquared

    def cartesian_from_degrees(self, longitude, latitude, height=0):

        return self.cartesian_from_radians(np.radians(longitude),
                                           np.radians(latitude),
                                           height)

    def cartesian_from_radians(self, longitude, latitude, height=0):

          radiiSquared = self.wgs84RadiiSquared

          cosLatitude = np.cos(latitude)
          x = cosLatitude * np.cos(longitude)
          y = cosLatitude * np.sin(longitude)
          z = np.sin(latitude)
          vec3 = np.array([x, y, z])
          scratchN = vec3 / np.linalg.norm(vec3, axis=0)

          scratchK = (radiiSquared.T * scratchN.T).T
          gamma = np.sqrt(np.sum(scratchN * scratchK, axis=0))
          scratchK = scratchK / gamma
          scratchN = scratchN * height

          return scratchK + scratchN

    def orth_basis_at_cartographic(self, longitude, latitude):
        """
        Returns the basis as columns of a matrix (2d array)
        :param longitude:
        :param latitude:
        :return:
        """
        lon = np.radians(longitude)
        lat = np.radians(latitude)

        # surface normal in Cartesian
        n = np.array([
            np.cos(lat) * np.cos(lon),
            np.cos(lat) * np.sin(lon),
            np.sin(lat)
        ])
        n /= np.linalg.norm(n, axis=0)

        # Longitude tangent
        T = np.array([
            np.sin(lat) * np.cos(lon),
            np.sin(lat) * np.sin(lon),
            -np.cos(lat)
        ])
        T /= np.linalg.norm(T, axis=0)

        # Latitude tangent
        B = np.array([
            - np.sin(lon),
            np.cos(lat),
            0
        ])
        B /= np.linalg.norm(B, axis=0)

        M = np.zeros((3,3))
        M[:, 0] = n
        M[:, 1] = T
        M[:, 2] = B

        return M


if __name__ == '__main__':

    cp = CesiumProjection()

    # Computed by Cesium:
    result = np.array([
        (3177033.834174991, 5502784.018156439, 552187.4462574795),
        (3184958.5626323987, 278647.76803015644, 5500511.77495479)])

    print ('\nExpected result:\n', result)

    arr = cp.cartesian_from_degrees(
        np.array([60, 5]),
        np.array([5, 60]),
        np.array([40, 40])).T

    print('\nActual result:\n', arr)

    print('\nDifference:\n', arr - result)

    N = cp.orth_basis_at_cartographic(60, 5)
    print('\nThe basis\n', N)





