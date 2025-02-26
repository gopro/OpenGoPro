/* LogConfig.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.util

// TODO

internal enum class LogVerbosity {
  TRACE,
  DEBUG,
  INFO,
  WARNING,
  ERROR,
  CRITICAL
}

// Get this from a .yml, etc.
// TODO we need to figure out how to set per-tag log levels
internal object LogConfig {}
