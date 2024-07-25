import os
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
            cmake_args = [
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + extdir,
                "-DPYTHON_EXECUTABLE=" + sys.executable,
            ]

            cfg = "Debug" if self.debug else "Release"
            build_args = ["--config", cfg]

            if platform.system() == "Windows":
                cmake_args += [
                    "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
                ]
                if sys.maxsize > 2**32:
                    cmake_args += ["-A", "x64"]
                build_args += ["--", "/m"]
            else:
                cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
                build_args += ["--", "-j2"]

            env = os.environ.copy()
            env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
                env.get("CXXFLAGS", ""), self.distribution.get_version()
            )
            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)
            print(["cmake", ext.sourcedir] + cmake_args)
            subprocess.check_call(
                ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env
            )
            subprocess.check_call(
                ["cmake", "--build", "."] + build_args, cwd=self.build_temp
            )


setup(
    ext_modules=[CMakeExtension("raybender._raybender")],
    cmdclass=dict(build_ext=CMakeBuild),
    packages=["raybender"],
)
