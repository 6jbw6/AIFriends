/*
 * 将 MediaRecorder 录出的音频 Blob(webm/ogg 等)解码后
 * 重编码为 16-bit PCM 单声道 WAV 文件,
 * 以满足语音复刻接口对音频格式的要求。
 */

export async function blobToWavFile(blob, filename = 'record.wav') {
    const arrayBuffer = await blob.arrayBuffer()
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)()
    let audioBuffer
    try {
        audioBuffer = await audioCtx.decodeAudioData(arrayBuffer)
    } finally {
        await audioCtx.close()
    }
    // 多声道混合为单声道
    const length = audioBuffer.length
    const mono = new Float32Array(length)
    for (let ch = 0; ch < audioBuffer.numberOfChannels; ch++) {
        const data = audioBuffer.getChannelData(ch)
        for (let i = 0; i < length; i++) {
            mono[i] += data[i] / audioBuffer.numberOfChannels
        }
    }
    const wavBuffer = encodeWav(mono, audioBuffer.sampleRate)
    return new File([wavBuffer], filename, {type: 'audio/wav'})
}

function encodeWav(samples, sampleRate) {
    const buffer = new ArrayBuffer(44 + samples.length * 2)
    const view = new DataView(buffer)
    const writeString = (offset, str) => {
        for (let i = 0; i < str.length; i++) {
            view.setUint8(offset + i, str.charCodeAt(i))
        }
    }
    writeString(0, 'RIFF')
    view.setUint32(4, 36 + samples.length * 2, true)
    writeString(8, 'WAVE')
    writeString(12, 'fmt ')
    view.setUint32(16, 16, true)
    view.setUint16(20, 1, true)          // PCM
    view.setUint16(22, 1, true)          // 单声道
    view.setUint32(24, sampleRate, true)
    view.setUint32(28, sampleRate * 2, true)
    view.setUint16(32, 2, true)
    view.setUint16(34, 16, true)
    writeString(36, 'data')
    view.setUint32(40, samples.length * 2, true)
    let offset = 44
    for (let i = 0; i < samples.length; i++) {
        const s = Math.max(-1, Math.min(1, samples[i]))
        view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true)
        offset += 2
    }
    return buffer
}
