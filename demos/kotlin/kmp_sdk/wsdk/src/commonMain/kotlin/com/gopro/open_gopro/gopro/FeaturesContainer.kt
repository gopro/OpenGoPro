/* FeaturesContainer.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:29 UTC 2025 */

package com.gopro.open_gopro.gopro

import com.gopro.open_gopro.domain.connector.ICameraConnector
import com.gopro.open_gopro.domain.gopro.IGoProFactory
import kotlinx.coroutines.CoroutineScope

internal interface IFeatureContext {
  val gopro: GoPro
  val connector: ICameraConnector
  val facadeFactory: IGoProFactory
  val scope: CoroutineScope
}

internal data class FeatureContext(
    override val gopro: GoPro,
    override val connector: ICameraConnector,
    override val facadeFactory: IGoProFactory,
    override val scope: CoroutineScope
) : IFeatureContext

/**
 * Container used to access and exercise features
 *
 * @param featureContext
 */
class FeaturesContainer internal constructor(featureContext: IFeatureContext) {
  val accessPoint = AccessPointFeature(featureContext)
  val cohn = CohnFeature(featureContext)
  val connectWifi = ConnectWifiFeature(featureContext)
}
