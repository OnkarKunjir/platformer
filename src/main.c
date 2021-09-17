#include "gfx/window.h"

int main() {

  create_window("Platformer", 500, 500);
  while (!window_should_close()) {
    update_window();
  }
  destroy_window();

  return 0;
}
