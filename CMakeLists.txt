# ============================================================
# CMakeLists.txt — OpenCV + ONNXRuntime 基础联调测试工程
# 构建环境：Windows + MSVC (VS 2026) + OpenCV 4.12 + ONNXRuntime 1.25
# ============================================================

cmake_minimum_required(VERSION 3.10)
project(YoloDeployTest LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ============================================================
# 依赖一：OpenCV
# ============================================================
set(OpenCV_DIR "D:/Doubao/OpenCV_Release/opencv/build")
find_package(OpenCV QUIET)

if(NOT OpenCV_FOUND)
    message(STATUS "OpenCV 自动检测失败，手动配置库路径...")
    set(OpenCV_INCLUDE_DIRS
        "D:/Doubao/OpenCV_Release/opencv/build/include"
        "D:/Doubao/OpenCV_Release/opencv/build/include/opencv2"
    )
    set(OpenCV_LIB_DIR "D:/Doubao/OpenCV_Release/opencv/build/x64/vc16/lib")
    set(OpenCV_LIBS
        debug       "${OpenCV_LIB_DIR}/opencv_world4120d.lib"
        optimized   "${OpenCV_LIB_DIR}/opencv_world4120.lib"
    )
    set(OpenCV_VERSION "4.12.0")
    set(OpenCV_FOUND TRUE)
    message(STATUS "  OpenCV ${OpenCV_VERSION} 手动配置 OK")
endif()
message(STATUS "OpenCV 头文件: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "OpenCV 库路径: ${OpenCV_LIBS}")

# ============================================================
# 依赖二：ONNXRuntime
# ============================================================
set(ORT_BASE "D:/Doubao/onnxruntime_release/onnxruntime-win-x64-1.25.1/onnxruntime-win-x64-1.25.1")
message(STATUS "ONNXRuntime 基础路径: ${ORT_BASE}")

# ----- 头文件目录 -----
set(ORT_INCLUDE_DIR "${ORT_BASE}/include")
# ----- 库文件（绝对路径） -----
set(ORT_LIB "${ORT_BASE}/lib/onnxruntime.lib")
# ----- 运行时 DLL 路径（运行前需加入 PATH） -----
set(ORT_DLL_DIR "${ORT_BASE}/lib")

message(STATUS "ONNXRuntime 头文件: ${ORT_INCLUDE_DIR}")
message(STATUS "ONNXRuntime 库文件: ${ORT_LIB}")
message(STATUS "ONNXRuntime DLL 路径: ${ORT_DLL_DIR}")

# ============================================================
# 编译目标
# ============================================================
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${ORT_INCLUDE_DIR})

add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME}
    ${OpenCV_LIBS}
    ${ORT_LIB}
)

# ============================================================
# 运行说明
# ============================================================
#   ①  cmake -G "Visual Studio 18 2026" -A x64 -S . -B build
#   ②  cmake --build build --config Release
#   ③  运行前设置 DLL 路径（二选一）：
#       方案 A（临时）：
#         set PATH=D:/Doubao/OpenCV_Release/opencv/build/x64/vc16/bin;D:/Doubao/onnxruntime_release/onnxruntime-win-x64-1.25.1/onnxruntime-win-x64-1.25.1/lib;%PATH%
#         build\Release\YoloDeployTest.exe
#       方案 B（推荐）：将上述两个 bin/lib 路径添加到系统 PATH 环境变量，之后直接运行 exe
# ============================================================

