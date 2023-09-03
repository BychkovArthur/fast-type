const getWPM = (timeStart, correctlyTypedSymbols, textObject) => {
    const timeNow = Date.now()
    const time = timeNow - timeStart
    const WPM = ((correctlyTypedSymbols.count / 5) / (time / 1000 / 60)).toFixed(0)
    textObject.textContent = WPM
}

const formatMilliseconds = (milliseconds) => {
    let seconds = Math.floor((milliseconds / 1000) % 60);
    let minutes = Math.floor((milliseconds / (1000 * 60)) % 60);
  
    // Добавляем ведущий ноль для однозначных значений
    if (seconds < 10) {
      seconds = "0" + seconds;
    }
    if (minutes < 10) {
        minutes = "0" + minutes;
      }

  
    return minutes + ":" + seconds;
}

const updateTime = (timeStart, timeParagraph) => {
    const timeNow = Date.now()
    const time = (timeNow - timeStart).toFixed(0)
    timeParagraph.textContent = formatMilliseconds(time)
}

export {
    getWPM,
    updateTime
}