import numpy as np
from numpy import float64, int64
from numpy.typing import ArrayLike, NDArray

# the compiled functions
from . import _raybender as rb


class EmbreeScene:
    """
    A simple wrapper for the raybender pybind11 functions to hold
    geometry which can have ray queries run against it.
    """

    def __init__(self):
        self._scene = rb.create_scene()

    def add_triangle_mesh(self, vertices: ArrayLike, faces: ArrayLike) -> int:
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
        self, origins: ArrayLike, vectors: ArrayLike
    ) -> tuple[NDArray[np.int64], NDArray[np.float64]]:
        """
        Run a ray-scene intersection query.

        Parameters
        -----------
        origins : (n, 3)
          The (n, 3) origin points of the rays
        vectors : (n, 3)
          The direction vectors of the rays

        Returns
        ----------
        geometry_id
          The index of the geometry that was hit.
        barycentric
          The barycentric coordinates for each hit.
        """
        # validate the inputs in Python
        origins = np.asanyarray(origins, dtype=float64)
        vectors = np.asanyarray(vectors, dtype=float64)

        if len(origins.shape) != 2 or origins.shape[1] != 3:
            raise ValueError("`origins` must be `(n, 3)`")
        if len(vectors.shape) != 2 or vectors.shape[1] != 3:
            raise ValueError("`vectors` must be `(n, 3)`")
        if vectors.shape != origins.shape:
            raise ValueError("`origins.shape` must match `vectors.shape`")

        geometry_ids, barycentric = rb.ray_scene_intersection(
            self._scene, origins, vectors
        )

        return geometry_ids, barycentric

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
