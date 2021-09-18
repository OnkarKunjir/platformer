#include "shader.h"
#include "utils/utils.h"

#include <stdio.h>
#include <stdlib.h>

char *read_shader(const char *path);
GLuint compile_shader(const char *path, const char *src, GLenum shader_type);

GLuint create_shader(const char *vs_path, const char *fs_path) {
  char *vs_src, *fs_src;

  // read source code for shaders from file.
  if (!(vs_src = read_shader(vs_path))) {
    log_message(ERROR, "Failed to read vertex shader");
  }

  if (!(fs_src = read_shader(fs_path))) {
    free(vs_src);
    log_message(ERROR, "Failed to read fragment shader");
  }

  GLuint vs = compile_shader(vs_path, vs_src, GL_VERTEX_SHADER);
  GLuint fs = compile_shader(fs_path, fs_src, GL_FRAGMENT_SHADER);

  GLuint program = glad_glCreateProgram();
  glad_glAttachShader(program, vs);
  glad_glAttachShader(program, fs);
  glad_glLinkProgram(program);

  glad_glDeleteShader(vs);
  glad_glDeleteShader(fs);

  bind_shader(program);

  free(vs_src);
  free(fs_src);

  return program;
}

void bind_shader(GLuint shader) { glad_glUseProgram(shader); }

void destroy_shader(GLuint shader) { glad_glDeleteProgram(shader); }

char *read_shader(const char *path) {
  FILE *shader_file;

  if ((shader_file = fopen(path, "r")) == NULL) {
    return NULL;
  }

  fseek(shader_file, 0, SEEK_END);

  // get the file size.
  int size = ftell(shader_file);
  rewind(shader_file);

  char *shader_src = (char *)calloc(size + 1, sizeof(char));
  fread(shader_src, sizeof(char), size, shader_file);
  fclose(shader_file);

  return shader_src;
}

GLuint compile_shader(const char *path, const char *src, GLenum shader_type) {
  GLuint shader = glad_glCreateShader(shader_type);
  glad_glShaderSource(shader, 1, &src, NULL);
  glad_glCompileShader(shader);

  GLint status;
  glad_glGetShaderiv(shader, GL_COMPILE_STATUS, &status);
  if (status == GL_FALSE) {
    log_message(WARN, path);
    glad_glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &status);
    char gl_log[status + 1];
    glad_glGetShaderInfoLog(shader, status, NULL, gl_log);
    log_message(WARN, gl_log);
  }
  return shader;
}
