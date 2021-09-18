#pragma once
#include <glad/gl.h>

// struct to store buffer data.
struct Buffer {
  GLuint id;     // id returned by the glGenBuffer.
  GLenum target; // target to bind buffer to.
  GLenum usage;  // usage patten of buffer.
};

/**
 * Function creates and binds opengl buffer.
 * @param target Specify target to which buffer should be bound. eg
 * GL_ARRAY_BUFFER.
 * @param usage Specify usage pattern of the buffer. eg GL_STATIC_DRAW.
 * @param size Specify the size of buffer in bytes.
 * @param data Specify the data to be copied into buffer.
 * @return struct Buffer.
 */
struct Buffer create_buffer(GLenum target, GLenum usage, GLsizeiptr size,
                            const GLvoid *data);

// Binds the buffer.
void bind_buffer(const struct Buffer *buffer);

/**
 * Transfer data to opengl buffer.
 * @param buffer Specify the buffer in which data to be transferd.
 * @param size Specify size of data to transfer in bytes.
 * @param data Specify data to transfer into the buffer.
 * NOTE: function binds the buffer.
 */
void buffer_data(const struct Buffer *buffer, GLsizeiptr size,
                 const GLvoid *data);

void destroy_buffer(const struct Buffer *buffer);
