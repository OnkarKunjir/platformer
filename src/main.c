#include "gfx/buffer.h"
#include "gfx/window.h"

int main() {
  create_window("Platformer", 500, 500);

  float vertex[] = {
      -0.5f, 0.5f,  // 0
      0.5f,  0.5f,  // 1
      -0.5f, -0.5f, // 2
      0.5f,  -0.5f, // 3
  };
  unsigned int index[] = {0, 1, 2, 2, 1, 3};

  struct Buffer vertex_buffer =
      create_buffer(GL_ARRAY_BUFFER, GL_STATIC_DRAW, sizeof(vertex), vertex);
  glad_glEnableVertexAttribArray(0);
  glad_glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0);

  struct Buffer index_buffer = create_buffer(
      GL_ELEMENT_ARRAY_BUFFER, GL_STATIC_DRAW, sizeof(index), index);

  while (!window_should_close()) {
    glad_glDrawElements(GL_TRIANGLES, sizeof(index) / sizeof(int),
                        GL_UNSIGNED_INT, 0);
    update_window();
  }
  destroy_window();

  destroy_buffer(&vertex_buffer);
  destroy_buffer(&index_buffer);

  return 0;
}
