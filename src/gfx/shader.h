#pragma once

#include "gfx/buffer.h"

/**
 * Creates shader program.
 * @param vs_path Specify path to vertex shader.
 * @param fs_path Specify path to fragment shader.
 */
GLuint create_shader(const char *vs_path, const char *fs_path);

void bind_shader(GLuint shader);

void destroy_shader(GLuint shader);
