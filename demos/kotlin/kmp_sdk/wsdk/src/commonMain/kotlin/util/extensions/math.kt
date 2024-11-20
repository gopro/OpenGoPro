package util.extensions

import kotlin.math.pow

internal fun Int.pow(i: Int): Int = this.toDouble().pow(i).toInt()