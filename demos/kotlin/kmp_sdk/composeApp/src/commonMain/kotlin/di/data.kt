package di

import data.IAppPreferences
import data.IAppPreferencesImpl
import org.koin.dsl.module


val dataModule = module {
    single<IAppPreferences> { IAppPreferencesImpl(get()) }
}