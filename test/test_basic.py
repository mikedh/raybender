import trimesh

import raybender as rb


class TrimeshRayScene(rb.EmbreeScene):
    def __init__(self, scene: trimesh.Scene):
        super().__init__()

        self.add_trimesh(scene)

    def add_trimesh(self, scene):
        self._trimesh = scene.dump()
        self._geom_id = {}
        for i, mesh in enumerate(self._trimesh):
            if not isinstance(mesh, trimesh.Trimesh):
                continue
            self._geom_id[
                self.add_triangle_mesh(vertices=mesh.vertices, faces=mesh.faces)
            ] = i

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()


def test_basic():
    import raybender as rb

    # Create Embree environment.
    scene = rb.EmbreeScene()

    scene.close()


def generate_scene(s: float = 10.0, r: float = 1.0) -> trimesh.Scene:
    ball = trimesh.creation.uv_sphere(radius=1.0).unwrap()
    plane = trimesh.creation.box(bounds=[[-s, -s, -2 * r], [s, s, -r]]).unwrap()

    # ball.visual.material.image = checkerboard()

    scene = trimesh.Scene({"ball": ball, "plane": plane})
    scene.camera_transform = scene.camera.look_at(ball.bounds)
    scene.lights[0].radius = 0.5
    scene.lights[1].radius = 0.5

    return scene


def test_ball_trimesh():
    ts = generate_scene()

    ball = ts.geometry["ball"]

    v = ball.vertices
    vn = ball.vertex_normals
    v += vn * 1e-5

    with TrimeshRayScene(ts) as ray:
        geom, bary = ray.intersection(ray_origins=v, ray_directions=vn)
        hit = geom[:, 0] >= 0

        assert hit is not None


if __name__ == "__main__":
    test_ball_trimesh()
