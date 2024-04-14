const FRAME_DURATION = 1000
export class Player {
  constructor(playerID, controlsID, frameCount) {
    this.playerDiv = document.getElementById(playerID)
    this.controlsDiv = document.getElementById(controlsID)
    this.frameCount = frameCount
    this.imgs = this.playerDiv.querySelectorAll('img');
    // this.imgMap = new Map([...this.imgs].map((el, n) => [el, n]))
    const pauseButton = this.controlsDiv.querySelector('button[name="play-pause"]');
    const nextButton = this.controlsDiv.querySelector('button[name="next"]');
    const prevButton = this.controlsDiv.querySelector('button[name="prev"]');
    const inputField = this.controlsDiv.querySelector('input[name="inputField"]');
    console.log(pauseButton, nextButton, prevButton, inputField)
    this.frameNum = 0
    this.pause()
  }

  play() {
    this.playing = true
    this.lastFrameTime = performance.now()
    this.controlsDiv.classList.add('playing')
    this.sync()
    this.onAnimationFrame()
  }

  pause() {
    this.sync()
    this.playing = false
    this.controlsDiv.classList.remove('playing')
    this.lastFrameTime = performance.now()
  }

  // Must be explictly bound for callback
  onAnimationFrame = () => {
    if (!this.playing) return
    const currentTime = performance.now()
    const frameElapsed = currentTime - this.lastFrameTime 
    if (frameElapsed > FRAME_DURATION) {
      this.advanceFrame()
    }
    requestAnimationFrame(this.onAnimationFrame);
  }

  advanceFrame() {
    this.lastFrameTime = performance.now()
    this.frameNum++
    this.sync()
  }

  sync() {
    this.frameNum = this.frameNum % this.frameCount
    const shownImgs = this.playerDiv.querySelectorAll('.shown');
    for (const img of shownImgs) {
      img.classList.remove("shown")
    }
    this.imgs[this.frameNum].classList.add("shown")
  }
}
