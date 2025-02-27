/* data_class_negative.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Thu Feb 27 23:20:21 UTC 2025 */


@pbandk.Export
internal data class NotReal(
    val id: com.gopro.open_gopro.operations.EnumPresetGroup? = null,
    val presetArray: List<com.gopro.open_gopro.operations.Preset> = emptyList(),
    val canAddPreset: Boolean? = null,
    val icon: com.gopro.open_gopro.operations.EnumPresetGroupIcon? = null,
    val modeArray: List<com.gopro.open_gopro.operations.EnumFlatMode> = emptyList(),
    override val unknownFields: Map<Int, pbandk.UnknownField> = emptyMap()
) : pbandk.Message {
    override operator fun plus(other: pbandk.Message?): com.gopro.open_gopro.operations.PresetGroup = protoMergeImpl(other)
    override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.PresetGroup> get() = Companion.descriptor
    override val protoSize: Int by lazy { super.protoSize }
    internal companion object : pbandk.Message.Companion<com.gopro.open_gopro.operations.PresetGroup> {
        internal val defaultInstance: com.gopro.open_gopro.operations.PresetGroup by lazy { com.gopro.open_gopro.operations.PresetGroup() }
        override fun decodeWith(u: pbandk.MessageDecoder): com.gopro.open_gopro.operations.PresetGroup = com.gopro.open_gopro.operations.PresetGroup.decodeWithImpl(u)

        override val descriptor: pbandk.MessageDescriptor<com.gopro.open_gopro.operations.PresetGroup> = pbandk.MessageDescriptor(
            fullName = "open_gopro.PresetGroup",
            messageClass = com.gopro.open_gopro.operations.PresetGroup::class,
            messageCompanion = this,
            fields = buildList(5) {
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "id",
                        number = 1,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = com.gopro.open_gopro.operations.EnumPresetGroup.Companion, hasPresence = true),
                        jsonName = "id",
                        value = com.gopro.open_gopro.operations.PresetGroup::id
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "preset_array",
                        number = 2,
                        type = pbandk.FieldDescriptor.Type.Repeated<com.gopro.open_gopro.operations.Preset>(valueType = pbandk.FieldDescriptor.Type.Message(messageCompanion = com.gopro.open_gopro.operations.Preset.Companion)),
                        jsonName = "presetArray",
                        value = com.gopro.open_gopro.operations.PresetGroup::presetArray
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "can_add_preset",
                        number = 3,
                        type = pbandk.FieldDescriptor.Type.Primitive.Bool(hasPresence = true),
                        jsonName = "canAddPreset",
                        value = com.gopro.open_gopro.operations.PresetGroup::canAddPreset
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "icon",
                        number = 4,
                        type = pbandk.FieldDescriptor.Type.Enum(enumCompanion = com.gopro.open_gopro.operations.EnumPresetGroupIcon.Companion, hasPresence = true),
                        jsonName = "icon",
                        value = com.gopro.open_gopro.operations.PresetGroup::icon
                    )
                )
                add(
                    pbandk.FieldDescriptor(
                        messageDescriptor = this@Companion::descriptor,
                        name = "mode_array",
                        number = 5,
                        type = pbandk.FieldDescriptor.Type.Repeated<com.gopro.open_gopro.operations.EnumFlatMode>(valueType = pbandk.FieldDescriptor.Type.Enum(enumCompanion = com.gopro.open_gopro.operations.EnumFlatMode.Companion)),
                        jsonName = "modeArray",
                        value = com.gopro.open_gopro.operations.PresetGroup::modeArray
                    )
                )
            }
        )
    }
}