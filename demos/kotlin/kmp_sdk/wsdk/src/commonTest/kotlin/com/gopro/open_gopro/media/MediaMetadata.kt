/* MediaMetadata.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.media

import com.gopro.open_gopro.operations.AudioOption
import com.gopro.open_gopro.operations.LensConfig
import com.gopro.open_gopro.operations.LensProjection
import com.gopro.open_gopro.operations.MediaContentType
import com.gopro.open_gopro.operations.MediaMetadata
import com.gopro.open_gopro.operations.PhotoMediaMetadata
import com.gopro.open_gopro.operations.VideoMediaMetadata
import com.gopro.open_gopro.operations.jsonDefault
import kotlin.test.Test
import kotlin.test.assertContentEquals
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue
import vectors.photoMetadataJson
import vectors.problematicMetadataJson
import vectors.videoMetadataJson
import vectors.videoMetadataJson2

class TestMediaMetadata {
  @Test
  fun `parse photo media metadata`() {
    // WHEN
    val metadata =
        jsonDefault.decodeFromString<MediaMetadata>(photoMetadataJson) as PhotoMediaMetadata

    // THEN
    with(metadata) {
      assertEquals(1648787120, creationTime) // cre
      assertEquals(3645396, fileSize) // s
      assertEquals(0, numHilights) // hc
      assertFalse { isUploaded } // us
      assertContentEquals(listOf(), offloadState) // mos
      assertFalse { isStabilized } // eis
      assertFalse { isHighDynamicRange!! } // hdr
      assertFalse { isWideDynamicRange!! } // wdr
      assertFalse { isRaw!! } // raw
      assertFalse { isTranscoded } // tr
      assertFalse { isMetadataPresent } // mp
      assertEquals(MediaContentType.SINGLE_PHOTO, contentType) // ct
      assertEquals("28", fov) // fov
      assertEquals(LensConfig.FRONT, lensConfig) // lc
      assertEquals(LensProjection.ERROR, lensProjection) // prjn
      assertEquals("a1a5834aa7714de5a36da58426829da2", id) // gumi
      assertEquals(5568, width) // w
      assertEquals(4872, height) // h
    }
  }

  @Test
  fun `parse video media metadata`() {
    // WHEN
    val metadata = jsonDefault.decodeFromString<VideoMediaMetadata>(videoMetadataJson)

    // THEN
    with(metadata) {
      assertEquals(1659769382, creationTime) // cre
      assertEquals(4489890, fileSize) // s
      assertEquals(0, maxAutoHilightScore) // mahs
      assertFalse { isUploaded } // us
      assertContentEquals(listOf(), offloadState) // mos
      assertFalse { isStabilized } // eis
      assertTrue { isProtuneAudio } // pta
      assertEquals(AudioOption.STEREO, audioOption) // ao
      assertFalse { isTranscoded } // tr
      assertFalse { isMetadataPresent } // mp
      assertEquals(MediaContentType.VIDEO, contentType) // ct
      assertEquals("0", fov) // fov
      assertEquals(LensConfig.FRONT, lensConfig) // lc
      assertEquals(LensProjection.ERROR, lensProjection) // prjn
      assertEquals("4bd0acdfc13ff52ba7b3f8c593cc932f", id) // gumi
      assertEquals(329080, lrvFileSize) // ls
      assertFalse { isClipped } // cl
      assertEquals(255, videoCodecProfile) // avc_profile
      assertEquals(255, videoCodecLevel) // profile
      assertEquals(0, numHilights) // hc
      assertContentEquals(listOf(), hilightList) // hi
      assertEquals(3, duration) // dur
      assertEquals(3840, width) // w
      assertEquals(2160, height) // h
      assertEquals(30000, frameRate) // fps
      assertEquals(1001, frameRateDenominator) // fps_denom
      assertTrue { isProgressive!! } // prog
      assertFalse { isSubsampled } // subsample
    }
  }

  @Test
  fun `parse a different video media metadata`() {
    // WHEN
    val metadata = jsonDefault.decodeFromString<VideoMediaMetadata>(videoMetadataJson2)

    // THEN
    assertFalse { metadata.isSubsampled }
  }

  @Test
  fun `parse problematic media metadata`() {
    // WHEN
    val metadata = jsonDefault.decodeFromString<VideoMediaMetadata>(problematicMetadataJson)

    // THEN
    assertFalse { metadata.isSubsampled }
  }
}
