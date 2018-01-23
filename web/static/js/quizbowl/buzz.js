function playerEvent(playerId) {
    console.log('player event')
    if (sessionStorage.getItem(playerId) !== null) {
        flashPlayerTile(playerId)
        console.log('div flash')
    }
    else {
        createPlayerEvent(playerId)
        console.log('create player event')
    }
};


function answerEvent(playerId) {
    // if (sessionStorage.getItem(playerId===null)) {
    //     console.log("playerId " + playerId + " doesn't exist")
    //     return false
    // }
    buzzInfo = document.getElementById('who-buzzed-in')
    playerData = JSON.parse(sessionStorage.getItem(playerId))
    buzzInfo.innerHTML = playerData['name'] + ' buzzed in!'
    fillerArea = document.getElementById('buzzer-ready-text')
    fillerArea.style.display = 'none'
    answerArea = document.getElementById('answer-area')
    answerArea.style.display = 'block'
    window.buzzerActive = false; 
    console.log('ok we should be listening for a click to award points to '+playerId)
    sessionStorage.setItem('answeringPlayer', playerId)
};


function awardPoints() {
    console.log('trying to award points!')
    pointsAwarded = document.getElementById("answer-field").value;
    playerAnswering = sessionStorage.getItem('answeringPlayer')
    playerData = JSON.parse(sessionStorage.getItem(playerAnswering))
    console.log('player ' + playerId + ' started with ' + parseInt(playerData['score']) + ' points')
    score = parseInt(playerData['score']) + parseInt(pointsAwarded)
    playerData['score'] = score
    sessionStorage.setItem(playerId, JSON.stringify(playerData))
    console.log('trying to give player ' + playerId + ' ' + score + ' points')
    updatePlayerTile(playerId, score)
    updateTeamTile(playerData['team'], pointsAwarded)
    openBuzzers()
}


function openBuzzers() {
    sessionStorage.removeItem('answeringPlayer')
    fillerArea = document.getElementById('buzzer-ready-text')
    fillerArea.style.display = 'block'
    answerArea = document.getElementById('answer-area')
    answerArea.style.display = 'none'
    window.buzzerActive = true;
}


function updatePlayerTile(playerId, score) {
    playerScoreDiv = document.getElementById(playerId).querySelector('.player-score')
    playerScoreDiv.innerHTML = score
}

function updateTeamTile(teamId, playerScore) {
    teamScoreDiv = document.getElementById(teamId).querySelector('.team-score')
    existingScore = parseInt(teamScoreDiv.innerHTML)
    newTeamScore = parseInt(existingScore) + parseInt(playerScore)
    teamScoreDiv.innerHTML = newTeamScore
}

function buzzEvent(event) {
    if (!window.buzzerActive) {
        console.log('no buzzing allowed!')
        return false
    }
    playerId = event.code
    var playerExists = sessionStorage.getItem(playerId) !== null
    if (playerExists&&window.gameActive) {
            answerEvent(playerId)
            console.log("sending playerId to answerEvent as " + playerId)
            answerEvent(playerId)
            document.getElementById("answer-button").addEventListener("click", awardPoints)            
    }

    else if (playerExists&&!window.gameActive) {
            flashPlayerTile(playerId)
    }

    else if (!playerExists&&!window.gameActive) {
            playerEvent(event.code)
    }
    else {
        return false
    }
};

document.addEventListener("keypress",  buzzEvent)


