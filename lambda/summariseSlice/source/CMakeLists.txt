add_compile_options(-O3 -march=haswell)
# add_compile_options(-Ofast -march=native)
# Line above controlled by init.sh
cmake_minimum_required(VERSION 3.5)
set(CMAKE_CXX_STANDARD 11)
project(function LANGUAGES CXX)

find_package(aws-lambda-runtime)
find_package(AWSSDK COMPONENTS dynamodb s3)

add_executable(${PROJECT_NAME} "main.cpp")

target_link_libraries(${PROJECT_NAME} PRIVATE AWS::aws-lambda-runtime ${AWSSDK_LINK_LIBRARIES})

target_compile_options(${PROJECT_NAME} PRIVATE
    "-Wall"
    "-Wextra"
    "-Wconversion"
    "-Wshadow"
    "-Wno-sign-conversion")

target_compile_features(${PROJECT_NAME} PRIVATE "cxx_std_11")

aws_lambda_package_target(${PROJECT_NAME} NO_LIBC)
