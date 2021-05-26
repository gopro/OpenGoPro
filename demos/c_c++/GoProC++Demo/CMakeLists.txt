cmake_minimum_required(VERSION 3.18.2)
set(PROJ_NAME tutorials)
project (${PROJ_NAME})

set(CMAKE_CXX_FLAGS "-std=c++11 -lcurl")
set(CMAKE_C_FLAGS "-lcurl")


#check if cJSON library is needed for the demo
if(DEFINED REQUIRES_CJSON)
    if(NOT EXISTS "${CMAKE_SOURCE_DIR}/inc/cJSON.h" OR NOT EXISTS "${CMAKE_SOURCE_DIR}/inc/cJSON.h")
        # set variable to indicate cJSON was cloned and needs to be copied before creating executable
        set(COPY_CJSON "1")
        include(ExternalProject)
        set(EXTERNAL_INSTALL_LOCATION ${CMAKE_BINARY_DIR})
        ExternalProject_Add(cJSON
                GIT_REPOSITORY https://github.com/DaveGamble/cJSON
                GIT_TAG 324a6ac9a9b285ff7a5a3e5b2071e3624b94f2db
                PREFIX cJSON-prefix
                SOURCE_DIR ${CMAKE_BINARY_DIR}/cJSON
                )
        add_custom_command(
                OUTPUT  ${CMAKE_BINARY_DIR}/cJSON-prefix/cJSON_copied.txt
                COMMAND cp ${CMAKE_BINARY_DIR}/cJSON/cJSON.h  ${CMAKE_BINARY_DIR}/../inc && cp ${CMAKE_BINARY_DIR}/cJSON/cJSON.c  ${CMAKE_BINARY_DIR}/../src
                COMMENT "Copying cJSON files"
                WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/cJSON
        )
        add_custom_target(copy_cJSON DEPENDS ${CMAKE_BINARY_DIR}/cJSON-prefix/cJSON_copied.txt)
    endif()
endif()

include_directories(COMMON_DIRECTORIES inc src)

# Create executable for set settings, change modes and presets
if(${DEMO} MATCHES "all" OR ${DEMO} MATCHES "ui_control_commands")
    if(DEFINED COPY_CJSON)
        set(UI_CONTROL_SOURCES ui_control_commands/ui_control.cpp )
        add_executable(ui_control_commands ${UI_CONTROL_SOURCES} ${COMMON_DIRECTORIES})
        add_dependencies(ui_control_commands cJSON_copied.txt cJSON copy_cJSON)
    endif()
endif()

# Create executable for preview stream
if(${DEMO} MATCHES "all" OR ${DEMO} MATCHES "stream_commands")
    set(PREVIEW_STREAM_SOURCES stream_commands/stream.c)
    add_executable(stream_commands ${PREVIEW_STREAM_SOURCES})
endif()

# Create executable for handling media files
if(${DEMO} MATCHES "all" OR ${DEMO} MATCHES "media_commands")
    if(DEFINED COPY_CJSON)
        set(MEDIA_SOURCES media_commands/media.cpp src/cJSON.c )
        add_executable(media_commands ${MEDIA_SOURCES} ${COMMON_DIRECTORIES})
        add_dependencies(media_commands copy_cJSON cJSON cJSON_copied.txt)
    endif()
endif()