cmake_minimum_required(VERSION 3.5)
project(eegoSports
	LANGUAGES CXX
	VERSION 1.13.0)
include(Findliblsl.cmake)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
find_package(Qt5 REQUIRED COMPONENTS Widgets)
find_package(Boost 1.65 REQUIRED)

add_executable(${PROJECT_NAME} MACOSX_BUNDLE WIN32
	main.cpp
	mainwindow.cpp
	mainwindow.h
	mainwindow.ui
	reader.h
	reader.cpp
	eemagine/sdk/wrapper.cc
)
target_link_libraries(${PROJECT_NAME}
	PRIVATE
	Qt5::Widgets
	Boost::boost
	LSL::lsl
	$<$<BOOL:${UNIX}>:dl>
)
target_include_directories(${PROJECT_NAME} PRIVATE eemagine/sdk)
set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD 14)
# target_compile_features(${PROJECT_NAME} PRIVATE cxx_auto_type cxx_lambda_init_captures)

installLSLApp(${PROJECT_NAME})
#installLSLAuxFiles(${PROJECT_NAME}
#	${PROJECT_NAME}.cfg
#)
LSLGenerateCPackConfig()
