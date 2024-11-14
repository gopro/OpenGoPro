package media

import entity.operation.GroupMediaItemType
import entity.operation.GroupedMediaListItem
import entity.operation.MediaList
import entity.operation.MediaListItem
import entity.operation.jsonDefault
import vectors.groupedMediaListItemJson
import vectors.mediaListJson2
import vectors.singleMediaListItemJson
import kotlin.test.Test
import kotlin.test.assertContentEquals
import kotlin.test.assertEquals
import kotlin.test.assertNull

class TestMediaList {
    @Test
    fun `parse single media list item`() {
        // WHEN
        val singleMediaListItem =
            jsonDefault.decodeFromString<MediaListItem>(singleMediaListItemJson)

        // THEN
        with(singleMediaListItem) {
            assertEquals("GX017060.MP4", filename) // n
            assertEquals(1659744181, creationTime) // cre
            assertEquals(1659744181, modifiedTime) // mod
            assertEquals(329080, lowResVideoSize) // glrv
            assertEquals(-1, lowResFileSize) // ls
            assertEquals(4489890, fileSize) // s
        }
    }

    @Test
    fun `parse grouped media list item`() {
        // WHEN
        val singleMediaListItem =
            jsonDefault.decodeFromString<MediaListItem>(groupedMediaListItemJson) as GroupedMediaListItem

        // THEN
        with(singleMediaListItem) {
            assertEquals("G0017061.JPG", filename) // n
            assertEquals(1, groupId) // g
            assertEquals(7061, firstGroupMemberId) // b
            assertEquals(7090, lastGroupMemberId) // l
            assertEquals(1729860144, creationTime) // cre
            assertEquals(1729860144, modifiedTime) // mod
            assertEquals(170856763, fileSize) // s
            assertEquals(GroupMediaItemType.BURST, groupType) // t
            assertContentEquals(listOf(), missingFileIds) // m

            assertNull(lowResVideoSize) // glrv
            assertNull(lowResFileSize) // ls
        }
    }

    @Test
    fun `parse media list`() {
        // WHEN
        val mediaList = jsonDefault.decodeFromString<MediaList>(mediaListJson2)

        // THEN
        assertEquals(1, mediaList.media.size)
    }
}