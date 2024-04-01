cmake_minimum_required(VERSION 3.12)
project(nes_emulator)


# Define a function to generate the binary
function(generate_binary SOURCE_FILE)

    # Create a directory
    file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin)

    # Generate the assembly file
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.s
        COMMAND cc65 -o ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.s ${CMAKE_CURRENT_SOURCE_DIR}/${SOURCE_FILE}
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${SOURCE_FILE}
    )

    # Generate the object file
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.o
        COMMAND ca65 -o ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.o ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.s
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.s
    )

    get_filename_component(FILE_NAME ${SOURCE_FILE} NAME_WE)

    # Generate the binary
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/bin/${FILE_NAME}.bin
        COMMAND ld65 -t sim6502 -o ${CMAKE_CURRENT_BINARY_DIR}/bin/${FILE_NAME}.bin ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.o sim6502.lib
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.o
    )

    # Create a custom target to build the binary
    add_custom_target(${SOURCE_FILE}_binary ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/bin/${FILE_NAME}.bin)

    # Create a custom target to run the binary
    add_custom_target(run_${SOURCE_FILE}
        COMMAND sim65 ${CMAKE_CURRENT_BINARY_DIR}/example.bin
        DEPENDS ${SOURCE_FILE}_binary
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    )

endfunction()

function(generate_raw_binary SOURCE_FILE)

    # Create a directory
    file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin)

    # Generate the assembly file
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.s
        COMMAND cc65 -o ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.s ${CMAKE_CURRENT_SOURCE_DIR}/${SOURCE_FILE}
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${SOURCE_FILE}
    )

    # Generate the object file
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.o
        COMMAND ca65 -o ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.o ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.s
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.s
    )


    # Copy the config file to the build directory
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/config
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/config ${CMAKE_CURRENT_BINARY_DIR}/config
    )

    get_filename_component(FILE_NAME ${SOURCE_FILE} NAME_WE)
    # Generate the binary
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/bin/${FILE_NAME}.bin
        COMMAND ld65 -C config -o ${CMAKE_CURRENT_BINARY_DIR}/bin/${FILE_NAME}.bin ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.o
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/${SOURCE_FILE}.o ${CMAKE_CURRENT_BINARY_DIR}/config
    )

    # Create a custom target to build the binary
    add_custom_target(${SOURCE_FILE}_binary ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/bin/${FILE_NAME}.bin)

    add_custom_target(clean_o_files ALL
        COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_CURRENT_BINARY_DIR}/*.o
        DEPENDS ${SOURCE_FILE}_binary
    )


endfunction()

#generate_binary(example.c)
generate_raw_binary(ex1.c)
