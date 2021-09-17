#pragma once

enum log_type { DEBUG, INFO, WARN, ERROR };

void log_message(enum log_type type, const char *msg);
