package com.warsay.high

import android.net.Uri
import android.os.Handler
import android.os.Looper
import androidx.annotation.OptIn
import androidx.media3.common.C
import androidx.media3.common.MediaItem
import androidx.media3.common.PlaybackException
import androidx.media3.common.PlaybackParameters
import androidx.media3.common.Player
import androidx.media3.common.VideoSize
import androidx.media3.common.util.UnstableApi
import androidx.media3.datasource.BaseDataSource
import androidx.media3.datasource.DataSource
import androidx.media3.datasource.DataSpec
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.source.ProgressiveMediaSource
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import io.flutter.view.TextureRegistry
import java.io.File

/** ExoPlayer DataSource reading decrypted bytes straight from [FourChunkReader]: no HTTP server, no temp file. */
@OptIn(UnstableApi::class)
class FourDataSource(private val reader: FourChunkReader) : BaseDataSource(false) {
    private var uri: Uri? = null
    private var pos = 0L
    private var remaining = 0L
    private var opened = false

    override fun open(dataSpec: DataSpec): Long {
        uri = dataSpec.uri
        transferInitializing(dataSpec)
        pos = dataSpec.position
        if (pos > reader.length) throw java.io.EOFException()
        remaining = if (dataSpec.length != C.LENGTH_UNSET.toLong()) dataSpec.length else reader.length - pos
        opened = true
        transferStarted(dataSpec)
        return remaining
    }

    override fun read(buffer: ByteArray, offset: Int, length: Int): Int {
        if (length == 0) return 0
        if (remaining == 0L) return C.RESULT_END_OF_INPUT
        val n = reader.read(pos, buffer, offset, minOf(length.toLong(), remaining).toInt())
        if (n < 0) return C.RESULT_END_OF_INPUT
        pos += n
        remaining -= n
        bytesTransferred(n)
        return n
    }

    override fun getUri(): Uri? = uri

    override fun close() {
        if (opened) {
            opened = false
            transferEnded()
        }
        uri = null
    }
}

/**
 * Channel `com.warsay.high/video`: encrypted 16:9 playback on a Flutter texture.
 *   create {path, key} → {id}     play/pause/seek{ms}/speed{rate}/state/dispose  (all take {id})
 */
@OptIn(UnstableApi::class)
class FourVideoChannel(private val activity: android.app.Activity) {
    private class Session(val player: ExoPlayer, val producer: TextureRegistry.SurfaceProducer, val reader: FourChunkReader) {
        var error: String? = null
        var w = 0
        var h = 0
    }

    private val sessions = HashMap<Long, Session>()
    private val main = Handler(Looper.getMainLooper())

    fun attach(engine: FlutterEngine) {
        val textures = engine.renderer
        MethodChannel(engine.dartExecutor.binaryMessenger, "com.warsay.high/video").setMethodCallHandler { call, result ->
            try {
                when (call.method) {
                    "create" -> result.success(mapOf("id" to create(textures, call.argument<String>("path")!!, call.argument<ByteArray>("key")!!)))
                    "play" -> { s(call.argument<Number>("id"))?.player?.play(); result.success(null) }
                    "loop" -> { s(call.argument<Number>("id"))?.player?.repeatMode = if (call.argument<Boolean>("on") == true) Player.REPEAT_MODE_ONE else Player.REPEAT_MODE_OFF; result.success(null) }
                    "pause" -> { s(call.argument<Number>("id"))?.player?.pause(); result.success(null) }
                    "seek" -> { s(call.argument<Number>("id"))?.player?.seekTo(call.argument<Number>("ms")!!.toLong()); result.success(null) }
                    "speed" -> { s(call.argument<Number>("id"))?.player?.playbackParameters = PlaybackParameters(call.argument<Number>("rate")!!.toFloat()); result.success(null) }
                    "state" -> {
                        val x = s(call.argument<Number>("id"))
                        if (x == null) result.success(null) else {
                            val p = x.player
                            result.success(mapOf(
                                "pos" to p.currentPosition,
                                "dur" to (if (p.duration == C.TIME_UNSET) 0L else p.duration),
                                "buf" to p.bufferedPosition,
                                "playing" to p.isPlaying,
                                "buffering" to (p.playbackState == Player.STATE_BUFFERING),
                                "ended" to (p.playbackState == Player.STATE_ENDED),
                                "w" to x.w, "h" to x.h,
                                "error" to x.error,
                            ))
                        }
                    }
                    "dispose" -> { dispose(call.argument<Number>("id")?.toLong()); result.success(null) }
                    else -> result.notImplemented()
                }
            } catch (e: Throwable) {
                HighLog.e("video ${call.method} failed", e)
                result.error("video", "${e.javaClass.simpleName}: ${e.message}", null)
            }
        }
    }

    private fun s(id: Number?) = id?.let { sessions[it.toLong()] }

    private fun create(textures: TextureRegistry, path: String, key: ByteArray): Long {
        val reader = FourChunkReader(File(path), key)
        key.fill(0)
        val producer = textures.createSurfaceProducer()
        val player = ExoPlayer.Builder(activity).build()
        val session = Session(player, producer, reader)
        val factory = DataSource.Factory { FourDataSource(reader) }
        player.setMediaSource(ProgressiveMediaSource.Factory(factory).createMediaSource(MediaItem.fromUri(Uri.parse("four://${producer.id()}"))))
        producer.setCallback(object : TextureRegistry.SurfaceProducer.Callback {
            override fun onSurfaceAvailable() { player.setVideoSurface(producer.surface) }
            override fun onSurfaceCleanup() { player.clearVideoSurface() }
        })
        player.setVideoSurface(producer.surface)
        player.addListener(object : Player.Listener {
            override fun onVideoSizeChanged(v: VideoSize) {
                if (v.width > 0 && v.height > 0) {
                    // rotated phone videos report the display size via pixelWidthHeightRatio; keep it simple: stored size
                    session.w = (v.width * v.pixelWidthHeightRatio).toInt()
                    session.h = v.height
                    producer.setSize(v.width, v.height)
                }
            }
            override fun onPlayerError(error: PlaybackException) {
                session.error = error.cause?.javaClass?.simpleName ?: error.errorCodeName
                HighLog.e("video playback error", error)
            }
        })
        player.prepare()
        sessions[producer.id()] = session
        return producer.id()
    }

    private fun dispose(id: Long?) {
        val x = id?.let { sessions.remove(it) } ?: return
        x.player.release()
        x.producer.release()
        x.reader.close()
    }

    fun disposeAll() = sessions.keys.toList().forEach { dispose(it) }
}
