package media

import entity.operation.AudioOption
import entity.operation.LensConfig
import entity.operation.LensProjection
import entity.operation.MediaContentType
import entity.operation.VideoMediaMetadata
import entity.operation.MediaMetadata
import entity.operation.PhotoMediaMetadata
import entity.operation.jsonDefault
import vectors.photoMetadataJson
import vectors.videoMetadataJson
import vectors.videoMetadataJson2
import kotlin.test.Test
import kotlin.test.assertContentEquals
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertTrue

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
            assertEquals(AudioOption.STEREO, audioOption)  // ao
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
}