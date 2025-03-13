/* TestAppDatabase.kt/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro). */
/* This copyright was auto-generated on Tue Feb 18 18:41:30 UTC 2025 */

package com.gopro.open_gopro.database

import android.content.Context
import androidx.room.Room
import androidx.test.core.app.ApplicationProvider
import com.gopro.open_gopro.operations.jsonDefault
import kotlin.test.assertEquals
import kotlinx.coroutines.test.runTest
import kotlinx.serialization.encodeToString
import org.junit.After
import org.junit.Before
import org.junit.Test

class TestAppDatabase {
  private lateinit var ssidDao: SsidDao
  private lateinit var httpsCredentialsDao: HttpsCredentialsDao
  private lateinit var certificatesDao: CertificatesDao
  private lateinit var db: AppDatabase

  @Before
  fun createDb() {
    val context = ApplicationProvider.getApplicationContext<Context>()
    db = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java).build()
    ssidDao = db.ssidDao()
    httpsCredentialsDao = db.httpsCredentialsDao()
    certificatesDao = db.certificatesDao()
  }

  @After
  fun closeDb() {
    db.close()
  }

  @Test
  fun testSsidDao() = runTest {
    // Add an retrieve one entry
    val ssidDbEntry1 = SsidDbEntry(serialId = "1234", ssid = "ssid", password = "password")
    ssidDao.insert(ssidDbEntry1)
    assertEquals(1, ssidDao.count())
    ssidDao.loadAll("1234").let { results ->
      assertEquals(1, results.size)
      with(results.first()) {
        assertEquals(ssidDbEntry1.serialId, serialId)
        assertEquals(ssidDbEntry1.ssid, ssid)
        assertEquals(ssidDbEntry1.password, password)
      }
    }

    // Overwrite and get new entry
    val ssidDbEntry2 = SsidDbEntry(serialId = "1234", ssid = "ssid2", password = "password2")
    ssidDao.insert(ssidDbEntry2)
    assertEquals(1, ssidDao.count())
    ssidDao.loadAll("1234").let { results ->
      assertEquals(1, results.size)
      with(results.first()) {
        assertEquals(ssidDbEntry2.serialId, serialId)
        assertEquals(ssidDbEntry2.ssid, ssid)
        assertEquals(ssidDbEntry2.password, password)
      }
    }

    // Add and get a second entry
    val ssidDbEntry3 = SsidDbEntry(serialId = "5678", ssid = "ssid2", password = "password2")
    ssidDao.insert(ssidDbEntry3)
    assertEquals(2, ssidDao.count())
    ssidDao.loadAll("5678").let { results ->
      assertEquals(1, results.size)
      with(results.first()) {
        assertEquals(ssidDbEntry3.serialId, serialId)
        assertEquals(ssidDbEntry3.ssid, ssid)
        assertEquals(ssidDbEntry3.password, password)
      }
    }

    // Delete all entries
    ssidDao.delete(SerialIdDb("1234"))
    ssidDao.delete(SerialIdDb("5678"))
    assertEquals(0, ssidDao.count())
  }

  @Test
  fun testHttpsCredentialsDao() = runTest {
    // Add an retrieve one entry
    val credentialsEntry1 =
        HttpsCredentialsDbEntry(serialId = "1234", username = "username", password = "password")
    httpsCredentialsDao.insert(credentialsEntry1)
    assertEquals(1, httpsCredentialsDao.count())
    httpsCredentialsDao.loadAll("1234").let { results ->
      assertEquals(1, results.size)
      with(results.first()) {
        assertEquals(credentialsEntry1.serialId, serialId)
        assertEquals(credentialsEntry1.username, username)
        assertEquals(credentialsEntry1.password, password)
      }
    }

    // Overwrite and get new entry
    val credentialsEntry2 =
        HttpsCredentialsDbEntry(serialId = "1234", username = "username2", password = "password2")
    httpsCredentialsDao.insert(credentialsEntry2)
    assertEquals(1, httpsCredentialsDao.count())
    httpsCredentialsDao.loadAll("1234").let { results ->
      assertEquals(1, results.size)
      with(results.first()) {
        assertEquals(credentialsEntry2.serialId, serialId)
        assertEquals(credentialsEntry2.username, username)
        assertEquals(credentialsEntry2.password, password)
      }
    }

    // Add and retrieve a second entry
    val credentialsEntry3 =
        HttpsCredentialsDbEntry(serialId = "5678", username = "username2", password = "password2")
    httpsCredentialsDao.insert(credentialsEntry3)
    assertEquals(2, httpsCredentialsDao.count())
    httpsCredentialsDao.loadAll("5678").let { results ->
      assertEquals(1, results.size)
      with(results.first()) {
        assertEquals(credentialsEntry3.serialId, serialId)
        assertEquals(credentialsEntry3.username, username)
        assertEquals(credentialsEntry3.password, password)
      }
    }

    // Delete all entries
    httpsCredentialsDao.delete(SerialIdDb("1234"))
    assertEquals(1, httpsCredentialsDao.count())
    httpsCredentialsDao.delete(SerialIdDb("5678"))
    assertEquals(0, httpsCredentialsDao.count())
  }

  @Test
  fun testCertificatesDao() = runTest {
    // Add an retrieve one entry
    val certs = CertificatesForDb(listOf("certificate1", "certificate2"))
    val certificateEntry1 =
        CertificatesDbEntry(serialId = "1234", certificates = jsonDefault.encodeToString(certs))
    certificatesDao.insert(certificateEntry1)
    assertEquals(1, certificatesDao.count())
    certificatesDao.loadAll("1234").let { results ->
      assertEquals(1, results.size)
      with(results.first()) {
        assertEquals(certificateEntry1.serialId, serialId)
        val decodedCerts =
            com.gopro.open_gopro.operations.jsonDefault
                .decodeFromString<CertificatesForDb>(certificates)
                .certificates
        assertEquals(2, decodedCerts.size)
      }
    }
  }
}
