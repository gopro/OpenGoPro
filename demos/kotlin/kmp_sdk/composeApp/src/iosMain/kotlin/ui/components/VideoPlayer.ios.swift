package ui.components

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier

// https://medium.com/@adman.shadman/creating-a-cross-platform-video-player-component-in-kotlin-multiplatform-android-ios-9d79174aa2ca

@Composable
actual fun VideoPlayer(
    modifier: Modifier,
    url: String,
    isLandscape: Boolean,
    shouldStop: Boolean,
    onMediaReadyToPlay: () -> Unit
) {
    let player = AVPlayer(url: URL(string: url)!)
    let playerLayer = AVPlayerLayer(player: player)
    let avPlayerViewController = AVPlayerViewController()
    avPlayerViewController.player = player
    avPlayerViewController.showsPlaybackControls = true

    if isLandscape {
        UIDevice.current.setValue(UIInterfaceOrientation.landscapeRight.rawValue, forKey: "orientation")
        UIApplication.shared.setStatusBarOrientation(UIInterfaceOrientation.unknown, animated: true)
    }

    UIKitView(
        factory: {
        let playerContainer = UIView()
        playerContainer.addSubview(avPlayerViewController.view)
        return playerContainer
    },
    update: { view, context in
        if shouldStop {
            player.pause()
            avPlayerViewController.player?.play()
            player.seek(to: .zero)
        } else {
            player.play()
        }
    }
    )
}