function startGame() {
	if (window.gameActive) {
		return false
	}
	var playersExist = document.getElementsByClassName("player-tile").length>0;
	var teamsExist = document.getElementsByClassName("team-tile").length>0;
	if (playersExist && teamsExist) {
		window.gameActive = true;
		gameFue = document.getElementById('game-pen').querySelector('.fue-text')
		gameFue.style.display = 'none'
		createGameScreen()
		setScoresTo(0)
	}
}
document.getElementById("game-pen").addEventListener("click",  startGame)


function createGameScreen() {
	var playerPen = document.getElementById("player-pen");
	var gamePen = document.getElementById('game-pen');
	playerPen.className += ' game-active';
	gamePen.className = 'col-md-12';
	console.log("game-pen should be expanded and player-pen")
	createReadyScreen(gamePen);
	createAnswerScreen();
}


function createReadyScreen(gamePen) {
	var fillerDiv = document.createElement('div');
	fillerDiv.innerHTML = "Ready for a buzz"
	fillerDiv.className = 'show'
	fillerDiv.id = 'buzzer-ready-text'
	gamePen.appendChild(fillerDiv);
	console.log("should see ready screen")
}


function createAnswerScreen() {
	var gamePen = document.getElementById('game-pen');
	var answerArea = document.createElement('div');
	gamePen.appendChild(answerArea)
	createBuzzDisplay(answerArea)
	createscoreArea(answerArea)
	createResetArea(answerArea)
	answerArea.id = 'answer-area'
	answerArea.className = 'row'
	answerArea.style.display='none'
}


function createBuzzDisplay(gamePen) {
	var buzzDisplayDiv = document.createElement('div');
	gamePen.appendChild(buzzDisplayDiv);
	buzzDisplayDiv.id = 'who-buzzed-in';
	buzzDisplayDiv.className = 'col-md-6';
}



function createscoreArea(gamePen) {
	var scoreBoxDiv = document.createElement('div');
	scoreBoxDiv.id = 'score-area';
	scoreBoxDiv.className = 'col-md-4';
	rawHtml = "<input type='text' id='answer-field' onkeypress='return event.charCode >= 48 && event.charCode <= 57'></input>"
	scoreBoxDiv.innerHTML = rawHtml
	gamePen.appendChild(scoreBoxDiv);
}



function createResetArea(gamePen) {
	var resetAreaDiv = document.createElement('div');
	resetAreaDiv.id = 'resetArea';
	resetAreaDiv.className = 'col-md-4';
	createResetButton(resetAreaDiv)
	gamePen.appendChild(resetAreaDiv);

}


function createResetButton(resetAreaDiv) {
	var resetButton = document.createElement("button");
	resetButton.id = 'answer-button'
	resetButton.innerHTML = "record answer";
	resetAreaDiv.appendChild(resetButton)
}

// function updateScore() {
//     rosters = document.getElementsByClassName("roster-pen")
//     for (i=0; i<rosters.length; i++) {
//         team = rosters[i].parentElement
//         teamScoreDiv = team.querySelector('.team-score')
//         teamScore = 0
//         rosterPlayers = rosters[i].childNodes
//         for (j=0; j<rosterPlayers.length; j++) {
//             player = rosterPlayers[j]
//             playerData = JSON.parse(sessionStorage.getItem(player.id))
//             console.log(player.id)
//             console.log(playerData['team'])
//             playerScoreDiv = document.getElementById(player.id).querySelector(".player-score");
//             playerScore = parseInt(playerData['score'])
//             playerScoreDiv.innerHTML = playerScore
//             teamScore = parseInt(teamScore) + parseInt(playerScore)
//             sessionStorage.setItem(player.id, JSON.stringify(playerData))
//         }
//         teamScoreDiv.innerHTML = teamScore
//     }   
// }

function setScoresTo(val=0) {
	rosters = document.getElementsByClassName("roster-pen")
	for (i=0; i<rosters.length; i++) {
		rosterPlayers = rosters[i].childNodes
		for (j=0; j<rosterPlayers.length; j++) {
			player = rosterPlayers[j]
			playerData = JSON.parse(sessionStorage.getItem(player.id))
			playerData['score'] = 0
			sessionStorage.setItem(player.id, JSON.stringify(playerData))
		}
	}
	updateScore()
}
