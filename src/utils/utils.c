#include "utils.h"
#include <stdio.h>
#include <stdlib.h>

void log_message(enum log_type type, const char *msg) {
  switch (type) {
  case DEBUG:
    fprintf(stdout, "[DEBUG]: %s\n", msg);
    break;

  case INFO:
    fprintf(stdout, "[INFO]: %s\n", msg);
    break;

  case WARN:
    fprintf(stdout, "[WARN]: %s\n", msg);
    break;

  case ERROR:
    fprintf(stderr, "[ERROR]: %s\n", msg);
    exit(EXIT_FAILURE);
    break;

  default:
    fprintf(stderr, "[ERROR]: Invalid log level\nMessage was %s\n", msg);
    break;
  }
}
