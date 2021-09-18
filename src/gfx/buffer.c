#include "buffer.h"

struct Buffer create_buffer(GLenum target, GLenum usage, GLsizeiptr size,
                            const GLvoid *data) {
  struct Buffer buffer = {0, target, usage};
  glad_glGenBuffers(1, &buffer.id);
  buffer_data(&buffer, size, data);
  return buffer;
}

void bind_buffer(const struct Buffer *buffer) {
  glad_glBindBuffer(buffer->target, buffer->id);
}

void buffer_data(const struct Buffer *buffer, GLsizeiptr size,
                 const GLvoid *data) {
  bind_buffer(buffer);
  glad_glBufferData(buffer->target, size, data, buffer->usage);
}

void destroy_buffer(const struct Buffer *buffer) {
  glad_glDeleteBuffers(1, &buffer->id);
}
