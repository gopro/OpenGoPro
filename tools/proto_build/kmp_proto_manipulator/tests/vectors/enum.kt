@pbandk.Export
internal sealed class EnumCOHNStatus(override val value: Int, override val name: String? = null) : pbandk.Message.Enum {
    override fun equals(other: kotlin.Any?): Boolean = other is com.gopro.open_gopro.operations.EnumCOHNStatus && other.value == value
    override fun hashCode(): Int = value.hashCode()
    override fun toString(): String = "EnumCOHNStatus.${name ?: "UNRECOGNIZED"}(value=$value)"
    internal object COHN_UNPROVISIONED : EnumCOHNStatus(0, "COHN_UNPROVISIONED")
    internal object COHN_PROVISIONED : EnumCOHNStatus(1, "COHN_PROVISIONED")
    internal class UNRECOGNIZED(value: Int) : EnumCOHNStatus(value)
    internal companion object : pbandk.Message.Enum.Companion<com.gopro.open_gopro.operations.EnumCOHNStatus> {
        internal val values: List<com.gopro.open_gopro.operations.EnumCOHNStatus> by lazy { listOf(COHN_UNPROVISIONED, COHN_PROVISIONED) }
        override fun fromValue(value: Int): com.gopro.open_gopro.operations.EnumCOHNStatus = values.firstOrNull { it.value == value } ?: UNRECOGNIZED(value)
        override fun fromName(name: String): com.gopro.open_gopro.operations.EnumCOHNStatus = values.firstOrNull { it.name == name } ?: throw IllegalArgumentException("No EnumCOHNStatus with name: $name")
    }
}