from conans import ConanFile, CMake, tools

# WIP - not tested on a project yet
# Personal blocker: Suitesparse for conan

class CeresConan(ConanFile):
    name = "ceres"
    version = "1.14.0"
    license = "New BSD"
    author = "Martin Zaenker"
    url = "https://github.com/ceres-solver/ceres-solver/"
    #url = "https://ceres-solver.googlesource.com/ceres-solver"
    description = "Conan wrapper for ceres: A large scale non-linear optimization library."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "build_tests": [True, False],
               "build_examples": [True, False]}
    default_options = {"shared": False,
                       "build_tests":False,
                       "build_examples":False}
    source_path = "ceres-solver"
    #exports = ["FindCeres.cmake"]
    generators = "cmake"
    build_policy = 'missing'

    def requirements(self):
        self.requires('eigen/3.3.7@conan/stable')

    def source(self):
        self.run('git clone --depth 1 --branch %s %s' % (self.version, self.url))

    def configure_cmake(self):
        cmake = CMake(self)
        #cmake_args = {'MINIGLOG': 'OFF'}
        cmake_args = {'MINIGLOG': 'ON',
                      'BUILD_SHARED_LIBS': self.options.shared,
                      'BUILD_EXAMPLES': self.options.build_examples,
                      'BUILD_TESTING': self.options.shared,
                      'SUITESPARSE': 'OFF',
                      'CXSPARSE': 'OFF',
                      'GFLAGS': 'OFF',
                      'EIGENSPARSE': 'ON',
                      'LAPACK': 'OFF',
                      'OPENMP': 'OFF',
                      'CUSTOM_BLAS': 'OFF',
                      }
        cmake.configure(source_dir='../%s' % self.source_path, build_dir='build', defs=cmake_args)

        return cmake

    def build(self):
        cmake = self.configure_cmake()
        #cmake.build(target='install')
        cmake.build()

        if self.options.build_tests:
            cmake.test()
        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = self._configure_cmake(package_folder=self.package_folder)
        cmake.install()
        # licenses
        self.copy("license*", dst="licenses", keep_path=True)
        #self.copy('FindCeres.cmake', '.', '.')

    def imports(self):
        self.copy("license*", dst="licenses", folder=True, ignore_case=True)

    def package_info(self):
        self.cpp_info.includedirs += ['include'] #, 'internal/ceres/miniglog/glog']
        self.cpp_info.libs = ["ceres"] # if self.settings.build_type != "Debug" else "ceres-debug"]
        self.cpp_info.libdirs = ['lib']

        #self.cpp_info.resdirs = ['res']
        #self.cpp_info.builddirs += ['lib/cmake/Ceres']

