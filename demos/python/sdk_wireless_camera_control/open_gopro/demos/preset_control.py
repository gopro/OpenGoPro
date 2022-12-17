# preset_control.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Aug 30 17:53:34 UTC 2022

"""Entrypoint for taking a picture demo."""

from __future__ import annotations
import enum
import logging
import argparse
from typing import Optional, Union, Callable

from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.table import Table
from rich import box

from open_gopro import WirelessGoPro, GoProResp
from open_gopro import Params as GoProParams
from open_gopro.constants import GoProEnum, SettingId
from open_gopro.util import set_stream_logging_level, setup_logging, add_cli_args_and_parse

console = Console()  # rich consoler printer
gopro: Optional[WirelessGoPro] = None

######### BEGIN PRESET PARSER #########


class Setting:
    """Class representation of preset setting

    Data populated by parsing preset status response
    """

    def __init__(self, settingDict: dict):
        """Constructor

        Raises:
            RuntimeError: Error parsing Setting from response dict

        Args:
            settingDict (dict): dict representation of setting
        """
        self.id: Union[SettingId, int]
        self.value: Union[GoProEnum, int]
        self.is_caption: bool

        valueType: Optional[Callable] = None
        if (parsedId := settingDict.get("id")) is not None:
            if parsedId in [i.value for i in SettingId]:
                self.id = SettingId(parsedId)
                valueType = GoProResp._get_query_container(self.id)
            else:
                self.id = parsedId
        else:
            raise RuntimeError("Error parsing preset id for Setting")
        if (parsedValue := settingDict.get("value")) is not None:
            self.value = valueType(parsedValue) if valueType else parsedValue
        else:
            raise RuntimeError("Error parsing preset value for Setting")
        if (parsedis_caption := settingDict.get("is_caption")) is not None:
            self.is_caption = parsedis_caption
        else:
            raise RuntimeError("Error parsing preset is_caption for Setting")

    def to_table(self) -> Table:
        """Formats data into rich table

        Returns:
            Table: rich table representation of data
        """
        settingTable = Table("Setting", box=box.SQUARE)

        settingTable.add_row("id:", str(self.id))
        settingTable.add_row("value:", str(self.value))
        settingTable.add_row("is_caption:", str(self.is_caption))

        return settingTable


class Preset:
    """Class representation of preset

    Data populated by parsing preset status response
    """

    def __init__(self, presetDict: dict):
        """Constructor

        Raises:
            RuntimeError: Error parsing Setting from response dict

        Args:
            presetDict (dict): dict representation of preset
        """
        self.id: int
        self.user_defined: bool = False
        self.is_modified: bool = False
        self.mode: Optional[enum.Enum] = None
        self.title_id: Optional[enum.Enum] = None
        self.icon: Optional[enum.Enum] = None
        self.is_fixed: Optional[bool] = None
        self.setting_array: Optional[list[Setting]] = None

        if (parsedId := presetDict.get("id")) is not None:
            self.id = parsedId
        else:
            raise RuntimeError("Error parsing preset id for Preset")

        if (parsed_user_defined := presetDict.get("user_defined")) is not None:
            self.user_defined = parsed_user_defined
        else:
            raise RuntimeError("Error parsing user_defined for Preset")

        if (parsed_is_modified := presetDict.get("is_modified")) is not None:
            self.is_modified = parsed_is_modified
        else:
            raise RuntimeError("Error parsing is_modified for Preset")

        if (parsedMode := presetDict.get("mode")) is not None:
            self.mode = parsedMode
        if (parsed_title_id := presetDict.get("title_id")) is not None:
            self.title_id = parsed_title_id
        if (parsed_icon := presetDict.get("icon")) is not None:
            self.icon = parsed_icon
        if (parsed_is_fixed := presetDict.get("is_fixed")) is not None:
            self.is_fixed = parsed_is_fixed
        if (settingDictArray := presetDict.get("setting_array")) is not None:
            if isinstance(settingDictArray, list):
                self.setting_array = []
                for settingDict in settingDictArray:
                    self.setting_array.append(Setting(settingDict))

    def to_table(self, activePreset: Optional[int] = None) -> Table:
        """Formats data into rich table

        Args:
            activePreset (Union[GoProParams.Preset, int, None]): The currently active preset if known, used to highlight active preset in table

        Returns:
            Table: rich table representation of data
        """
        presetTable = Table("Preset", box=box.SQUARE)
        if (activePreset is not None) and activePreset == self.id:
            presetTable.add_column("ACTIVE")
            presetTable.box = box.HEAVY
        else:
            presetTable.add_column("")

        presetTable.add_row("id:", str(self.id))
        presetTable.add_row("user_defined:", str(self.user_defined))

        presetTable.add_row("is_modified:", str(self.is_modified))

        if self.mode is not None:
            presetTable.add_row("mode:", str(self.mode))
        if self.title_id is not None:
            presetTable.add_row("title_id:", str(self.title_id))
        if self.icon is not None:
            presetTable.add_row("icon:", str(self.icon))
        if self.is_fixed is not None:
            presetTable.add_row("is_fixed:", str(self.is_fixed))
        if self.setting_array is not None:
            settingTables: list[Table] = []
            for setting in self.setting_array:
                settingTables.append(setting.to_table())
            # Use horizontal grid layout for compactness
            setting_arrayGrid = Table.grid(expand=False)
            setting_arrayGrid.add_row(*settingTables)
            presetTable.add_row("Settings:", setting_arrayGrid)

        return presetTable


class PresetGroup:
    """Class representation of preset group

    Data populated by parsing preset status response
    """

    def __init__(self, presetGroupDict: dict):
        """Constructor

        Raises:
            RuntimeError: Error parsing Setting from response dict

        Args:
            presetGroupDict (dict): dict representation of preset group
        """
        self.id: Union[GoProParams.PresetGroup, int]
        self.presetArray: list[Preset] = []
        self.can_add_preset: Optional[bool] = None

        # Parse id
        if (parsedId := presetGroupDict.get("id")) is not None:
            self.id = parsedId
        else:
            raise RuntimeError("Error parsing id for PresetGroup")

        # Parse can_add_preset
        if (parsed_can_add_preset := presetGroupDict.get("can_add_preset")) is not None:
            self.can_add_preset = parsed_can_add_preset

        # Parse preset_array
        presetDictArray: Optional[list[dict]] = presetGroupDict.get("preset_array")
        if presetDictArray is not None:
            for preset in presetDictArray:
                self.presetArray.append(Preset(preset))
        else:
            raise RuntimeError("Error parsing presetArray for PresetGroup")

    def to_table(self, activePreset: Optional[int] = None) -> Table:
        """Formats data into rich table

        Args:
            activePreset (Optional[int]): The currently active preset if known, used to highlight active preset in table

        Returns:
            Table: rich table representation of data
        """
        presetGroupTable = Table("Preset Group", box=box.SQUARE)

        presetGroupTable.add_row("id:", str(self.id))

        if self.can_add_preset is not None:
            presetGroupTable.add_row("can_add_preset:", str(self.can_add_preset))

        # Horizontal layout is more compact but can cause present and setting attributes to be cut off
        for preset in self.presetArray:
            presetGroupTable.add_row("", preset.to_table(activePreset))

        return presetGroupTable

    def get_preset_by_id(self, presetId: int) -> Optional[Preset]:
        """helper function for fetching the preset with specified preset id

        Args:
            presetId (int): The preset id being searched for

        Returns:
            Optional[Preset]: The matching preset found
        """
        for preset in self.presetArray:
            if presetId == preset.id:
                return preset
        return None


class PresetCollection:
    """Class representation of preset collection

    Data populated by parsing preset status response
    """

    def __init__(self, presetCollectionDict: dict):
        """Constructor

        Raises:
            RuntimeError: Error parsing Setting from response dict

        Args:
            presetCollectionDict (dict): dict representation of preset collection
        """
        self.presetGroupArray: list[PresetGroup] = []

        # Parse presetGroupArray
        presetGroupDictArray = presetCollectionDict.get("preset_group_array")
        if isinstance(presetGroupDictArray, list):
            for presetGroupDict in presetGroupDictArray:
                self.presetGroupArray.append(PresetGroup(presetGroupDict))
        else:
            raise RuntimeError("Error parsing presetGroupArray for PresetCollection")

    #
    def to_table(self, activePreset: Optional[int] = None) -> Table:
        """Formats data into rich table

        Args:
            activePreset (Union[GoProParams.Preset, int, None]): The currently active preset if known, used to
                highlight active preset in table

        Returns:
            Table: rich table representation of data
        """
        presetCollectionTable = Table("Preset Collection", box=box.SQUARE)

        for presetGroup in self.presetGroupArray:
            presetCollectionTable.add_row(presetGroup.to_table(activePreset))

        return presetCollectionTable

    def get_preset_tuple(self, presetId: int) -> tuple[Optional[PresetGroup], Optional[Preset]]:
        """helper function for fetching the preset with specified preset id and its parent preset group

        Args:
            presetId (int): The preset id being searched for

        Returns:
            tuple[Optional[PresetGroup], Optional[Preset]]: The matching preset and preset group if found
        """
        for presetGroup in self.presetGroupArray:
            if preset := presetGroup.get_preset_by_id(presetId):
                return presetGroup, preset
        return None, None


######### END PRESET PARSER #########


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect to a GoPro camera's Wifi Access Point.")
    return add_cli_args_and_parse(parser)


class MenuMode(enum.Enum):
    """Enum to identify the current menu state"""

    MAIN = 0
    TOP_LEVEL_SETTINGS = 1
    COLLECTION = 2
    DEMO = 3


class CameraModel(enum.Enum):
    """Enum to identify the camera model"""

    HERO10 = 0
    HERO11 = 1
    HERO11_MINI = 2


def applySettingChange(setting: SettingId, value: GoProEnum) -> None:
    """Applies specified value to the specified setting

    Args:
        setting (SettingId): The setting to modify
        value (GoProEnum): The value to apply to the setting
    """
    if gopro is None:
        return

    if setting not in gopro.ble_setting:
        return

    gopro.ble_setting[setting].set(value)


def printCurrentPresetStatus() -> None:
    """Prints the current preset status"""
    if gopro is None:
        return

    presetCollection = PresetCollection(gopro.ble_command.get_preset_status().data)
    activePresetId = gopro.ble_status.active_preset.get_value().flatten
    console.print(presetCollection.to_table(activePresetId))


def presetDemo(cameraModel: CameraModel) -> None:
    """Demonstrates setting combinations which cause distinct preset collections

    Args:
        cameraModel (CameraModel): Model for the paired camera
    """
    if gopro is None:
        return

    console.print(
        "[green]This demo walks through all setting combinations that cause distinct preset combinations."
    )

    if cameraModel == CameraModel.HERO11_MINI:
        # Easy
        console.print("[blue bold]Preset Collection 1")
        console.print("[gray]UX Mode:[/gray] [purple]Easy")
        applySettingChange(SettingId.CAMERA_UX_MODE, GoProParams.CameraUxMode.EASY)
        printCurrentPresetStatus()
        Prompt.ask(prompt="[yellow]Press enter to continue to the next preset collection")

        # Pro
        console.print("[blue bold]Preset Collection 2")
        console.print("[gray]UX Mode:[/gray] [purple]Pro")
        applySettingChange(SettingId.CAMERA_UX_MODE, GoProParams.CameraUxMode.PRO)
        printCurrentPresetStatus()
        Prompt.ask(prompt="[yellow]Press enter to end demo")

    else:
        # Max Lens
        console.print("[blue bold]Preset Collection 1")
        console.print("[gray]Max Lens:[/gray] [purple]On")
        applySettingChange(SettingId.MAX_LENS_MOD, GoProParams.MaxLensMode.MAX_LENS)
        printCurrentPresetStatus()
        Prompt.ask(prompt="[yellow]Press enter to continue to the next preset collection")

        if cameraModel == CameraModel.HERO11:
            # Easy Highest Quality
            console.print("[blue bold]Preset Collection 2")
            console.print("[gray]Max Lens:[/gray] [purple]Off")
            console.print("[gray]UX Mode:[/gray] [purple]Easy")
            console.print("[gray]Easy Night Photo:[/gray] [purple]Off")
            console.print("[gray]System Video Mode:[/gray] [purple]Highest Quality")
            applySettingChange(SettingId.MAX_LENS_MOD, GoProParams.MaxLensMode.DEFAULT)
            applySettingChange(SettingId.CAMERA_UX_MODE, GoProParams.CameraUxMode.EASY)
            gopro.ble_command.load_preset_group(group=GoProParams.PresetGroup.PHOTO)
            applySettingChange(SettingId.PHOTO_EASY_MODE, GoProParams.PhotoEasyMode.OFF)
            gopro.ble_command.load_preset_group(group=GoProParams.PresetGroup.VIDEO)
            applySettingChange(SettingId.SYSTEM_VIDEO_MODE, GoProParams.SystemVideoMode.HIGHEST_QUALITY)
            printCurrentPresetStatus()
            Prompt.ask(prompt="[yellow]Press enter to continue to the next preset collection")

            # Easy Highest Quality Night Photo
            console.print("[blue bold]Preset Collection 3")
            console.print("[gray]Max Lens:[/gray] [purple]Off")
            console.print("[gray]UX Mode:[/gray] [purple]Easy")
            console.print("[gray]Easy Night Photo:[/gray] [purple]On")
            console.print("[gray]System Video Mode:[/gray] [purple]Highest Quality")
            gopro.ble_command.load_preset_group(group=GoProParams.PresetGroup.PHOTO)
            applySettingChange(SettingId.PHOTO_EASY_MODE, GoProParams.PhotoEasyMode.NIGHT_PHOTO)
            printCurrentPresetStatus()
            Prompt.ask(prompt="[yellow]Press enter to continue to the next preset collection")

            # Easy Extended Battery
            console.print("[blue bold]Preset Collection 4")
            console.print("[gray]Max Lens:[/gray] [purple]Off")
            console.print("[gray]UX Mode:[/gray] [purple]Easy")
            console.print("[gray]Easy Night Photo:[/gray] [purple]Off")
            console.print("[gray]System Video Mode:[/gray] [purple]Extended Battery")
            applySettingChange(SettingId.PHOTO_EASY_MODE, GoProParams.PhotoEasyMode.OFF)
            gopro.ble_command.load_preset_group(group=GoProParams.PresetGroup.VIDEO)
            applySettingChange(SettingId.SYSTEM_VIDEO_MODE, GoProParams.SystemVideoMode.EXTENDED_BATTERY)
            printCurrentPresetStatus()
            Prompt.ask(prompt="[yellow]Press enter to continue to the next preset collection")

            # Easy Extended Battery Night Photo
            console.print("[blue bold]Preset Collection 5")
            console.print("[gray]Max Lens:[/gray] [purple]Off")
            console.print("[gray]UX Mode:[/gray] [purple]Easy")
            console.print("[gray]Easy Night Photo:[/gray] [purple]On")

            console.print("[gray]System Video Mode:[/gray] [purple]Extended Battery")
            gopro.ble_command.load_preset_group(group=GoProParams.PresetGroup.PHOTO)
            applySettingChange(SettingId.PHOTO_EASY_MODE, GoProParams.PhotoEasyMode.NIGHT_PHOTO)
            printCurrentPresetStatus()
            Prompt.ask(prompt="[yellow]Press enter to continue to the next preset collection")

            # Pro Highest Quality
            console.print("[blue bold]Preset Collection 6")
            console.print("[gray]Max Lens:[/gray] [purple]Off")
            console.print("[gray]UX Mode:[/gray] [purple]Pro")
            console.print("[gray]System Video Mode:[/gray] [purple]Highest Quality")
            applySettingChange(SettingId.CAMERA_UX_MODE, GoProParams.CameraUxMode.PRO)
            gopro.ble_command.load_preset_group(group=GoProParams.PresetGroup.VIDEO)
            applySettingChange(SettingId.SYSTEM_VIDEO_MODE, GoProParams.SystemVideoMode.EXTENDED_BATTERY)
            printCurrentPresetStatus()
            Prompt.ask(prompt="[yellow]Press enter to continue to the next preset collection")

            # Pro Extended Battery
            console.print("[blue bold]Preset Collection 7")
            console.print("[gray]Max Lens:[/gray] [purple]Off")
            console.print("[gray]UX Mode:[/gray] [purple]Pro")
            console.print("[gray]System Video Mode:[/gray] [purple]Extended Battery")
            applySettingChange(SettingId.CAMERA_UX_MODE, GoProParams.CameraUxMode.PRO)
            gopro.ble_command.load_preset_group(group=GoProParams.PresetGroup.VIDEO)
            applySettingChange(SettingId.SYSTEM_VIDEO_MODE, GoProParams.SystemVideoMode.EXTENDED_BATTERY)
            printCurrentPresetStatus()
            Prompt.ask(prompt="[yellow]Press enter to end demo")
        else:
            # Max Performance
            console.print("[blue bold]Preset Collection 2")
            console.print("[gray]Max Lens:[/gray] [purple]Off")
            console.print("[gray]Video Performance Mode:[/gray] [purple]Max Performance")
            applySettingChange(SettingId.MAX_LENS_MOD, GoProParams.MaxLensMode.DEFAULT)
            applySettingChange(SettingId.VIDEO_PERFORMANCE_MODE, GoProParams.PerformanceMode.MAX_PERFORMANCE)
            printCurrentPresetStatus()
            Prompt.ask(prompt="[yellow]Press enter to continue to the next preset collection")

            # Extended Battery
            console.print("[blue bold]Preset Collection 3")
            console.print("[gray]Max Lens:[/gray] [purple]Off")
            console.print("[gray]Video Performance Mode:[/gray] [purple]Extended Battery")
            applySettingChange(SettingId.VIDEO_PERFORMANCE_MODE, GoProParams.PerformanceMode.EXTENDED_BATTERY)
            printCurrentPresetStatus()
            Prompt.ask(prompt="[yellow]Press enter to continue to the next preset collection")

            # Stationary
            console.print("[blue bold]Preset Collection 4")
            console.print("[gray]Max Lens:[/gray] [purple]Off")
            console.print("[gray]Video Performance Mode:[/gray] [purple]Stationary")
            applySettingChange(SettingId.VIDEO_PERFORMANCE_MODE, GoProParams.PerformanceMode.STATIONARY)
            printCurrentPresetStatus()
            Prompt.ask(prompt="[yellow]Press enter to end demo")


def main(args: argparse.Namespace) -> None:
    global gopro
    logger = setup_logging(__name__, args.log)

    # Constants
    topLevelSettings: list[SettingId]
    hero10_topLevelSettings: list[SettingId] = [SettingId.MAX_LENS_MOD, SettingId.VIDEO_PERFORMANCE_MODE]
    hero11_topLevelSettings: list[SettingId] = [
        SettingId.MAX_LENS_MOD,
        SettingId.SYSTEM_VIDEO_MODE,
        SettingId.CAMERA_UX_MODE,
        SettingId.PHOTO_EASY_MODE,
    ]
    hero11_mini_topLevelSettings: list[SettingId] = [SettingId.CAMERA_UX_MODE]

    # State
    collectionCacheInvalidated = True
    activeCacheInvalidated = True
    loopRunning = True
    menuMode: MenuMode = MenuMode.MAIN
    focusedPresetGroup: Optional[PresetGroup] = None
    focusedPreset: Optional[Preset] = None
    focusedSetting: Optional[Setting] = None
    focusedTopLevelSetting: Optional[SettingId] = None
    activePresetGroup: Optional[PresetGroup] = None
    activePreset: Optional[Preset] = None
    presetCollectionCache: Optional[PresetCollection] = None
    cameraModel: CameraModel = CameraModel.HERO10

    with WirelessGoPro(
        args.identifier,
        wifi_interface=args.wifi_interface,
        sudo_password=args.password,
        enable_wifi=False,
    ) as gopro:
        # Now we only want errors
        set_stream_logging_level(logging.ERROR)

        if (fwVersion := gopro.ble_command.get_hardware_info().data.get("firmware_version")) is not None:
            if fwVersion.split(".")[0] == "H21":
                cameraModel = CameraModel.HERO10
            elif fwVersion.split(".")[0] == "H22":
                if fwVersion.split(".")[1] == "01":
                    cameraModel = CameraModel.HERO11
                else:
                    cameraModel = CameraModel.HERO11_MINI

        if cameraModel == CameraModel.HERO10:
            console.print("Detected Hero 10")
            topLevelSettings = hero10_topLevelSettings
        elif cameraModel == CameraModel.HERO11:
            console.print("Detected Hero 11 camera")
            topLevelSettings = hero11_topLevelSettings
        elif cameraModel == CameraModel.HERO11_MINI:
            console.print("Detected Hero 11 Mini camera")
            topLevelSettings = hero11_mini_topLevelSettings
        else:
            console.print("Unsupported camera detected")
            return

        while loopRunning:
            # REFRESH INVALID CACHES
            if collectionCacheInvalidated:
                console.print("[yellow]Refreshing preset status cache")
                presetCollectionCache = PresetCollection(
                    gopro.ble_command.get_preset_status(register=[GoProParams.RegisterPreset.PRESET]).data
                )
                collectionCacheInvalidated = False

            if presetCollectionCache is None:
                logger.error("Unable to fetch or parse current preset status, ending demo")
                loopRunning = False
                continue

            if activeCacheInvalidated:
                console.print("[yellow]Refreshing active preset cache")
                activePresetId = gopro.ble_status.active_preset.get_value().flatten
                activePresetGroup, activePreset = presetCollectionCache.get_preset_tuple(activePresetId)
                activeCacheInvalidated = False

            # MAIN MENU
            if menuMode == MenuMode.MAIN:
                console.print("[bold blue]Main Menu")
                menu = Table.grid(expand=False)
                menu.add_column(justify="right", width=4)
                menu.add_column()
                menu.add_column()
                menu.add_row("0", " ) ", "Print current preset status")
                menu.add_row("1", " ) ", "Modify top level settings")
                menu.add_row("2", " ) ", "Modify preset collection settings")
                menu.add_row("3", " ) ", "Run Preset Availability Demo")
                menu.add_row("4", " ) ", "Exit")
                console.print(menu)
                option = IntPrompt.ask(
                    prompt="Select an option from the menu above",
                    choices=[str(i) for i in range(0, 5)],
                    show_choices=False,
                )
                if option == 0:
                    if activePreset is not None:
                        console.print(presetCollectionCache.to_table(activePreset.id))
                    else:
                        console.print(presetCollectionCache.to_table())
                elif option == 1:
                    menuMode = MenuMode.TOP_LEVEL_SETTINGS
                    focusedTopLevelSetting = None
                elif option == 2:
                    menuMode = MenuMode.COLLECTION
                    focusedPresetGroup = None
                    focusedPreset = None
                    focusedSetting = None
                elif option == 3:
                    menuMode = MenuMode.DEMO
                else:
                    loopRunning = False

            # TOP LEVEL SETTING MENU
            elif menuMode == MenuMode.TOP_LEVEL_SETTINGS:
                if focusedTopLevelSetting is None:
                    menu = Table.grid(expand=False)
                    menu.add_column(justify="right", width=4)
                    menu.add_column()
                    menu.add_column()
                    menu.add_row("0", " ) ", "Back to Main Menu")
                    option_offset = 1
                    for i, settingId in enumerate(topLevelSettings):
                        if settingId not in gopro.ble_setting:
                            menu.add_row(
                                str(i + option_offset),
                                " ) ",
                                "(Inaccessible) Setting " + str(settingId),
                            )
                        else:
                            menu.add_row(str(i + option_offset), " ) ", "Modify setting " + str(settingId))

                    console.print("[bold blue]Top Level Setting Menu")
                    console.print(menu)
                    option = IntPrompt.ask(
                        prompt="Select an option from the menu above",
                        choices=[str(i) for i in range(len(topLevelSettings) + option_offset)],
                        show_choices=False,
                    )
                    if option == 0:
                        menuMode = MenuMode.MAIN
                    if topLevelSettings[option - option_offset] not in gopro.ble_setting:
                        console.print("[red]Invalid selection")
                    else:
                        focusedTopLevelSetting = topLevelSettings[option - option_offset]
                else:
                    menu = Table.grid(expand=False)
                    menu.add_column(justify="right", width=4)
                    menu.add_column()
                    menu.add_column()
                    menu.add_row("0", " ) ", "Back to Top Level Settings Menu")
                    option_offset = 1

                    try:
                        settingHandler = gopro.ble_setting[focusedTopLevelSetting]

                        logger.debug(f"Fetching value for setting {str(focusedTopLevelSetting)}")
                        response = settingHandler.get_value()
                        logger.debug(response)

                        currentValue = response.data.get(focusedTopLevelSetting)

                        logger.debug(f"Fetching capabilities for setting {str(focusedTopLevelSetting)}")
                        response = settingHandler.get_capabilities_values()
                        logger.debug(response)

                        settingValues = response.data.get(focusedTopLevelSetting)
                        if settingValues is None:
                            console.print(
                                f"No reported capabilities, cannot edit setting {str(focusedTopLevelSetting)}"
                            )
                            focusedTopLevelSetting = None
                        else:
                            for i, value in enumerate(settingValues):
                                if value == currentValue:
                                    menu.add_row(
                                        str(i + option_offset),
                                        " ) ",
                                        "Capability " + str(value) + " [green](CURRENT)",
                                    )
                                else:
                                    menu.add_row(str(i + option_offset), " ) ", "Capability " + str(value))

                            console.print(f"[bold blue]Setting Menu: ({str(focusedTopLevelSetting)})")
                            console.print(menu)
                            option = IntPrompt.ask(
                                prompt="Select an option from the menu above",
                                choices=[str(i) for i in range(len(settingValues) + option_offset)],
                                show_choices=False,
                            )
                            if option == 0:
                                focusedTopLevelSetting = None
                            else:
                                console.print(
                                    f"Changing setting {str(focusedTopLevelSetting)} value to {str(settingValues[option - option_offset])}"
                                )
                                logger.debug(
                                    f"Changing setting {str(focusedTopLevelSetting)} to {str(settingValues[option - option_offset])}"
                                )
                                response = settingHandler.set(settingValues[option - option_offset])
                                logger.debug(response)
                                collectionCacheInvalidated = True
                                activeCacheInvalidated = True
                    except KeyError:
                        console.print(
                            f"Unable to edit setting, no setting handler found for {str(focusedTopLevelSetting)}"
                        )
                        focusedTopLevelSetting = None
            # COLLECTION MENU
            elif menuMode == MenuMode.COLLECTION:
                if focusedPresetGroup is None:
                    menu = Table.grid(expand=False)
                    menu.add_column(justify="right", width=4)
                    menu.add_column()
                    menu.add_column()
                    menu.add_column()
                    menu.add_row("0", " ) ", "Back to Main Menu")
                    option_offset = 1
                    if isinstance(presetCollectionCache.presetGroupArray, list):
                        for i, group in enumerate(presetCollectionCache.presetGroupArray):
                            if group == activePresetGroup:
                                menu.add_row(
                                    str(i + option_offset),
                                    " ) ",
                                    "Preset Group " + str(group.id) + " [green](ACTIVE)",
                                )
                            else:
                                menu.add_row(
                                    str(i + option_offset),
                                    " ) ",
                                    "Preset Group " + str(group.id),
                                )

                        console.print("[bold blue]Preset Collection Menu")
                        console.print(menu)
                        option = IntPrompt.ask(
                            prompt="Select an option from the menu above",
                            choices=[
                                str(i)
                                for i in range(len(presetCollectionCache.presetGroupArray) + option_offset)
                            ],
                            show_choices=False,
                        )
                        if option == 0:
                            menuMode = MenuMode.MAIN
                        else:
                            focusedPresetGroup = presetCollectionCache.presetGroupArray[option - option_offset]

                elif focusedPreset is None:
                    menu = Table.grid(expand=False)
                    menu.add_column(justify="right", width=4)
                    menu.add_column()
                    menu.add_column()
                    menu.add_column()
                    menu.add_row("0", " ) ", "Back to Preset Collection Menu")
                    option_offset = 1
                    if isinstance(focusedPresetGroup.presetArray, list):
                        for i, preset in enumerate(focusedPresetGroup.presetArray):
                            if preset.title_id is None:
                                if preset == activePreset:
                                    menu.add_row(
                                        str(i + option_offset),
                                        " ) ",
                                        "Preset " + str(preset.id) + " [green](ACTIVE)",
                                    )
                                else:
                                    menu.add_row(
                                        str(i + option_offset),
                                        " ) ",
                                        "Preset " + str(preset.id),
                                    )
                            else:
                                if preset == activePreset:
                                    menu.add_row(
                                        str(i + option_offset),
                                        " ) ",
                                        "Preset " + str(preset.title_id) + " [green](ACTIVE)",
                                    )
                                else:
                                    menu.add_row(
                                        str(i + option_offset),
                                        " ) ",
                                        "Preset " + str(preset.title_id),
                                    )

                        console.print(f"[bold blue]Preset Group Menu: ({str(focusedPresetGroup.id)})")

                        console.print(menu)
                        option = IntPrompt.ask(
                            prompt="Select an option from the menu above",
                            choices=[
                                str(i) for i in range(len(focusedPresetGroup.presetArray) + option_offset)
                            ],
                            show_choices=False,
                        )
                        if option == 0:
                            focusedPresetGroup = None
                        elif (
                            focusedPresetGroup.presetArray[option - option_offset].setting_array is None
                        ) or (focusedPresetGroup.presetArray[option - option_offset].title_id is None):
                            console.print("[red]Invalid selection")
                        else:
                            focusedPreset = focusedPresetGroup.presetArray[option - option_offset]

                elif focusedSetting is None:
                    menu = Table.grid(expand=False)
                    menu.add_column(justify="right", width=4)
                    menu.add_column()
                    menu.add_column()
                    menu.add_row("0", " ) ", "Back to Preset Group Menu")
                    option_offset = 1

                    if focusedPreset != activePreset:
                        menu.add_row("1", " ) ", "Load this preset")
                        option_offset += 1
                    else:
                        if isinstance(focusedPreset.setting_array, list):
                            for i, setting in enumerate(focusedPreset.setting_array):
                                if setting.id in gopro.ble_setting:
                                    menu.add_row(
                                        str(i + option_offset),
                                        " ) ",
                                        "Setting " + str(setting.id),
                                    )
                                else:
                                    menu.add_row(
                                        str(i + option_offset),
                                        " ) ",
                                        "Setting " + str(setting.id) + " [red](NO API SUPPORT)",
                                    )

                    if focusedPreset == activePreset:
                        console.print(
                            f"[bold blue]Preset Menu: ({str(focusedPreset.title_id)})[/bold blue] [green](ACTIVE)"
                        )
                    else:
                        console.print(f"[bold blue]Preset Menu: ({str(focusedPreset.title_id)})")
                    console.print(menu)
                    optionCount = option_offset
                    if focusedPreset.setting_array is not None:
                        optionCount += len(focusedPreset.setting_array)
                    option = IntPrompt.ask(
                        prompt="Select an option from the menu above",
                        choices=[str(i) for i in range(optionCount)],
                        show_choices=False,
                    )
                    if option == 0:
                        focusedPreset = None
                    elif option == 1 and (focusedPreset != activePreset):
                        if focusedPreset.title_id is None:
                            console.print(f"[purple]Loading preset {str(focusedPreset.id)}")
                        else:
                            console.print(f"[purple]Loading preset {str(focusedPreset.title_id)}")
                        gopro.ble_command.load_preset(preset=focusedPreset.id)
                        activeCacheInvalidated = True
                    elif isinstance(focusedPreset.setting_array, list):
                        if focusedPreset.setting_array[option - option_offset].id not in gopro.ble_setting:
                            console.print("[red]Invalid selection")
                        else:
                            focusedSetting = focusedPreset.setting_array[option - option_offset]

                else:
                    menu = Table.grid(expand=False)

                    menu.add_column(justify="right", width=4)
                    menu.add_column()
                    menu.add_column()
                    menu.add_row("0", " ) ", "Back to Preset Menu")
                    option_offset = 1

                    try:
                        if not isinstance(focusedSetting.id, SettingId):
                            raise KeyError

                        settingHandler = gopro.ble_setting[focusedSetting.id]
                    except KeyError:
                        console.print(
                            f"Unable to edit setting, no setting handler found for {str(focusedSetting.id)}"
                        )
                        focusedSetting = None
                        return

                    logger.debug("Fetching capabilities for setting " + str(focusedSetting.id))
                    response = settingHandler.get_capabilities_values()
                    logger.debug(response)

                    settingValues = response.data.get(focusedSetting.id)

                    if not isinstance(settingValues, list):
                        console.print(
                            f"Failed to retrieve capabilities, cannot edit setting {str(focusedSetting.id)}"
                        )
                        focusedSetting = None
                    else:
                        for i, value in enumerate(settingValues):
                            if value == focusedSetting.value:
                                menu.add_row(
                                    str(i + option_offset),
                                    " ) ",
                                    "Capability " + str(value) + " [green](CURRENT)",
                                )
                            else:
                                menu.add_row(str(i + option_offset), " ) ", "Capability " + str(value))

                        console.print(f"[bold blue]Setting Menu: ({str(focusedSetting.id)})")
                        console.print(menu)
                        option = IntPrompt.ask(
                            prompt="Select an option from the menu above",
                            choices=[str(i) for i in range(len(settingValues) + option_offset)],
                            show_choices=False,
                        )
                        if option == 0:
                            focusedSetting = None
                        else:
                            console.print(
                                f"Changing setting {str(focusedSetting.id)} value to {str(settingValues[option - option_offset])}"
                            )

                            logger.debug(
                                f"Changing setting {str(focusedSetting.id)} to {str(settingValues[option - option_offset])}"
                            )
                            response = settingHandler.set(settingValues[option - option_offset])
                            logger.debug(response)
                            focusedSetting.value = settingValues[option - option_offset]
            else:
                presetDemo(cameraModel)
                collectionCacheInvalidated = True
                activeCacheInvalidated = True
                menuMode = MenuMode.MAIN


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
