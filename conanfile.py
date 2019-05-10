# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import shutil
import os

class LibnameConan(ConanFile):
    name = "vcl"
    version = "20190502"
    commit_id = "7b73e9914fc15165bbc3d61e70fc0de804e440a7"
    description = "Visual Computing Library (VCL)"
    topics = ("Visual Computing")
    url = "https://github.com/bfierz/vcl"
    homepage = "https://github.com/bfierz/vcl"
    author = "Basil Fierz <basil.fierz@hotmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = { 
            "vectorization": ["AVX", "AVX 2", "SSE 4.2" ], 
            "fPIC": [True, False]
            }
    default_options = {
            "vectorization": "AVX",
            "fPIC": True
    }

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "abseil/20180600@bincrafters/stable",
        "eigen/3.3.7@conan/stable",
        "fmt/4.1.0@bincrafters/stable",
        "glew/2.1.0@bincrafters/stable"
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
        else:
            self.options["abseil"].fPIC = self.options.fPIC
            self.options["glew"].fPIC = self.options.fPIC

        # Support multi-package configuration
        #if self.settings.compiler == "Visual Studio":
        #    del self.settings.build_type
        #    del self.settings.compiler["Visual Studio"].runtime

    def source(self):
        
        self.run("git clone --recursive " + self.url + ".git " + self._source_subfolder)
        shutil.rmtree(self._source_subfolder + "/src/externals/json/test")

        #source_url = "https://github.com/bfierz/vcl"
        #tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.commit_id))
        #extracted_dir = self.name + "-" + self.commit_id
        #os.rename(extracted_dir, self._source_subfolder)
        
    def _configure_cmake(self):
        cmake = CMake(self)

        # Configure which parts to build
        cmake.definitions["VCL_BUILD_BENCHMARKS"] = False
        cmake.definitions["VCL_BUILD_TESTS"] = False
        cmake.definitions["VCL_BUILD_TOOLS"] = False
        cmake.definitions["VCL_BUILD_EXAMPLES"] = False
        # Support multi-package configuration
        #if not hasattr(self.settings, "build_type"):
        #    cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"
        # Required for compatibility atm
        cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"
        # Configure features
        cmake.definitions["VCL_VECTORIZE"] = str(self.options.vectorization)
        cmake.definitions["VCL_OPENGL_SUPPORT"] = True
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        # Configure external targets
        cmake.definitions["vcl_ext_absl"] = "CONAN_PKG::abseil"
        cmake.definitions["vcl_ext_eigen"] = "CONAN_PKG::eigen"
        cmake.definitions["vcl_ext_fmt"] = "CONAN_PKG::fmt"
        cmake.definitions["vcl_ext_glew"] = "CONAN_PKG::glew"

        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.configure(build_folder=self._build_subfolder)

        if not hasattr(self.settings, "build_type"):
            if cmake.is_multi_configuration:
                cmake.build(target="vcl_core",     args=["--config","Debug"])
                cmake.build(target="vcl_geometry", args=["--config","Debug"])
                cmake.build(target="vcl_graphics", args=["--config","Debug"])
                cmake.build(target="vcl_math",     args=["--config","Debug"])
                cmake.build(target="vcl_core",     args=["--config","Release"])
                cmake.build(target="vcl_geometry", args=["--config","Release"])
                cmake.build(target="vcl_graphics", args=["--config","Release"])
                cmake.build(target="vcl_math",     args=["--config","Release"])
            else:
                for config in ("Debug", "Release"):
                    self.output.info("Building %s" % config)
                    cmake.definitions["CMAKE_BUILD_TYPE"] = config
                    cmake.configure(build_folder=self._build_subfolder)
                    shutil.rmtree("CMakeFiles")
                    os.remove("CMakeCache.txt")
        else:
            cmake.build(target="vcl_core")
            cmake.build(target="vcl_geometry")
            cmake.build(target="vcl_graphics")
            cmake.build(target="vcl_math")

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        
        bin_folder = os.path.join(self._build_subfolder, "bin")
        lib_folder = os.path.join(self._build_subfolder, "lib")
        inc_folder = os.path.join(self._source_subfolder, "src/libs")
        self.copy("*.dll", dst="bin", src=bin_folder)
        self.copy("*.a", dst="lib", src=lib_folder)
        self.copy("*.lib", dst="lib", src=lib_folder)
        self.copy("*.h", dst="include", src=inc_folder)
        self.copy("*.inl", dst="include", src=inc_folder)
        self.copy("config.h", dst="include/vcl.core/vcl/config", src=os.path.join(self._build_subfolder, self._source_subfolder, "src/libs/vcl.core/vcl/config"))

    def package_info(self):
        self.cpp_info.includedirs = ['include/vcl.core', 'include/vcl.math', 'include/vcl.graphics', 'include/vcl.geometry']
        if self.settings.os == "Windows":
            if not hasattr(self.settings, "build_type"):
                self.cpp_info.debug.libs = ['vcl_core_d.lib', 'vcl_math_d.lib', 'vcl_geometry_d.lib', 'vcl_graphics_d.lib']
                self.cpp_info.release.libs = ['vcl_core.lib', 'vcl_math.lib', 'vcl_geometry.lib', 'vcl_graphics.lib']
            else:
                # Required for compatibility atm
                if self.settings.build_type == 'Debug':
                    self.cpp_info.libs = ['vcl_core_d.lib', 'vcl_math_d.lib', 'vcl_geometry_d.lib', 'vcl_graphics_d.lib']
                else:
                    self.cpp_info.libs = ['vcl_core.lib', 'vcl_math.lib', 'vcl_geometry.lib', 'vcl_graphics.lib']
        else:
            self.cpp_info.libs = ['libvcl_core.a', 'libvcl_math.a', 'libvcl_geometry.a', 'libvcl_graphics.a']
        self.cpp_info.libdirs = [ "lib" ]
