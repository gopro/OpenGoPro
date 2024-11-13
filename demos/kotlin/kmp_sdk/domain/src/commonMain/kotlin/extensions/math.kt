package extensions

import kotlin.math.pow

fun Int.pow(i: Int): Int = this.toDouble().pow(i).toInt()