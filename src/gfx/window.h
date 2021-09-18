/**
 * Function creates glfw window and initalizes openGL context.
 * NOTE: Call this function before calling any openGL functions.
 */
void create_window(const char *title, int width, int height);

/**
 * Swaps window buffer and polls events.
 */
void update_window();

int window_should_close();

/**
 * Destroyes created window and deallocates glfw resources
 */
void destroy_window();
