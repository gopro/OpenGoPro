# Developer README

## Build

`./gradlew :composeApp:assembleDebug`
`./gradlew :simplifiedApp:assembleDebug`
`./gradlew :composeApp:assembleRelease`
`./gradlew :simplifiedApp:assembleRelease`

## Formatting

`./gradlew ktfmtFormat`

## Linting

`./gradlew lint`

We haven't actually analyzed the lint results yet. They need to be fixed / configured.

## Testing

### Unit Testing

`./gradlew :wsdk:testDebugUnitTest`

### Instrumented Testing

TODO

## Documentation

`./gradlew dokkaHtml`

## Licenses

`./gradlew copyLicenseReport`

which will run

`./gradlew licenseReleaseReport`
 
> TODO! The copy appears to be broken due to some locked file.

## CI Notes

gradle cache?