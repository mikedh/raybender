import numpy as np

from numpy import int64, float64
from numpy.typing import NDArray

# the compiled functions
from . import _raybender as rb


class EmbreeScene:
    """
    A simple wrapper for the `raybender.raw` functions to hold
    geometry which can have ray queries run against it.
    """

    def __init__(self):
        self._scene = rb.create_scene()

    def add_triangle_mesh(
        self, vertices: NDArray[float64], faces: NDArray[int64]
    ) -> int:
        """
        Add a mesh to the scene and return its geometry ID.

        Parameters
        -----------
        vertices : (n, 3)
          3D vertices of the triangular mesh.
        faces : (m, 3)
          Indexes of `vertices` that form triangles.

        Returns
        ----------
        geom_id
          The index in the scene for the geometry.
        """
        return rb.add_triangle_mesh(
            self._scene,
            np.asanyarray(vertices, dtype=float64),
            np.asanyarray(faces, dtype=int64),
        )

    def intersection(
        self, ray_origins: NDArray[float64], ray_directions: NDArray[float64]
    ):
        """ """
        geom_ids, barycentric = rb.ray_scene_intersection(
            self._scene, ray_origins, ray_directions
        )
        return geom_ids, barycentric

    def close(self):
        """
        Release the scene in a way that can be called repeatedly.
        """
        scene = getattr(self, "_scene", None)
        if scene is not None:
            rb.release_scene(scene)
            self._scene = None

    def __del__(self):
        self.close()
