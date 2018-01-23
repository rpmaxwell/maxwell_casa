sessionStorage.clear();
// var players = [];
// var teams = [];

// document.addEventListener("keypress", function(event) {
//     playerEvent(event.code)
// });


// function playerEvent(playerId) {
// 	if (sessionStorage.getItem(playerId) !== null) {
// 		flashPlayerTile(playerId)
// 	}
// 	else {
// 		playerName = prompt("A new player has buzzed! enter a name");
// 		if (playerName == null || playerName == "") {
//     			return false
// 			}
// 		else {
// 			createPlayer(playerId, playerName)
// 			updateFue()			
// 		}
// 	}
// };

function isValidPlayerName(playerName) {
    if (playerName == null || playerName == "") {
		return false
    }
        else {
            return true
        }
}


function createPlayerEvent(playerId) {
	playerName = prompt("A new player has buzzed! enter a name");
	if (!isValidPlayerName(playerName)) {
		return false
	}
	var playerPayload = {
    	name:  playerName,
    	team: null,
    	score: null
	}
	sessionStorage.setItem(playerId, JSON.stringify(playerPayload));
	createPlayerTile(playerId, playerPayload)
	updateFue()
};



function flashPlayerTile(playerId) {
var playerTile = document.getElementById(playerId),
    flashClass = 'flash';
  	playerTile.classList.add(flashClass);
	playerTile.addEventListener('animationend',function() {
  		this.classList.remove(flashClass);
	});
}


function createPlayerTile(playerId, playerData) {
	var playerTile = document.createElement('div');
	playerTile.id = playerId
	playerTile.className = 'row player-tile'
	//create child node with name
	var playerNameDiv = document.createElement('div');
	playerNameDiv.innerHTML = playerData['name'];
	playerNameDiv.className = 'col-md-8 player-name';
	// create child node with score
	var playerScoreDiv = document.createElement('div');
	playerScoreDiv.innerHTML = playerData['score']
	playerScoreDiv.className = 'col-md-4 player-score'
	playerTile.appendChild(playerNameDiv);
	playerTile.appendChild(playerScoreDiv);
	document.getElementById('player-pen').appendChild(playerTile);
};





// function updateFue() {
// 	pen = document.getElementById('player-pen')
// 	player = document.getElementsByClassName('fue-text')
// 	for (i=0; i<player.length; i++) {
// 		if (player[i].parentElement.id=='player-pen') {
// 			player[i].parentNode.removeChild(player[i])
// 		}
// 		if (player[i].parentElement.id=='game-pen') {
// 			player[i].innerHTML = 'Add teams to start the game!'
// 		}
// 	}
// }


function updateFue() {

	var playersExist = document.getElementsByClassName("player-tile").length>0;
	var teamsExist = document.getElementsByClassName("team-tile").length>0;
	fueMessages = document.getElementsByClassName('fue-text');
	
	
	for (i=0; i<fueMessages.length; i++) {
		if (fueMessages[i].parentElement.id=='player-pen') {
			if (playersExist) {
				fueMessages[i].parentNode.removeChild(fueMessages[i])
			}
		}
		else if (fueMessages[i].parentElement.id=='team-pen') {
			if (teamsExist) {
				fueMessages[i].parentNode.removeChild(fueMessages[i])
			}
		}
		else if (fueMessages[i].parentElement.id=='game-pen') {
			if (teamsExist && playersExist) {
				fueMessages[i].innerHTML = "click to start the game!"
			}
			else if (!teamsExist && playersExist) {
				fueMessages[i].innerHTML = "add a team to start the game!"

			}
			else if (teamsExist && !playersExist) {
				fueMessages[i].innerHTML = "add players to start the game!"
			}
		}
	}
};


