cmake_minimum_required(VERSION 3.8)
project(custom_map)

# Compiler flags (optional)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# ----------------------------------
# Install your files so ROS 2 can find them
# ----------------------------------
install(DIRECTORY
  launch
  urdf
  worlds
  DESTINATION share/${PROJECT_NAME}
)

# if you have meshes/models folder, include that too
# install(DIRECTORY
#   models
#   DESTINATION share/${PROJECT_NAME}
# )

ament_package()
