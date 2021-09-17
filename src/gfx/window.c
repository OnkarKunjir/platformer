#define GLFW_INCLUDE_NONE

#include <GLFW/glfw3.h>
#include <glad/gl.h>

#include "utils/utils.h"
#include "window.h"

GLFWwindow *window = NULL;

/**
 * Error callback function for glfw.
 */
void error_callback(int error_code, const char *description) {
  log_message(ERROR, description);
}

void create_window(const char *title, int width, int height) {

  // allows creation of only one window at a time.
  if (window != NULL) {
    log_message(WARN, "Creation of multiple windows is not supported.");
    return;
  }

  glfwSetErrorCallback(error_callback);

  if (!glfwInit()) {
    log_message(ERROR, "Failed to initalize glfw");
  }

  glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
  if (!(window = glfwCreateWindow(width, height, title, NULL, NULL))) {
    glfwTerminate();
    log_message(ERROR, "Failed to create window");
  }

  glfwMakeContextCurrent(window);

  // vsyncn turned on.
  glfwSwapInterval(1);

  if (!gladLoadGL(glfwGetProcAddress)) {
    destroy_window(window);
    log_message(ERROR, "Failed to load openGL");
  }
  glad_glClear(GL_COLOR_BUFFER_BIT);
}

void update_window() {
  glfwSwapBuffers(window);
  glfwPollEvents();
  glad_glClear(GL_COLOR_BUFFER_BIT);
}

int window_should_close() { return glfwWindowShouldClose(window); }

void destroy_window() {
  glfwDestroyWindow(window);
  glfwTerminate();

  // reset value of window pointer if user decides to create new window again
  // for some reason.
  window = NULL;
}
