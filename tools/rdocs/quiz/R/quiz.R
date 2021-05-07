# quiz.R/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:42 AM

#' Create a multiple choice quiz
#'
#' Provide a question, answers, select the correct answer, and provide
#' information on incorrect answer
#'
#' @import htmlwidgets
#'
#' @export
quiz <- function(question, correct_answer, answer_info, answers) {

  # forward options using x
  x <- list(
    question = question,
    correct_answer = correct_answer,
    answer_info = answer_info,
    answers = answers
  )

  width <- NULL
  height <- NULL
  elementId <- NULL

  # create widget
  htmlwidgets::createWidget(
    name = "quiz",
    x,
    width = width,
    height = height,
    package = "quiz",
    elementId = elementId
  )
}

#' Shiny bindings for quiz
#'
#' Output and render functions for using quiz within Shiny
#' applications and interactive Rmd documents.
#'
#' @param outputId output variable to read from
#' @param width,height Must be a valid CSS unit (like \code{'100\%'},
#'   \code{'400px'}, \code{'auto'}) or a number, which will be coerced to a
#'   string and have \code{'px'} appended.
#' @param expr An expression that generates a quiz
#' @param env The environment in which to evaluate \code{expr}.
#' @param quoted Is \code{expr} a quoted expression (with \code{quote()})? This
#'   is useful if you want to save an expression in a variable.
#'
#' @name quiz-shiny
#'
#' @export
quizOutput <- function(outputId, width = "100%", height = "400px") {
  htmlwidgets::shinyWidgetOutput(outputId, "quiz", width, height, package = "quiz")
}

#' @rdname quiz-shiny
#' @export
renderQuiz <- function(expr, env = parent.frame(), quoted = FALSE) {
  if (!quoted) {
    expr <- substitute(expr)
  } # force quoted
  htmlwidgets::shinyRenderWidget(expr, quizOutput, env, quoted = TRUE)
}